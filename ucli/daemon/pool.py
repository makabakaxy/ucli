"""MCP connections owned by dedicated tasks, with idle reclamation."""

from __future__ import annotations

import asyncio
import hashlib
import json
import logging
import os
import time
from contextlib import asynccontextmanager
from dataclasses import dataclass, field

from ucli.config.models import ServerConfig
from ucli.config.reader import find_server_config

logger = logging.getLogger("ucli.daemon")

SERVER_IDLE_SECONDS = 600
WATCHDOG_INTERVAL = 30
CONNECTION_CLOSE_SECONDS = 5
CONNECTION_START_SECONDS = 60


def _config_hash(config: ServerConfig) -> str:
    payload = json.dumps(
        {"command": config.command, "args": config.args, "env": config.env},
        sort_keys=True,
    )
    return hashlib.sha256(payload.encode()).hexdigest()


@dataclass
class ServerConnection:
    server_name: str
    config_hash: str
    ready: asyncio.Future
    close: asyncio.Event = field(default_factory=asyncio.Event)
    idle: asyncio.Event = field(default_factory=asyncio.Event)
    task: asyncio.Task | None = None
    active: int = 0
    last_used: float = field(default_factory=time.monotonic)

    def idle_seconds(self) -> float:
        return time.monotonic() - self.last_used


class ConnectionPool:
    """Keep MCP context entry and exit in the same owner task."""

    def __init__(self) -> None:
        self._connections: dict[str, ServerConnection] = {}
        self._locks: dict[str, asyncio.Lock] = {}
        self._watchdog_task: asyncio.Task | None = None
        self._stopping = False

    async def start_watchdog(self) -> None:
        self._watchdog_task = asyncio.create_task(self._watchdog_loop())

    async def stop(self) -> None:
        self._stopping = True
        if self._watchdog_task:
            self._watchdog_task.cancel()
            await asyncio.gather(self._watchdog_task, return_exceptions=True)
        await asyncio.gather(*(self.disconnect(name) for name in list(self._connections)))

    @asynccontextmanager
    async def session(self, server_name: str):
        """Lease a session so disconnect and idle reclaim cannot interrupt calls."""
        lock = self._locks.setdefault(server_name, asyncio.Lock())
        async with lock:
            if self._stopping:
                raise RuntimeError("Connection pool is stopping")
            config = find_server_config(server_name)
            if config is None:
                raise ValueError(f"Server '{server_name}' is not configured")
            conn = self._connections.get(server_name)
            if conn and (conn.task.done() or conn.config_hash != _config_hash(config)):
                await self._close_server(server_name)
                conn = None
            if conn is None:
                conn = ServerConnection(
                    server_name, _config_hash(config), asyncio.get_running_loop().create_future(),
                )
                conn.idle.set()
                self._connections[server_name] = conn
                conn.task = asyncio.create_task(self._own_connection(conn, config))
                try:
                    await asyncio.wait_for(asyncio.shield(conn.ready), CONNECTION_START_SECONDS)
                except BaseException:
                    await self._close_server(server_name)
                    # Retrieve a concurrent initialization error, if any.
                    if conn.ready.done() and not conn.ready.cancelled():
                        conn.ready.exception()
                    raise
            session = conn.ready.result()
            conn.active += 1
            conn.idle.clear()
        try:
            yield session
        finally:
            conn.active -= 1
            conn.last_used = time.monotonic()
            if not conn.active:
                conn.idle.set()

    async def _own_connection(self, conn: ServerConnection, config: ServerConfig) -> None:
        try:
            from mcp import ClientSession, StdioServerParameters
            from mcp.client.stdio import stdio_client

            params = StdioServerParameters(
                command=config.command, args=config.args,
                env={**os.environ, **config.env} if config.env else None,
            )
            async with stdio_client(params) as (read_stream, write_stream):
                async with ClientSession(read_stream, write_stream) as session:
                    await session.initialize()
                    conn.ready.set_result(session)
                    logger.info("Connected to %s", conn.server_name)
                    await conn.close.wait()
        except asyncio.CancelledError:
            if not conn.ready.done():
                conn.ready.cancel()
            raise
        except Exception as exc:
            if not conn.ready.done():
                conn.ready.set_exception(exc)
            else:
                logger.exception("Connection failed for %s", conn.server_name)
        finally:
            logger.info("Connection owner finished for %s", conn.server_name)

    async def disconnect(self, server_name: str) -> bool:
        lock = self._locks.setdefault(server_name, asyncio.Lock())
        async with lock:
            if server_name not in self._connections:
                return False
            await self._close_server(server_name)
            return True

    def is_empty(self) -> bool:
        return not self._connections

    def server_names(self) -> list[str]:
        return list(self._connections)

    async def _close_server(self, server_name: str) -> None:
        """Called under the server lock; lease releases never need that lock."""
        conn = self._connections.get(server_name)
        if conn is None:
            return
        await conn.idle.wait()
        conn.close.set()
        try:
            await asyncio.wait_for(asyncio.shield(conn.task), CONNECTION_CLOSE_SECONDS)
        except TimeoutError:
            logger.warning("Cancelling slow connection owner for %s", server_name)
            conn.task.cancel()
            await asyncio.gather(conn.task, return_exceptions=True)
        except asyncio.CancelledError:
            conn.task.cancel()
            await asyncio.gather(conn.task, return_exceptions=True)
            raise
        finally:
            if conn.task.done():
                self._connections.pop(server_name, None)

    async def _watchdog_loop(self) -> None:
        while True:
            await asyncio.sleep(WATCHDOG_INTERVAL)
            for name in list(self._connections):
                lock = self._locks.setdefault(name, asyncio.Lock())
                async with lock:
                    conn = self._connections.get(name)
                    if conn and not conn.active and conn.idle_seconds() > SERVER_IDLE_SECONDS:
                        logger.info("Idle reclaim: %s (%.0fs idle)", name, conn.idle_seconds())
                        await self._close_server(name)
