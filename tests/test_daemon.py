from __future__ import annotations

import asyncio
import errno
import fcntl
import sys
import subprocess
from concurrent.futures import ThreadPoolExecutor
import tempfile
import unittest
from contextlib import asynccontextmanager, ExitStack
from pathlib import Path
from unittest.mock import Mock, patch

import anyio
import click

from ucli.config.models import ServerConfig
from ucli.daemon import client, lifecycle, pool, server


class LifecycleTests(unittest.TestCase):
    def setUp(self):
        self.stack = ExitStack()
        self.addCleanup(self.stack.close)
        root = Path(self.stack.enter_context(tempfile.TemporaryDirectory()))
        for name, filename in [('DAEMON_LOCK', 'daemon.lock'), ('DAEMON_PID', 'daemon.pid'),
                               ('DAEMON_SOCK', 'daemon.sock'), ('DAEMON_LOG', 'daemon.log')]:
            self.stack.enter_context(patch.object(lifecycle, name, root / filename))

    def test_socket_permission_does_not_spawn(self):
        with patch.object(client, '_send_request', side_effect=PermissionError(errno.EPERM, 'denied')), \
                patch.object(lifecycle.subprocess, 'Popen') as launch:
            with self.assertRaisesRegex(click.ClickException, 'Cannot access daemon'):
                lifecycle.ensure_daemon()
            launch.assert_not_called()

    def test_ping_only_absence_returns_false(self):
        for exc in (FileNotFoundError(), ConnectionRefusedError()):
            with patch.object(client, '_send_request', side_effect=exc):
                self.assertFalse(client.ping())
        for exc in (PermissionError(), TimeoutError(), ConnectionResetError()):
            with patch.object(client, '_send_request', side_effect=exc):
                with self.assertRaises(type(exc)):
                    client.ping()

    def test_invalid_ping_is_not_healthy(self):
        with patch.object(client, '_send_request', return_value={'ok': True, 'result': 'wrong'}):
            with self.assertRaises(ValueError):
                client.ping()

    def test_live_socket_does_not_require_pid_probe(self):
        with patch.object(lifecycle, 'ping', return_value=True), \
                patch.object(lifecycle, 'is_daemon_running', side_effect=AssertionError):
            self.assertTrue(lifecycle.ensure_daemon())

    def test_pid_permission_is_not_absence(self):
        lifecycle.DAEMON_PID.write_text('123')
        with patch.object(lifecycle.os, 'kill', side_effect=PermissionError):
            self.assertTrue(lifecycle.is_daemon_running())

    def test_denied_stop_preserves_runtime_files(self):
        lifecycle.DAEMON_PID.write_text('123')
        lifecycle.DAEMON_SOCK.touch()
        with patch.object(lifecycle.os, 'kill', side_effect=PermissionError):
            with self.assertRaises(click.ClickException):
                lifecycle.stop_daemon()
        self.assertTrue(lifecycle.DAEMON_PID.exists())
        self.assertTrue(lifecycle.DAEMON_SOCK.exists())

    def test_child_failure_has_exit_code_and_log(self):
        proc = Mock()
        proc.poll.return_value = 2
        with patch.object(lifecycle, 'ping', return_value=False), \
                patch.object(lifecycle.subprocess, 'Popen', return_value=proc) as launch:
            with self.assertRaisesRegex(click.ClickException, r'exit 2.*daemon.log'):
                lifecycle.ensure_daemon()
        self.assertNotEqual(launch.call_args.kwargs['stderr'], lifecycle.subprocess.DEVNULL)

    def test_start_deadline_is_bounded(self):
        proc = Mock()
        proc.poll.return_value = None
        with patch.object(lifecycle, 'ping', return_value=False), \
                patch.object(lifecycle, 'START_WAIT_SECONDS', 0.03), \
                patch.object(lifecycle.subprocess, 'Popen', return_value=proc):
            with self.assertRaisesRegex(click.ClickException, 'not ready within'):
                lifecycle.ensure_daemon()

    def test_busy_instance_is_not_replaced_or_cleaned(self):
        lifecycle.DAEMON_PID.write_text('123')
        lifecycle.DAEMON_SOCK.touch()
        with lifecycle.DAEMON_LOCK.open('a+') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            lifecycle._cleanup_stale(123)
            with patch.object(lifecycle, 'ping', return_value=False), \
                    patch.object(lifecycle, 'START_WAIT_SECONDS', 0.03), \
                    patch.object(lifecycle.subprocess, 'Popen') as launch:
                with self.assertRaisesRegex(click.ClickException, 'lifetime lock'):
                    lifecycle.ensure_daemon()
                launch.assert_not_called()
        self.assertTrue(lifecycle.DAEMON_SOCK.exists())

    def test_cleanup_preserves_new_owner(self):
        lifecycle.DAEMON_PID.write_text('456')
        lifecycle.DAEMON_SOCK.touch()
        lifecycle._cleanup_stale(123)
        self.assertTrue(lifecycle.DAEMON_SOCK.exists())


class DaemonProcessTests(unittest.TestCase):
    setUp = LifecycleTests.setUp
    def test_concurrent_launch_and_shutdown(self):
        root = lifecycle.DAEMON_SOCK.parent
        script = root / 'run_daemon.py'
        script.write_text(
            "import asyncio, sys, time\n"
            "from pathlib import Path\n"
            f"sys.path.insert(0, {str(Path(pool.__file__).resolve().parents[2])!r})\n"
            "import ucli.constants as constants\n"
            "root = Path(sys.argv[1])\n"
            "for name, filename in [('DAEMON_LOCK', 'daemon.lock'), ('DAEMON_PID', 'daemon.pid'), "
            "('DAEMON_SOCK', 'daemon.sock'), ('DAEMON_LOG', 'daemon.log')]:\n"
            "    setattr(constants, name, root / filename)\n"
            "from ucli.daemon.server import run_daemon\n"
            "time.sleep(0.2)\n"
            "raise SystemExit(asyncio.run(run_daemon()))\n"
        )
        real_popen = subprocess.Popen
        children = []
        def spawn(args, **kwargs):
            # Keep the implementation's descriptor/session settings.
            child = real_popen([sys.executable, str(script), str(root)], **kwargs)
            children.append(child)
            return child
        try:
            with patch.object(client, 'DAEMON_SOCK', lifecycle.DAEMON_SOCK), \
                    patch.object(lifecycle.subprocess, 'Popen', side_effect=spawn):
                with ThreadPoolExecutor(max_workers=8) as callers:
                    results = list(callers.map(lambda _: lifecycle.ensure_daemon(), range(8)))
                self.assertTrue(all(results))
                self.assertEqual(len(children), 1)
                self.assertTrue(client.ping())
                children[0].terminate()
                self.assertEqual(children[0].wait(timeout=10), 0)
                self.assertFalse(lifecycle.DAEMON_PID.exists())
                self.assertFalse(lifecycle.DAEMON_SOCK.exists())
                self.assertTrue(lifecycle.ensure_daemon())
                self.assertEqual(len(children), 2)
        finally:
            for child in children:
                if child.poll() is None:
                    child.terminate()
                    child.wait(timeout=10)
        self.assertNotIn('Traceback', lifecycle.DAEMON_LOG.read_text())


class PoolTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.stack = ExitStack()
        self.addCleanup(self.stack.close)
        self.closed = []
        self.entered = []
        self.initialize_error = False
        self.initialize_wait = None
        outer = self

        @asynccontextmanager
        async def stdio(params):
            owner = asyncio.current_task()
            async with anyio.create_task_group():
                outer.entered.append('stdio')
                try:
                    yield (None, None)
                finally:
                    outer.assertIs(asyncio.current_task(), owner)
                    outer.closed.append('stdio')

        class Session:
            async def __aenter__(self):
                self.owner = asyncio.current_task()
                self.group = anyio.create_task_group()
                await self.group.__aenter__()
                outer.entered.append('session')
                return self

            async def __aexit__(self, *args):
                outer.assertIs(asyncio.current_task(), self.owner)
                outer.closed.append('session')
                return await self.group.__aexit__(*args)

            async def initialize(self):
                if outer.initialize_error:
                    raise RuntimeError('initialization failed')
                if outer.initialize_wait:
                    await outer.initialize_wait.wait()

        self.stack.enter_context(patch('mcp.client.stdio.stdio_client', stdio))
        self.stack.enter_context(patch('mcp.ClientSession', lambda *args: Session()))
        self.config = ServerConfig('test', 'unused')
        self.stack.enter_context(patch.object(pool, 'find_server_config', lambda name: self.config))
        self.pool = pool.ConnectionPool()
        self.addAsyncCleanup(self.pool.stop)

    async def test_context_exit_uses_owner_task(self):
        async with self.pool.session('test'):
            pass
        await self.pool.disconnect('test')
        self.assertEqual(self.closed, ['session', 'stdio'])
        self.assertTrue(self.pool.is_empty())

    async def test_disconnect_waits_for_active_call(self):
        async with self.pool.session('test'):
            close = asyncio.create_task(self.pool.disconnect('test'))
            await asyncio.sleep(0.01)
            self.assertFalse(close.done())
            self.assertEqual(self.closed, [])
        await close
        self.assertEqual(self.closed, ['session', 'stdio'])

    async def test_concurrent_leases_share_connection(self):
        async with self.pool.session('test') as first:
            async with self.pool.session('test') as second:
                self.assertIs(first, second)
                self.assertEqual(self.pool._connections['test'].active, 2)
        self.assertEqual(self.entered, ['stdio', 'session'])

    async def test_initialize_failure_unwinds_contexts(self):
        self.initialize_error = True
        with self.assertRaises(Exception):
            async with self.pool.session('test'):
                self.fail('Must not yield a failed connection')
        self.assertEqual(self.closed, ['session', 'stdio'])
        self.assertTrue(self.pool.is_empty())

    async def test_cancelled_initialize_cleans_owner(self):
        self.initialize_wait = asyncio.Event()
        async def acquire():
            async with self.pool.session('test'):
                pass
        with patch.object(pool, 'CONNECTION_CLOSE_SECONDS', 0.01):
            task = asyncio.create_task(acquire())
            while not self.entered:
                await asyncio.sleep(0)
            task.cancel()
            with self.assertRaises(asyncio.CancelledError):
                await task
        self.assertTrue(self.pool.is_empty())
        self.assertEqual(self.closed, ['session', 'stdio'])

    async def test_config_change_replaces_connection(self):
        async with self.pool.session('test'):
            pass
        self.config.args.append('changed')
        async with self.pool.session('test'):
            self.assertEqual(self.closed, ['session', 'stdio'])
        self.assertEqual(self.entered, ['stdio', 'session', 'stdio', 'session'])

    async def test_watchdog_does_not_reclaim_active_lease(self):
        with patch.object(pool, 'SERVER_IDLE_SECONDS', -1), patch.object(pool, 'WATCHDOG_INTERVAL', 0.005):
            await self.pool.start_watchdog()
            async with self.pool.session('test'):
                await asyncio.sleep(0.02)
                self.assertEqual(self.closed, [])
            for _ in range(50):
                if self.pool.is_empty():
                    break
                await asyncio.sleep(0.005)
            self.assertTrue(self.pool.is_empty())


class RealMCPTests(unittest.IsolatedAsyncioTestCase):
    async def test_real_stdio_connect_call_disconnect_reconnect(self):
        with tempfile.TemporaryDirectory() as temp:
            script = Path(temp) / 'local_mcp.py'
            script.write_text('''from mcp.server.fastmcp import FastMCP
mcp = FastMCP("regression")
@mcp.tool()
def echo(text: str) -> str:
    return text
mcp.run(transport="stdio")
''')
            config = ServerConfig('local', sys.executable, [str(script)])
            connections = pool.ConnectionPool()
            try:
                with patch.object(pool, 'find_server_config', return_value=config):
                    for _ in range(2):
                        result = await server.handle_request(connections, {
                            'method': 'call_tool', 'server': 'local', 'tool': 'echo',
                            'params': {'text': 'verified'},
                        })
                        self.assertTrue(result['ok'], result)
                        self.assertEqual(result['result'], 'verified')
                        await connections.disconnect('local')
                        self.assertTrue(connections.is_empty())
            finally:
                await connections.stop()


if __name__ == '__main__':
    unittest.main()
