"""MCP Proxy Daemon — asyncio-based Unix socket server."""

from __future__ import annotations

import asyncio
import fcntl
import json
import logging
import os
import signal
import struct
import time
import uuid
from typing import IO

from ucli.constants import DAEMON_LOCK, DAEMON_LOG, DAEMON_PID, DAEMON_SOCK
from ucli.daemon.pool import ConnectionPool

logger = logging.getLogger("ucli.daemon")

DAEMON_IDLE_SECONDS = 300  # 5 min — exit if all servers disconnected and no requests
MAX_LIFETIME_SECONDS = 86400  # 24h — unconditional exit
CLIENT_READ_SECONDS = 5
CLIENT_CLOSE_SECONDS = 2
SHUTDOWN_SECONDS = 10


async def handle_request(pool: ConnectionPool, request: dict) -> dict:
    """Process a single IPC request and return a response dict."""
    req_id = request.get("id", str(uuid.uuid4()))
    method = request.get("method", "")

    if method == "ping":
        return {"id": req_id, "ok": True, "result": "pong"}

    if method == "call_tool":
        server = request.get("server", "")
        tool = request.get("tool", "")
        params = request.get("params", {})

        if not server:
            return _error(req_id, "SERVER_NOT_FOUND", "Missing 'server' field")
        if not tool:
            return _error(req_id, "TOOL_NOT_FOUND", "Missing 'tool' field")

        try:
            async with pool.session(server) as session:
                try:
                    result = await session.call_tool(tool, params)
                    content_parts = []
                    for item in result.content:
                        content_parts.append(item.text if hasattr(item, "text") else str(item))
                    if result.isError:
                        return _error(req_id, "TOOL_CALL_FAILED", "\n".join(content_parts))
                    return {"id": req_id, "ok": True, "result": "\n".join(content_parts)}
                except Exception as e:
                    return _error(req_id, "TOOL_CALL_FAILED", str(e))
        except ValueError as e:
            return _error(req_id, "SERVER_NOT_FOUND", str(e))
        except Exception as e:
            return _error(req_id, "SERVER_START_FAILED", str(e))

    if method == "disconnect":
        server = request.get("server", "")
        ok = await pool.disconnect(server)
        return {"id": req_id, "ok": True, "result": f"disconnected={ok}"}

    if method == "status":
        servers = pool.server_names()
        return {"id": req_id, "ok": True, "result": {"servers": servers}}

    return _error(req_id, "INTERNAL_ERROR", f"Unknown method: {method}")


def _error(req_id: str, code: str, message: str) -> dict:
    return {"id": req_id, "ok": False, "error": {"code": code, "message": message}}


async def _read_frame(reader: asyncio.StreamReader) -> bytes | None:
    """Read a length-prefixed frame. Returns None on EOF."""
    header = await reader.readexactly(4)
    length = struct.unpack(">I", header)[0]
    if length > 10 * 1024 * 1024:  # 10MB sanity limit
        return None
    return await reader.readexactly(length)


def _write_frame(data: bytes) -> bytes:
    """Create a length-prefixed frame."""
    return struct.pack(">I", len(data)) + data


async def _client_handler(
    reader: asyncio.StreamReader,
    writer: asyncio.StreamWriter,
    pool: ConnectionPool,
    activity_event: asyncio.Event,
    clients: set[asyncio.StreamWriter],
    handlers: set[asyncio.Task],
) -> None:
    """Handle a single client connection."""
    clients.add(writer)
    handlers.add(asyncio.current_task())
    try:
        raw = await asyncio.wait_for(_read_frame(reader), timeout=CLIENT_READ_SECONDS)
        if raw is None:
            return
        request = json.loads(raw.decode("utf-8"))
        activity_event.set()
        response = await handle_request(pool, request)
        frame = _write_frame(json.dumps(response, ensure_ascii=False).encode("utf-8"))
        writer.write(frame)
        await asyncio.wait_for(writer.drain(), timeout=CLIENT_CLOSE_SECONDS)
    except (asyncio.IncompleteReadError, ConnectionResetError, TimeoutError):
        pass
    except Exception as e:
        logger.exception("Client handler error: %s", e)
    finally:
        writer.close()
        try:
            await asyncio.wait_for(writer.wait_closed(), timeout=CLIENT_CLOSE_SECONDS)
        except (Exception, asyncio.CancelledError):
            pass
        finally:
            clients.discard(writer)
            handlers.discard(asyncio.current_task())


def _acquire_instance_lock() -> IO[str] | None:
    """Acquire the lifetime lock that guarantees a single daemon instance."""
    DAEMON_LOCK.parent.mkdir(parents=True, exist_ok=True)
    lock_file = DAEMON_LOCK.open("a+")
    try:
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        lock_file.close()
        return None
    return lock_file


def _cleanup_owned_runtime_files(pid: int) -> None:
    """Remove runtime files only when the PID file still belongs to this daemon."""
    try:
        owner_pid = int(DAEMON_PID.read_text().strip())
    except (FileNotFoundError, ValueError):
        return
    if owner_pid != pid:
        return
    DAEMON_PID.unlink(missing_ok=True)
    DAEMON_SOCK.unlink(missing_ok=True)


async def _close_clients(clients: set[asyncio.StreamWriter]) -> None:
    """Close every accepted client so Server.wait_closed cannot hang."""
    writers = list(clients)
    for writer in writers:
        writer.close()
    if writers:
        await asyncio.gather(
            *(asyncio.wait_for(writer.wait_closed(), timeout=CLIENT_CLOSE_SECONDS) for writer in writers),
            return_exceptions=True,
        )


async def run_daemon() -> int:
    """Main daemon entry point — runs until idle or max lifetime."""
    DAEMON_SOCK.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    DAEMON_SOCK.parent.chmod(0o700)
    logging.basicConfig(
        filename=str(DAEMON_LOG),
        level=logging.INFO,
        format="%(asctime)s %(levelname)s pid=%(process)d %(message)s",
    )

    instance_lock = _acquire_instance_lock()
    if instance_lock is None:
        logger.info("Another daemon instance owns the lock; exiting.")
        return 75

    pid = os.getpid()
    pool = ConnectionPool()
    await pool.start_watchdog()

    activity_event = asyncio.Event()
    shutdown_event = asyncio.Event()
    clients: set[asyncio.StreamWriter] = set()
    handlers: set[asyncio.Task] = set()
    start_time = time.monotonic()

    loop = asyncio.get_running_loop()
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, shutdown_event.set)

    server = None
    try:
        DAEMON_SOCK.unlink(missing_ok=True)
        # Publish ownership before bind so startup failures can clean up safely.
        DAEMON_PID.write_text(str(pid))
        server = await asyncio.start_unix_server(
            lambda r, w: _client_handler(r, w, pool, activity_event, clients, handlers),
            path=str(DAEMON_SOCK),
        )
        DAEMON_SOCK.chmod(0o600)
        logger.info("Daemon started, socket=%s", DAEMON_SOCK)
        while True:
            if shutdown_event.is_set():
                logger.info("Shutdown signal received.")
                break
            activity_event.clear()
            activity_task = asyncio.create_task(activity_event.wait())
            shutdown_task = asyncio.create_task(shutdown_event.wait())
            done, pending = await asyncio.wait(
                {activity_task, shutdown_task},
                timeout=DAEMON_IDLE_SECONDS,
                return_when=asyncio.FIRST_COMPLETED,
            )
            for task in pending:
                task.cancel()
            await asyncio.gather(*pending, return_exceptions=True)

            if shutdown_task in done:
                logger.info("Shutdown signal received.")
                break
            if not done:
                if pool.is_empty():
                    logger.info("Daemon idle with no connections, shutting down.")
                    break

            elapsed = time.monotonic() - start_time
            if elapsed > MAX_LIFETIME_SECONDS:
                logger.info("Max lifetime reached (%.0fs), shutting down.", elapsed)
                break
    finally:
        try:
            if server is not None:
                server.close()
            # Stop handlers before closing the sessions they may be using.
            tasks = list(handlers)
            for task in tasks:
                task.cancel()
            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)
            await _close_clients(clients)
            if server is not None:
                await asyncio.wait_for(server.wait_closed(), timeout=SHUTDOWN_SECONDS)
            await asyncio.wait_for(pool.stop(), timeout=SHUTDOWN_SECONDS)
        finally:
            _cleanup_owned_runtime_files(pid)
            for sig in (signal.SIGTERM, signal.SIGINT):
                loop.remove_signal_handler(sig)
            fcntl.flock(instance_lock.fileno(), fcntl.LOCK_UN)
            instance_lock.close()
            logger.info("Daemon stopped.")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(run_daemon()))
