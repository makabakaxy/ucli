"""Read/write ~/.agents/ucli/servers.yaml."""

from __future__ import annotations

from pathlib import Path

import click
import yaml

from ucli.config.models import ServerConfig
from ucli.constants import DATA_DIR, SERVERS_YAML
from ucli.utils.file_ops import atomic_write_text


def load_servers_yaml() -> dict:
    if not SERVERS_YAML.exists():
        return {"servers": {}}
    try:
        data = yaml.safe_load(SERVERS_YAML.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return {"servers": {}}
        if "servers" not in data:
            data["servers"] = {}
        return data
    except yaml.YAMLError:
        return {"servers": {}}


def server_exists(server_name: str) -> bool:
    data = load_servers_yaml()
    return server_name in data.get("servers", {})


def write_server(config: ServerConfig, force: bool = False) -> bool:
    """Write server config to servers.yaml.

    Returns True on success, False if already exists without force.
    """
    data = load_servers_yaml()
    servers = data.setdefault("servers", {})

    if config.name in servers and not force:
        return True  # Not an error, just skipped

    servers[config.name] = config.to_dict()

    DATA_DIR.mkdir(parents=True, exist_ok=True, mode=0o700)
    DATA_DIR.chmod(0o700)
    atomic_write_text(
        SERVERS_YAML,
        yaml.dump(data, allow_unicode=True, default_flow_style=False, sort_keys=False),
    )
    click.echo(f"✓ servers.yaml: {config.name} added")
    return True


def remove_server(server_name: str) -> bool:
    """Remove a server from servers.yaml. Returns True if removed."""
    data = load_servers_yaml()
    servers = data.get("servers", {})

    if server_name not in servers:
        click.echo(f"Server '{server_name}' not found in servers.yaml.")
        return False

    del servers[server_name]
    atomic_write_text(
        SERVERS_YAML,
        yaml.dump(data, allow_unicode=True, default_flow_style=False, sort_keys=False),
    )
    click.echo(f"✓ servers.yaml: {server_name} removed")
    return True
