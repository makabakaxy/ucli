"""IPC client for communicating with the MCP Proxy Daemon."""

from __future__ import annotations

import json
import math
import os
import socket
import struct
import time
import uuid

from ucli.constants import DAEMON_SOCK

DEFAULT_TIMEOUT = 60
PING_TIMEOUT = 3


def _send_request(request: dict, timeout: float = DEFAULT_TIMEOUT) -> dict:
    """Send a request to the daemon and return the response."""
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    deadline = time.monotonic() + timeout
    sock.settimeout(timeout)
    try:
        sock.connect(str(DAEMON_SOCK))
        data = json.dumps(request, ensure_ascii=False).encode("utf-8")
        frame = struct.pack(">I", len(data)) + data
        sock.settimeout(max(0.001, deadline - time.monotonic()))
        sock.sendall(frame)

        # Read response
        header = _recv_exact(sock, 4, deadline)
        length = struct.unpack(">I", header)[0]
        if length > 10 * 1024 * 1024:
            raise ValueError("Daemon response exceeds 10 MiB")
        body = _recv_exact(sock, length, deadline)
        return json.loads(body.decode("utf-8"))
    finally:
        sock.close()


def _recv_exact(sock: socket.socket, n: int, deadline: float) -> bytes:
    """Receive exactly n bytes from socket."""
    buf = b""
    while len(buf) < n:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError("Daemon response timed out")
        sock.settimeout(remaining)
        chunk = sock.recv(n - len(buf))
        if not chunk:
            raise ConnectionError("Daemon connection closed unexpectedly")
        buf += chunk
    return buf


def call_tool(
    server: str,
    tool: str,
    params: dict | None = None,
    timeout: float | None = None,
) -> dict:
    """Call an MCP tool through the daemon.

    Returns the full response dict: {"id": ..., "ok": bool, "result": ..., "error": ...}
    """
    if timeout is None:
        from ucli.config.tool_store import load_tools

        tools = load_tools(server)
        default = (tools.server_meta or {}).get("timeout", DEFAULT_TIMEOUT) if tools else DEFAULT_TIMEOUT
        timeout = float(os.environ.get("UCLI_TIMEOUT", default))
    if not math.isfinite(timeout) or timeout <= 0:
        raise ValueError("Request timeout must be a positive finite number")
    request = {
        "id": str(uuid.uuid4()),
        "method": "call_tool",
        "server": server,
        "tool": tool,
        "params": params or {},
    }
    return _send_request(request, timeout=timeout)


def ping(timeout: float = PING_TIMEOUT) -> bool:
    """Return False only when no listener exists; preserve access and health errors."""
    try:
        resp = _send_request(
            {"id": str(uuid.uuid4()), "method": "ping"}, timeout=timeout,
        )
    except (FileNotFoundError, ConnectionRefusedError):
        return False
    if resp.get("ok") is not True or resp.get("result") != "pong":
        raise ValueError("Invalid daemon ping response")
    return True


def daemon_status() -> dict | None:
    """Query daemon status. Returns response dict or None if not running."""
    try:
        return _send_request(
            {"id": str(uuid.uuid4()), "method": "status"},
            timeout=PING_TIMEOUT,
        )
    except (OSError, ConnectionError, TimeoutError):
        return None


def daemon_disconnect(server_name: str) -> bool:
    """Ask the daemon to disconnect a server. Returns True on success."""
    try:
        resp = _send_request(
            {"id": str(uuid.uuid4()), "method": "disconnect", "server": server_name},
            timeout=PING_TIMEOUT,
        )
        return resp.get("ok", False)
    except (OSError, ConnectionError, TimeoutError):
        return False
