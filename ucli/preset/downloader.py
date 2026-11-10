"""Download preset files from remote repository."""

from __future__ import annotations

import json
import re
import shutil
import tempfile
from pathlib import Path
from urllib.request import urlopen
from urllib.error import URLError

import click

from ucli.constants import CLI_DIR, DATA_DIR, PROTECTED_SKILL_DIRS, TOOLS_DIR
from ucli.preset.models import Manifest
from ucli.preset.registry import _raw_base, find_preset
from ucli.utils import safe_filename, skills_path
from ucli.utils.file_ops import ensure_users_dir

FILE_TIMEOUT = 10


def pull_preset(
    server_name: str,
    version: str | None = None,
    force: bool = False,
    dry_run: bool = False,
) -> bool:
    """Download all preset files for a server.

    Args:
        server_name: MCP server name.
        version: Specific version to pull, or None for latest.
        force: Overwrite existing files without prompting.
        dry_run: Preview what would be downloaded without writing files.

    Returns True on success.
    """
    raw_base = _raw_base()
    safe_name = safe_filename(server_name)

    # Resolve version from index
    entry = find_preset(server_name)
    if entry is None:
        click.echo(f"Error: no preset found for '{server_name}'.", err=True)
        return False

    try:
        resolved_version = entry.resolve_version(version)
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        return False

    if dry_run:
        click.echo(f"[DRY RUN] Would download preset for {server_name}:")
        click.echo(f"  Version: {resolved_version}")
        click.echo(f"  Available versions: {', '.join(entry.versions)}")
        return True

    # Fetch manifest
    manifest_url = f"{raw_base}/{safe_name}/{resolved_version}/manifest.json"
    manifest_data = _download_json(manifest_url)
    if manifest_data is None:
        click.echo(f"Error: could not download manifest for {server_name}@{resolved_version}.", err=True)
        return False

    try:
        manifest = Manifest.from_dict(manifest_data)
        targets = _validate_files(server_name, manifest.files)
    except (KeyError, TypeError, ValueError) as e:
        click.echo(f"Error: invalid preset manifest: {e}", err=True)
        return False
    base_url = f"{raw_base}/{safe_name}/{resolved_version}"

    click.echo(f"Downloading preset for {server_name}...")
    click.echo(
        f"  Preset: v{resolved_version}, "
        f"{manifest.tool_count} tools, "
        f"generated {manifest.generated_at[:10]}"
    )

    # Check existing files
    if not force:
        existing = _check_existing(server_name, manifest.files)
        if existing:
            click.echo(f"\n  Local files already exist for {server_name}:")
            for f in existing[:5]:
                click.echo(f"    {f}")
            if not click.confirm("  Overwrite with preset?", default=True):
                return False

    # Finish all downloads before replacing any existing files.
    with tempfile.TemporaryDirectory(prefix="ucli-preset-") as tmp:
        staged = []
        for index, (rel_path, target) in enumerate(targets):
            if _preserve_user_file(rel_path, target):
                continue
            source = Path(tmp) / str(index)
            if not download_file(f"{base_url}/{rel_path}", source):
                click.echo(f"  Error: failed to download {rel_path}", err=True)
                return False
            staged.append((rel_path, source))
        for rel_path, source in staged:
            target = _map_target_path(server_name, rel_path)
            _copy_file(source, target)
            click.echo(f"  ✓ {rel_path}")

    ensure_users_dir(skills_path(server_name))

    click.echo(f"Done! Files written to {DATA_DIR}/")
    return True


def download_file(url: str, target_path: Path) -> bool:
    """Download a single file to target path (atomic write)."""
    try:
        with urlopen(url, timeout=FILE_TIMEOUT) as resp:
            if resp.status != 200:
                return False
            content = resp.read()
    except (URLError, OSError):
        return False

    target_path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=target_path.parent, suffix=".tmp")
    try:
        with open(fd, "wb") as f:
            f.write(content)
        Path(tmp).replace(target_path)
        return True
    except Exception:
        Path(tmp).unlink(missing_ok=True)
        return False


def _download_json(url: str) -> dict | None:
    try:
        with urlopen(url, timeout=FILE_TIMEOUT) as resp:
            if resp.status != 200:
                return None
            return json.loads(resp.read().decode("utf-8"))
    except (URLError, OSError, json.JSONDecodeError):
        return None


def _map_target_path(server_name: str, rel_path: str) -> Path:
    """Map only supported paths, confined to this server's own files."""
    name = safe_filename(server_name)
    if not re.fullmatch(r"[A-Za-z0-9_@][A-Za-z0-9._@-]*", name):
        raise ValueError("Invalid preset server name")
    if not isinstance(rel_path, str) or "\\" in rel_path or "\x00" in rel_path:
        raise ValueError("Invalid preset file path")
    parts = rel_path.split("/")
    if any(part in {"", ".", ".."} for part in parts):
        raise ValueError(f"Invalid preset file path: {rel_path}")
    if rel_path == "tools.json":
        target = TOOLS_DIR / f"{name}.json"
        root = TOOLS_DIR
    elif rel_path == "cli.yaml":
        target = CLI_DIR / f"{name}.yaml"
        root = CLI_DIR
    elif len(parts) > 1 and parts[0] == "skills":
        root = skills_path(server_name)
        target = root.joinpath(*parts[1:])
    else:
        raise ValueError(f"Unsupported preset file: {rel_path}")

    if not target.resolve().is_relative_to(root.resolve()):
        raise ValueError(f"Path traversal detected in preset manifest: {rel_path}")
    for path in (target, *target.parents):
        if path == DATA_DIR:
            break
        if path.is_symlink():
            raise ValueError(f"Symlink in preset destination: {rel_path}")
    return target


def _validate_files(server_name: str, files: list[str]) -> list[tuple[str, Path]]:
    if not isinstance(files, list) or not files:
        raise ValueError("Preset files must be a nonempty list")
    targets = [(relative, _map_target_path(server_name, relative)) for relative in files]
    if len({path for _, path in targets}) != len(targets):
        raise ValueError("Duplicate preset destination")
    return targets


def _preserve_user_file(relative: str, target: Path) -> bool:
    parts = relative.split("/")
    return len(parts) > 2 and parts[0] == "skills" and parts[1] in PROTECTED_SKILL_DIRS and target.exists()


def _copy_file(source: Path, target: Path) -> None:
    """Replace a validated destination without following a final symlink."""
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(dir=target.parent, suffix=".tmp")
    try:
        with open(fd, "wb") as output, source.open("rb") as incoming:
            shutil.copyfileobj(incoming, output)
        Path(temporary).replace(target)
    finally:
        Path(temporary).unlink(missing_ok=True)


def install_from_local_dir(
    server_name: str,
    version_dir: Path,
    force: bool = False,
) -> bool:
    """Install preset files from a local version directory.

    version_dir must contain manifest.json, tools.json, cli.yaml, and skills/.

    Returns True on success.
    """
    manifest_path = version_dir / "manifest.json"
    if not manifest_path.exists():
        click.echo(f"Error: no manifest.json found in {version_dir}", err=True)
        return False

    try:
        manifest_data = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest = Manifest.from_dict(manifest_data)
        targets = _validate_files(server_name, manifest.files)
        for rel_path, _ in targets:
            source = version_dir / rel_path
            if not source.resolve().is_relative_to(version_dir.resolve()) or not source.is_file():
                raise ValueError(f"Invalid or missing preset source: {rel_path}")
    except Exception as e:
        click.echo(f"Error: could not read manifest.json: {e}", err=True)
        return False

    click.echo(f"Installing from local preset: {version_dir}")
    click.echo(
        f"  {manifest.tool_count} tools, "
        f"generated {manifest.generated_at[:10]}"
    )

    if not force:
        existing = _check_existing(server_name, manifest.files)
        if existing:
            click.echo(f"\n  Local files already exist for {server_name}:")
            for f in existing[:5]:
                click.echo(f"    {f}")
            if not click.confirm("  Overwrite with local preset?", default=True):
                return False

    for rel_path, _ in targets:
        src = version_dir / rel_path
        try:
            target = _map_target_path(server_name, rel_path)
        except ValueError as e:
            click.echo(f"  Error: {e}", err=True)
            return False

        if _preserve_user_file(rel_path, target):
            continue
        _copy_file(src, target)
        click.echo(f"  ✓ {rel_path}")

    ensure_users_dir(skills_path(server_name))
    click.echo(f"Done! Files written to {DATA_DIR}/")
    return True


def _check_existing(server_name: str, files: list[str]) -> list[Path]:
    """Check which preset files already exist locally."""
    existing: list[Path] = []
    for rel_path in files:
        target = _map_target_path(server_name, rel_path)
        if target.exists():
            existing.append(target)
    return existing
