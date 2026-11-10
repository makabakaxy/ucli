"""Update pipeline — scan, diff, regenerate as needed."""

from __future__ import annotations

import click

from ucli.cli.mapping import cli_path
from ucli.config.reader import find_server_config
from ucli.config.tool_store import load_tools, save_tools
from ucli.installer.servers_writer import server_exists
from ucli.scanner import scan_server
from ucli.updater.diff import ToolsDiff, compute_diff


def update_server(
    server_name: str,
    yes: bool = False,
    dry_run: bool = False,
) -> bool:
    """Run the update pipeline for a single server.

    Returns True on success or up-to-date.
    """
    from ucli.installer.managed import installed_record, install_preset, shipped_presets

    record = installed_record(server_name)
    if record:
        source = shipped_presets().get(server_name)
        if source is None:
            raise click.ClickException(f"No shipped preset for {server_name} in this ucli version.")
        click.echo(f"{server_name}: installed {record['version']}, shipped {source.name}")
        if dry_run:
            click.echo("[DRY RUN] No files were modified.")
            return True
        if not yes and not click.confirm("Install the shipped preset?", default=True):
            return True
        install_preset(server_name, source)
        return True

    # Precondition checks
    old_tools = load_tools(server_name)
    if old_tools is None:
        click.echo(
            f"Error: {server_name} has not been scanned. "
            f"Run 'ucli mcp add {server_name}' or 'ucli mcp install {server_name}' first.",
            err=True,
        )
        return False

    if not server_exists(server_name) and find_server_config(server_name) is None:
        click.echo(
            f"Error: {server_name} is not registered. "
            f"Run 'ucli mcp add' or 'ucli mcp install' first.",
            err=True,
        )
        return False

    # Re-scan
    click.echo(f"Scanning {server_name}...")
    new_tools_json = scan_server(server_name)
    if new_tools_json is None:
        click.echo(f"Error: failed to scan {server_name}.", err=True)
        return False

    # Compute diff
    diff = compute_diff(old_tools, new_tools_json)

    if not diff.has_any_change:
        click.echo(
            f"{server_name} is up-to-date "
            f"(version {old_tools.version}, {len(old_tools.tools)} tools). Nothing to do."
        )
        return True

    # Display changes
    click.echo("\nChanges detected:")
    for line in diff.summary_lines():
        click.echo(f"  {line}")

    if dry_run:
        click.echo("\n[DRY RUN] No files were modified.")
        return True

    if not yes:
        if not click.confirm("\nContinue?", default=True):
            click.echo("Aborted.")
            return True

    # Write new tools JSON (already done by scan_server, but we ensure it)
    save_tools(new_tools_json)
    click.echo(f"✓ tools/{server_name}.json updated")

    # Regenerate CLI tree if needed
    if diff.needs_cli_regen:
        from ucli.generator.cli_gen import generate_cli

        cp = cli_path(server_name)
        merge = cp.exists()
        click.echo(f"Regenerating CLI tree ({'merge' if merge else 'full'})...")
        ok = generate_cli(server_name, merge=merge)
        if not ok:
            click.echo("Warning: CLI tree regeneration failed.", err=True)

    # Regenerate skill (incremental via source_cli_hash)
    from ucli.generator.skill_gen import generate_skill

    skill_ok = generate_skill(server_name)

    # Skill sync if skill was updated
    if skill_ok:
        from ucli.installer.skill_sync import skill_sync
        skill_sync(server_name, skip_disable=True)

    # Summary
    version_str = ""
    if diff.version_changed:
        version_str = f" {diff.old_version} -> {diff.new_version}"
    click.echo(f"\nDone! {server_name} updated.{version_str}")
    return True


def update_all(yes: bool = False, dry_run: bool = False) -> bool:
    """Update all registered servers.

    Returns True if all succeeded.
    """
    from ucli.config.reader import iter_servers_yaml
    from ucli.constants import TOOLS_DIR

    servers: list[str] = []
    for name, _ in iter_servers_yaml():
        tp = TOOLS_DIR / f"{name}.json"
        if tp.exists():
            servers.append(name)

    if not servers:
        click.echo("No servers to update.")
        return True

    click.echo(f"Scanning {len(servers)} servers...")

    # Collect diffs
    needs_update: list[tuple[str, ToolsDiff]] = []
    errors: list[str] = []

    from ucli.installer.managed import installed_record

    for name in servers:
        if installed_record(name):
            try:
                if not update_server(name, yes=yes, dry_run=dry_run):
                    errors.append(name)
            except Exception as exc:
                click.echo(f"  {name}: {exc}", err=True)
                errors.append(name)
            continue
        old_tools = load_tools(name)
        if old_tools is None:
            continue
        try:
            new_tools = scan_server(name)
            if new_tools is None:
                errors.append(name)
                continue
            diff = compute_diff(old_tools, new_tools)
            if diff.has_any_change:
                needs_update.append((name, diff))
            else:
                click.echo(f"  {name:<25} up-to-date")
        except Exception as e:
            click.echo(f"  {name:<25} error: {e}", err=True)
            errors.append(name)

    for name, diff in needs_update:
        changes = []
        if diff.added_tools:
            changes.append(f"+{len(diff.added_tools)} tools")
        if diff.removed_tools:
            changes.append(f"-{len(diff.removed_tools)} tools")
        if diff.version_changed:
            changes.append(f"{diff.old_version} -> {diff.new_version}")
        click.echo(f"  {name:<25} needs update ({', '.join(changes)})")

    summary = f"\n{len(servers)} servers scanned, {len(needs_update)} need update"
    if errors:
        summary += f", {len(errors)} errors"
    click.echo(summary)

    if not needs_update:
        return not errors

    if dry_run:
        click.echo("[DRY RUN] No files were modified.")
        return True

    if not yes:
        if not click.confirm(f"\nUpdate {len(needs_update)} servers?", default=True):
            click.echo("Aborted.")
            return True

    # Execute updates sequentially
    success_count = 0
    for i, (name, _) in enumerate(needs_update, 1):
        click.echo(f"\n[{i}/{len(needs_update)}] Updating {name}...")
        ok = update_server(name, yes=True)
        if ok:
            success_count += 1

    click.echo(f"\nDone! {success_count}/{len(needs_update)} servers updated.")
    return success_count == len(needs_update) and not errors
