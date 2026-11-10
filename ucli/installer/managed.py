"""Install shipped presets and their local MCP runtimes without AI generation."""

from __future__ import annotations

import asyncio
from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import uuid

import click
import yaml

from ucli.constants import CLIENT_CONFIGS, CLI_DIR, DATA_DIR, PROTECTED_SKILL_DIRS, SERVERS_YAML, TOOLS_DIR
from ucli.installer.skill_sync import _copy_skill
from ucli.utils import skills_path
from ucli.utils.file_ops import atomic_write_json, atomic_write_text


def preset_root() -> Path:
    installed = Path(__file__).resolve().parents[1] / "_presets"
    return installed if installed.is_dir() else Path(__file__).resolve().parents[2] / "presets"


def shipped_presets() -> dict[str, Path]:
    result = {}
    for manifest in preset_root().glob("*/*/manifest.json"):
        data = json.loads(manifest.read_text())
        if "runtime" not in data:
            continue
        name = manifest.parent.parent.name
        current = result.get(name)
        if current is None or _version(manifest.parent.name) > _version(current.name):
            result[name] = manifest.parent
    return result


def _version(value: str) -> tuple[int, ...]:
    return tuple(int(part) for part in value.split("."))


def _name(name: str) -> str:
    if not re.fullmatch(r"[a-z][a-z0-9-]*", name):
        raise click.ClickException(f"Invalid tool name: {name}")
    return name


def record_path(name: str) -> Path:
    return DATA_DIR / "installed" / f"{_name(name)}.json"


def installed_record(name: str) -> dict | None:
    if not re.fullmatch(r"[a-z][a-z0-9-]*", name):
        return None
    path = record_path(name)
    return json.loads(path.read_text()) if path.exists() else None


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _servers() -> dict:
    try:
        data = yaml.safe_load(SERVERS_YAML.read_text()) if SERVERS_YAML.exists() else {}
    except yaml.YAMLError as exc:
        raise click.ClickException(f"Invalid YAML in {SERVERS_YAML}. Fix it before continuing.") from exc
    if data is None:
        data = {}
    if not isinstance(data, dict) or not isinstance(data.get("servers", {}), dict):
        raise click.ClickException(f"Invalid config: {SERVERS_YAML}. Fix it before installing.")
    data.setdefault("servers", {})
    return data


@contextmanager
def _lock():
    import fcntl

    DATA_DIR.mkdir(parents=True, exist_ok=True, mode=0o700)
    DATA_DIR.chmod(0o700)
    with (DATA_DIR / "install.lock").open("a+") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise click.ClickException("Another install or uninstall is running. Retry when it finishes.") from exc
        try:
            yield
        finally:
            fcntl.flock(lock, fcntl.LOCK_UN)


@contextmanager
def _transaction(paths: list[Path]):
    """Restore touched files and directories if an operation fails or is interrupted."""
    with tempfile.TemporaryDirectory(prefix="rollback-", dir=DATA_DIR) as tmp:
        backups = []
        for index, path in enumerate(dict.fromkeys(paths)):
            if path.is_symlink():
                raise click.ClickException(f"Refusing to replace a symlink: {path}")
            backup = Path(tmp) / str(index)
            exists = path.exists()
            if exists:
                if path.is_dir():
                    shutil.copytree(path, backup, symlinks=True)
                else:
                    shutil.copy2(path, backup)
            backups.append((path, backup, exists))
        try:
            yield
        except BaseException:
            for path, backup, exists in reversed(backups):
                if path.is_dir():
                    shutil.rmtree(path)
                else:
                    path.unlink(missing_ok=True)
                if exists:
                    path.parent.mkdir(parents=True, exist_ok=True)
                    if backup.is_dir():
                        shutil.copytree(backup, path, symlinks=True)
                    else:
                        shutil.copy2(backup, path)
            raise


def _disconnect(name: str) -> None:
    from ucli.daemon.client import daemon_disconnect
    from ucli.daemon.lifecycle import is_daemon_running

    if is_daemon_running() and not daemon_disconnect(name):
        raise click.ClickException("Could not disconnect the MCP backend. Wait for active commands and retry.")


def _load_preset(name: str, source: Path) -> dict:
    manifest = json.loads((source / "manifest.json").read_text())
    if manifest["server"] != name:
        raise click.ClickException("Preset server name does not match the requested tool.")
    version = manifest.get("server_version")
    if not isinstance(version, str) or not re.fullmatch(r"[0-9]+(?:\.[0-9]+)*", version):
        raise click.ClickException("Managed preset version must contain only numbers separated by dots.")
    required = {"cli.yaml", "tools.json", "skills/SKILL.md", "backend/package.json", "backend/package-lock.json"}
    checksums = manifest.get("checksums", {})
    if not required.issubset(checksums):
        raise click.ClickException("Preset is missing required files or checksums.")
    actual_files = {str(p.relative_to(source)) for p in source.rglob("*") if p.is_file() and p != source / "manifest.json"}
    if actual_files != set(checksums) or any(p.is_symlink() for p in source.rglob("*")):
        raise click.ClickException("Preset has unlisted files or symlinks.")
    for relative, expected in checksums.items():
        path = source / relative
        if not path.resolve().is_relative_to(source.resolve()) or path.is_symlink():
            raise click.ClickException(f"Invalid preset path: {relative}")
        if not path.is_file() or _digest(path) != expected:
            raise click.ClickException(f"Preset checksum failed: {relative}")
    from ucli.cli.mapping import extract_tools_from_yaml

    mapping = yaml.safe_load((source / "cli.yaml").read_text())
    tools = json.loads((source / "tools.json").read_text())
    names = {tool["name"] for tool in tools["tools"]}
    if mapping.get("server") != name or tools.get("server") != name or extract_tools_from_yaml(mapping) != names:
        raise click.ClickException("Preset CLI mapping does not match its tool schema.")
    runtime = manifest["runtime"]
    entrypoint = Path(runtime["entrypoint"])
    if entrypoint.is_absolute() or ".." in entrypoint.parts:
        raise click.ClickException("Invalid backend entrypoint.")
    package = json.loads((source / "backend/package.json").read_text())
    lock = json.loads((source / "backend/package-lock.json").read_text())
    expected = {runtime["package"]: manifest["server_version"]}
    if package.get("dependencies") != expected or lock["packages"][""]["dependencies"] != expected:
        raise click.ClickException("Backend dependencies do not match the preset version.")
    return manifest


def _node(runtime: dict) -> tuple[str, str, str]:
    node, npm = shutil.which("node"), shutil.which("npm")
    if not node or not npm:
        raise click.ClickException("Node.js and npm are required. Install Node.js 24, then run this command again.")
    info = json.loads(subprocess.check_output([node, "-p", "JSON.stringify(process.versions)"], text=True))
    if int(info["node"].split(".")[0]) not in runtime["node_majors"]:
        raise click.ClickException(f"Node.js {info['node']} is unsupported by this preset. Use Node.js 24.")
    return str(Path(node).resolve()), str(Path(npm).absolute()), info["modules"]


async def _probe(config: dict, tools: dict, health: dict, *, ready: bool) -> tuple[bool, str]:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    params = StdioServerParameters(command=config["command"], args=config["args"], env={**os.environ, **config.get("env", {})})
    async with asyncio.timeout(90):
        async with stdio_client(params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                found = set()
                cursor = None
                while True:
                    result = await session.list_tools(cursor=cursor)
                    found.update(tool.name for tool in result.tools)
                    cursor = result.nextCursor
                    if not cursor:
                        break
                expected = {tool["name"] for tool in tools["tools"]}
                if expected - found:
                    raise click.ClickException(f"Backend is missing tools: {', '.join(sorted(expected - found))}")
                if not ready:
                    return True, f"MCP ready ({len(found)} tools)."
                result = await session.call_tool(health["tool"], {})
                message = "\n".join(item.text for item in result.content if hasattr(item, "text"))
                ok = not result.isError and health["success_text"] in message
                return ok, message


def _check_backend(config: dict, tools: dict, health: dict, *, ready: bool) -> tuple[bool, str]:
    try:
        return asyncio.run(_probe(config, tools, health, ready=ready))
    except Exception as exc:
        def describe(error: BaseException) -> str:
            if isinstance(error, BaseExceptionGroup):
                return "; ".join(describe(child) for child in error.exceptions)
            return str(error) or type(error).__name__

        raise click.ClickException(f"Backend check failed: {describe(exc)}") from exc


def _managed_files(roots: list[Path]) -> dict[str, str]:
    files = {}
    for root in roots:
        if root.is_file():
            files[str(root)] = _digest(root)
        elif root.is_dir():
            for path in root.rglob("*"):
                if path.is_file() and path.relative_to(root).parts[0] not in PROTECTED_SKILL_DIRS:
                    files[str(path)] = _digest(path)
    return files


def _has_managed_content(path: Path) -> bool:
    if path.is_symlink() or path.is_file():
        return True
    return bool(_managed_files([path]))


def install_preset(name: str, source: Path, *, clients: list[str] | None = None,
                   env: dict[str, str] | None = None, force: bool = False) -> None:
    """Install a versioned backend and commit config and skill files together."""
    _name(name)
    manifest = _load_preset(name, source)
    if sys.platform not in manifest["runtime"]["platforms"]:
        raise click.ClickException("This shipped preset currently supports macOS only.")
    with _lock():
        previous = installed_record(name)
        clients = clients if clients is not None else (previous["clients"] if previous else ["codex"])
        if not clients or set(clients) - CLIENT_CONFIGS.keys():
            raise click.ClickException("Choose clients from codex, claude, cursor.")
        # Keep existing destinations managed when adding another client.
        clients = sorted(set(clients) | set(previous["clients"] if previous else []))
        destinations = sorted({CLIENT_CONFIGS[c]["skill_dir"] / name for c in clients})
        roots = [CLI_DIR / f"{name}.yaml", TOOLS_DIR / f"{name}.json", skills_path(name), *destinations]
        data = _servers()
        existing = data["servers"].get(name)
        if not force:
            if previous:
                changed = [p for p, digest in previous["files"].items() if Path(p).exists() and _digest(Path(p)) != digest]
                if existing != previous["config"] or changed:
                    raise click.ClickException("Managed files or config were edited. Back them up and use --force to replace them.")
                for target in destinations:
                    if str(target) not in previous["skill_dirs"] and _has_managed_content(target):
                        raise click.ClickException(f"Skill already exists: {target}. Use --force to replace it.")
            elif existing is not None or any(_has_managed_content(p) for p in roots):
                raise click.ClickException(f"{name} already exists outside this installer. Use --force to adopt it; user notes are kept.")
        node, npm, abi = _node(manifest["runtime"])
        lock_hash = manifest["checksums"]["backend/package-lock.json"]
        runtime = Path(previous["runtime_dir"]) if previous else None
        reuse = bool(previous and previous["lock_hash"] == lock_hash and previous["node_abi"] == abi
                     and runtime and (runtime / manifest["runtime"]["entrypoint"]).is_file())
        new_runtime = None
        try:
            if not reuse:
                runtime = DATA_DIR / "packages" / name / f"{manifest['server_version']}-{uuid.uuid4().hex[:12]}"
                runtime.mkdir(parents=True)
                new_runtime = runtime
                for filename in ("package.json", "package-lock.json"):
                    shutil.copy2(source / "backend" / filename, runtime / filename)
                click.echo(f"Installing {manifest['runtime']['package']}@{manifest['server_version']}...")
                subprocess.run([npm, "ci", "--no-audit", "--no-fund"], cwd=runtime, check=True, timeout=600,
                               env={**os.environ, "PATH": str(Path(node).parent) + os.pathsep + os.environ.get("PATH", "")})
            assert runtime is not None
            config = {"command": node, "args": [str(runtime / manifest["runtime"]["entrypoint"])],
                      "env": {**manifest["runtime"].get("env", {}), **(existing.get("env", {}) if isinstance(existing, dict) else {}), **(env or {})}}
            tools = json.loads((source / "tools.json").read_text())
            click.echo("Checking MCP startup and tool coverage...")
            _check_backend(config, tools, manifest["health"], ready=False)
            _disconnect(name)
            data = _servers()
            if data["servers"].get(name) != existing:
                raise click.ClickException("The tool config changed during installation. Retry with the current config.")
            with _transaction([*roots, SERVERS_YAML, record_path(name)]):
                for filename, target in (("cli.yaml", roots[0]), ("tools.json", roots[1])):
                    target.parent.mkdir(parents=True, exist_ok=True)
                    atomic_write_text(target, (source / filename).read_text())
                _copy_skill(source / "skills", skills_path(name))
                for target in destinations:
                    _copy_skill(skills_path(name), target)
                data["servers"][name] = config
                atomic_write_text(SERVERS_YAML, yaml.safe_dump(data, sort_keys=False))
                record_path(name).parent.mkdir(parents=True, exist_ok=True)
                atomic_write_json(record_path(name), {
                    "version": manifest["server_version"], "clients": clients, "config": config,
                    "runtime_dir": str(runtime), "lock_hash": lock_hash, "node_abi": abi,
                    "health": manifest["health"], "files": _managed_files(roots),
                    "skill_dirs": [str(skills_path(name)), *map(str, destinations)],
                })
        except BaseException:
            if new_runtime:
                shutil.rmtree(new_runtime, ignore_errors=True)
            raise
        if previous and Path(previous["runtime_dir"]) != runtime:
            _delete_runtime(name, Path(previous["runtime_dir"]))
    click.echo(f"Installed {name} {manifest['server_version']} for {', '.join(clients)}.")
    click.echo("Client MCP configuration was not changed.")
    if not doctor(name):
        click.echo(f"Installation is complete; Photoshop is not ready. Resolve the issue above and run `ucli doctor {name}`.")


def doctor(name: str) -> bool:
    record = installed_record(name)
    if not record:
        raise click.ClickException(f"{name} is not installed by ucli install. Run `ucli install {name}` first.")
    problems = [p for p, digest in record["files"].items() if not Path(p).is_file() or _digest(Path(p)) != digest]
    if problems or _servers()["servers"].get(name) != record["config"]:
        click.echo("Installation files or config have changed. Run install again (use --force to replace edits).", err=True)
        return False
    try:
        tools = json.loads((TOOLS_DIR / f"{name}.json").read_text())
        ok, message = _check_backend(record["config"], tools, record["health"], ready=True)
    except Exception as exc:
        click.echo(f"Not ready: {exc}", err=True)
        return False
    click.echo(("Ready: " if ok else "Not ready: ") + message)
    return ok


def _delete_runtime(name: str, path: Path) -> None:
    parent = (DATA_DIR / "packages" / name).resolve()
    if path.resolve().parent != parent or path.is_symlink():
        raise click.ClickException(f"Invalid runtime path: {path}")
    shutil.rmtree(path, ignore_errors=True)


def uninstall(name: str, *, force: bool = False, dry_run: bool = False, keep_config: bool = False) -> None:
    with _lock():
        record = installed_record(name)
        if not record:
            raise click.ClickException(f"No installation record for {name}.")
        data = _servers()
        if not keep_config and data["servers"].get(name) not in (None, record["config"]):
            raise click.ClickException("Config was edited. Use --keep-config to preserve it.")
        click.echo(f"Remove {name} {record['version']}; keep user notes and modified files.")
        if dry_run:
            return
        if not force and not click.confirm("Proceed?", default=True):
            return
        _disconnect(name)
        paths = [Path(p) for p in record["files"]]
        with _transaction([*paths, SERVERS_YAML, record_path(name)]):
            for path in paths:
                if path.is_file() and _digest(path) == record["files"][str(path)]:
                    path.unlink()
                elif path.exists():
                    click.echo(f"Kept modified file: {path}")
            if not keep_config:
                data["servers"].pop(name, None)
                atomic_write_text(SERVERS_YAML, yaml.safe_dump(data, sort_keys=False))
            record_path(name).unlink()
        if not keep_config:
            _delete_runtime(name, Path(record["runtime_dir"]))
        click.echo(f"Uninstalled {name}.")
