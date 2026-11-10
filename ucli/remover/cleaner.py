"""File deletion and skill directory removal with safety checks."""

from __future__ import annotations

import shutil
from pathlib import Path

import click

from ucli.constants import PROTECTED_SKILL_DIRS
from ucli.utils import safe_filename
from ucli.utils.file_ops import parse_frontmatter


def delete_file(file_path: Path) -> bool:
    """Delete a single file. Idempotent: returns True if file doesn't exist."""
    if not file_path.exists():
        return True
    try:
        file_path.unlink()
        click.echo(f"  ✓ {file_path} removed")
        return True
    except OSError as e:
        click.echo(f"  Warning: could not delete {file_path}: {e}", err=True)
        return False


def delete_dir(dir_path: Path, *, keep_protected: bool = False) -> bool:
    """Delete a directory tree. Idempotent: returns True if doesn't exist.

    If *keep_protected* is True, protected skill subdirectories are preserved
    and only the remaining contents are removed.
    """
    if not dir_path.exists():
        return True
    try:
        if keep_protected:
            for item in dir_path.iterdir():
                if item.name in PROTECTED_SKILL_DIRS:
                    continue
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()
            kept = ", ".join(f"{name}/" for name in sorted(PROTECTED_SKILL_DIRS))
            click.echo(f"  ✓ {dir_path} cleaned ({kept} kept)")
        else:
            shutil.rmtree(dir_path)
            click.echo(f"  ✓ {dir_path} removed")
        return True
    except OSError as e:
        click.echo(f"  Warning: could not delete {dir_path}: {e}", err=True)
        return False


def safe_remove_skill_dir(skill_dir: Path, expected_server_name: str) -> bool:
    """Safely remove a skill directory (copied by skill sync).

    Validates that the directory is managed by ucli before deleting.
    Preserves protected skill subdirectories unless empty.
    """
    if not skill_dir.is_dir():
        return True

    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        click.echo(f"  Warning: skipping {skill_dir} — no SKILL.md, not managed by ucli", err=True)
        return True

    name = _parse_frontmatter_name(skill_md)
    if name and safe_filename(name) != safe_filename(expected_server_name):
        click.echo(
            f"  Warning: skipping {skill_dir} — SKILL.md name '{name}' != '{expected_server_name}'",
            err=True,
        )
        return True

    # Delete managed content.
    for item in skill_dir.iterdir():
        if item.name in PROTECTED_SKILL_DIRS:
            continue
        if item.is_dir():
            shutil.rmtree(item)
        else:
            item.unlink()

    # If only empty protected directories remain, remove the whole directory.
    remaining = list(skill_dir.iterdir())
    if not remaining:
        skill_dir.rmdir()
    elif all(item.name in PROTECTED_SKILL_DIRS for item in remaining):
        if all(_protected_dir_is_empty(item) for item in remaining):
            shutil.rmtree(skill_dir)

    if skill_dir.exists():
        kept = ", ".join(f"{name}/" for name in sorted(PROTECTED_SKILL_DIRS))
        click.echo(f"  ✓ {skill_dir} cleaned ({kept} kept)")
    else:
        click.echo(f"  ✓ {skill_dir} removed")
    return True


def unsync_skills(
    server_name: str,
    skill_copies: list[Path],
    agents_skill_dir: Path | None,
) -> bool:
    """Remove all skill copy directories."""
    ok = True
    for p in skill_copies:
        if not safe_remove_skill_dir(p, server_name):
            ok = False

    if agents_skill_dir and agents_skill_dir.exists():
        if not safe_remove_skill_dir(agents_skill_dir, server_name):
            ok = False

    return ok


def _parse_frontmatter_name(skill_md: Path) -> str | None:
    """Extract 'name' from SKILL.md YAML frontmatter."""
    try:
        text = skill_md.read_text(encoding="utf-8")
    except OSError:
        return None
    fm = parse_frontmatter(text)
    return fm.get("name") if fm else None


def _protected_dir_is_empty(path: Path) -> bool:
    """Return True when a protected directory has no custom content."""
    if not path.is_dir():
        return False
    return not any(item.name != ".gitkeep" for item in path.iterdir())
