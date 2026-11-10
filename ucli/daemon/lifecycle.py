"""Daemon lifecycle management — start, stop, health check."""

from __future__ import annotations

import fcntl
import os
import signal
import subprocess
import sys
import time
from contextlib import contextmanager

import click

from ucli.constants import DAEMON_LOCK, DAEMON_LOG, DAEMON_PID, DAEMON_SOCK
from ucli.daemon.client import ping

STOP_WAIT_SECONDS = 15
START_WAIT_SECONDS = 15


def is_daemon_running() -> bool:
    """Check process existence without treating denied access as absence."""
    try:
        pid = int(DAEMON_PID.read_text().strip())
        if pid <= 0:
            return False
        os.kill(pid, 0)
        return True
    except (FileNotFoundError, ValueError, ProcessLookupError):
        return False
    except PermissionError:
        return True


def ensure_daemon() -> bool:
    """Ensure a listener is ready, preserving the reason when access fails."""
    try:
        if ping():
            return True
        return _start_daemon()
    except PermissionError as exc:
        raise click.ClickException(
            f"Cannot access daemon at {DAEMON_SOCK}: {exc}. "
            "Run ucli in an environment allowed to access this socket and its runtime directory."
        ) from exc
    except (OSError, ConnectionError, ValueError) as exc:
        raise click.ClickException(f"Daemon at {DAEMON_SOCK} is unavailable: {exc}") from exc


@contextmanager
def _instance_guard():
    """Try the daemon lifetime lock without removing a live owner's files."""
    with DAEMON_LOCK.open("a+") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            yield False
        else:
            try:
                yield True
            finally:
                fcntl.flock(lock, fcntl.LOCK_UN)


def _start_daemon() -> bool:
    """Serialize launchers and wait for readiness using a wall-clock deadline."""
    DAEMON_SOCK.parent.mkdir(parents=True, exist_ok=True)
    deadline = time.monotonic() + START_WAIT_SECONDS
    proc = None
    # This lock is separate from the child's lifetime lock.
    with DAEMON_LOCK.with_name("daemon.start.lock").open("a+") as start_lock:
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise click.ClickException(f"Timed out waiting for another daemon launcher; see {DAEMON_LOG}")
            if ping(timeout=min(0.25, remaining)):
                return True
            try:
                fcntl.flock(start_lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except BlockingIOError:
                time.sleep(min(0.1, remaining))

        while (remaining := deadline - time.monotonic()) > 0:
            if ping(timeout=min(0.25, remaining)):
                return True
            if proc is not None:
                code = proc.poll()
                if code is not None:
                    if code != 75:
                        raise click.ClickException(
                            f"Daemon exited before becoming ready (exit {code}); see {DAEMON_LOG}"
                        )
                    proc = None  # A previous instance was still shutting down.
            if proc is None:
                with _instance_guard() as available:
                    pass
                if available:
                    with DAEMON_LOG.open("ab") as log:
                        proc = subprocess.Popen(
                            [sys.executable, "-m", "ucli.daemon.server"],
                            start_new_session=True,
                            stdin=subprocess.DEVNULL,
                            stdout=log,
                            stderr=log,
                        )
            time.sleep(min(0.1, max(0, deadline - time.monotonic())))
    detail = f"child PID {proc.pid}" if proc is not None else "another instance holds the lifetime lock"
    raise click.ClickException(
        f"Daemon was not ready within {START_WAIT_SECONDS}s ({detail}); see {DAEMON_LOG}"
    )


def stop_daemon() -> bool:
    """Stop the daemon; permission failures must never remove runtime files."""
    try:
        pid = int(DAEMON_PID.read_text().strip())
    except (FileNotFoundError, ValueError):
        return False
    if pid <= 0:
        raise click.ClickException("Invalid daemon PID")
    try:
        os.kill(pid, signal.SIGTERM)
        deadline = time.monotonic() + STOP_WAIT_SECONDS
        while time.monotonic() < deadline:
            time.sleep(0.1)
            try:
                os.kill(pid, 0)
            except ProcessLookupError:
                _cleanup_stale(pid)
                return True
        os.kill(pid, signal.SIGKILL)
        _cleanup_stale(pid)
        return True
    except ProcessLookupError:
        _cleanup_stale(pid)
        return True
    except PermissionError as exc:
        raise click.ClickException(f"Cannot stop daemon PID {pid}: {exc}") from exc


def _cleanup_stale(expected_pid: int) -> None:
    """Remove stale files only while holding the lifetime lock."""
    with _instance_guard() as available:
        if not available:
            return
        try:
            current_pid = int(DAEMON_PID.read_text().strip())
        except (FileNotFoundError, ValueError):
            return
        if current_pid == expected_pid:
            DAEMON_PID.unlink(missing_ok=True)
            DAEMON_SOCK.unlink(missing_ok=True)


def get_daemon_info() -> dict | None:
    """Return daemon information only after checking socket access."""
    try:
        if not ping():
            return None
        pid = int(DAEMON_PID.read_text().strip())
        from ucli.daemon.client import daemon_status
        status = daemon_status()
        if status is None:
            raise click.ClickException(f"Daemon status unavailable at {DAEMON_SOCK}")
    except (OSError, ConnectionError, ValueError) as exc:
        raise click.ClickException(f"Cannot query daemon at {DAEMON_SOCK}: {exc}") from exc
    return {
        "pid": pid,
        "socket": str(DAEMON_SOCK),
        "servers": status.get("result", {}).get("servers", []),
    }
