"""ucli CLI entry point."""

from __future__ import annotations

from pathlib import Path

import click


class DynamicRootGroup(click.Group):
    """Fall back to dynamic command resolution for unknown top-level tokens."""

    def invoke(self, ctx):
        protected_args = list(getattr(ctx, "_protected_args", ()))
        if not protected_args:
            return super().invoke(ctx)

        args = [*protected_args, *ctx.args]
        cmd_name = click.utils.make_str(args[0])
        cmd = self.get_command(ctx, cmd_name)

        if cmd is None and ctx.token_normalize_func is not None:
            cmd_name = ctx.token_normalize_func(cmd_name)
            cmd = self.get_command(ctx, cmd_name)

        if cmd is None and not args[0].startswith("-"):
            ctx._protected_args = []
            ctx.args = args
            ctx.invoked_subcommand = None
            with ctx:
                return click.Command.invoke(self, ctx)

        return super().invoke(ctx)


@click.group(cls=DynamicRootGroup, invoke_without_command=True)
@click.version_option(package_name="ucli-tools")
@click.pass_context
def cli(ctx):
    """ucli - Build hierarchical CLI commands for MCP servers and local helpers."""
    if ctx.invoked_subcommand is None:
        # Unknown top-level commands are handled dynamically by DynamicRootGroup.
        args = list(ctx.args)
        if args and not args[0].startswith("-"):
            _handle_dynamic_command(args)
        else:
            click.echo(ctx.get_help())


def _handle_dynamic_command(args: list[str]) -> None:
    """Handle dynamic hierarchical commands (e.g. ucli mcp-atlassian jira issue create)."""
    from ucli.cli.resolver import ExecResult, resolve_command

    result = resolve_command(args)
    if result is None:
        raise SystemExit(1)

    if isinstance(result, ExecResult):
        _handle_exec_command(result)
    else:
        _handle_tool_command(result)


def _handle_tool_command(result) -> None:
    """Call a resolved MCP tool through the daemon."""
    from ucli.daemon.client import call_tool
    from ucli.daemon.lifecycle import ensure_daemon

    if not ensure_daemon():
        click.echo("Error: could not start daemon.", err=True)
        raise SystemExit(1)

    try:
        response = call_tool(result.server, result.tool, result.params)
    except TimeoutError as exc:
        raise click.ClickException(
            "The tool call timed out. It may still be running. Check the application before retrying; "
            "set UCLI_TIMEOUT to allow more time."
        ) from exc
    except (OSError, ConnectionError, ValueError) as exc:
        raise click.ClickException(str(exc)) from exc

    if response.get("ok"):
        output = response.get("result", "")
        click.echo(output)
    else:
        error = response.get("error", {})
        click.echo(
            f"Error [{error.get('code', 'UNKNOWN')}]: {error.get('message', 'Unknown error')}",
            err=True,
        )
        raise SystemExit(1)


def _handle_exec_command(result) -> None:
    """Run a resolved _exec command as a local subprocess."""
    import subprocess

    def _expand_user(value: str) -> str:
        return str(Path(value).expanduser()) if value.startswith("~") else value

    argv = [_expand_user(result.command)]
    argv.extend(_expand_user(arg) for arg in result.args)
    for param_name, flag in result.param_map.items():
        if param_name not in result.exec_params:
            continue
        argv.extend([flag, str(result.exec_params[param_name])])

    try:
        proc = subprocess.run(argv, shell=False)
    except FileNotFoundError:
        click.echo(f"Error: command not found: {argv[0]}", err=True)
        raise SystemExit(1)

    if proc.returncode:
        raise SystemExit(proc.returncode)


def _preset_status(local_ver: str | None, remote_entry) -> str:
    """Return a human-readable status string for a preset."""
    if local_ver and remote_entry:
        return "synced"
    if local_ver:
        return "local"
    return "remote"


def _display_preset_info(entry, version: str | None) -> None:
    """Print preset availability info to stdout."""
    display_ver = version or entry.latest
    click.echo("\nPre-generated skill files available:")
    click.echo(
        f"  Version: {display_ver} | "
        f"Tools: {entry.tool_count} | "
        f"Updated: {entry.updated_at[:10]}"
    )
    if entry.versions and len(entry.versions) > 1:
        click.echo(f"  Available versions: {', '.join(entry.versions)}")


def _display_install_name(raw_name: str, server_name: str) -> None:
    """Print install-name normalization only when it changes the input."""
    if raw_name != server_name:
        click.echo(f"  '{raw_name}' -> '{server_name}' (install name)")


def _warn_deprecated(old_cmd: str, new_cmd: str) -> None:
    """Print a short deprecation notice for hidden compatibility commands."""
    click.echo(f"Deprecated: use `{new_cmd}` instead of `{old_cmd}`.", err=True)


@cli.group("mcp")
def mcp_group():
    """Manage MCP servers, raw tools, and direct tool calls."""
    pass


@cli.group("cli")
def cli_group():
    """Manage generated CLI mappings."""
    pass


@cli.group("skill")
def skill_group():
    """Manage generated skill files."""
    pass


# ---------------------------------------------------------------------------
# list
# ---------------------------------------------------------------------------

def _run_list_servers() -> None:
    """List all MCP servers from all config sources."""
    from ucli.config.reader import list_all_servers

    servers = list_all_servers()
    if not servers:
        click.echo("No MCP servers found.")
        click.echo("Check ~/.claude.json, ~/.cursor/mcp.json, or ~/.agents/ucli/servers.yaml")
        return

    click.echo(f"{'NAME':<25} {'SOURCE':<30}")
    click.echo("-" * 55)
    for s in servers:
        click.echo(f"{s['name']:<25} {s['source']:<30}")


@mcp_group.command("list")
def mcp_list_cmd():
    """List all MCP servers from all config sources."""
    _run_list_servers()


@cli.command("list")
def list_servers():
    """List shipped tools and configured MCP servers."""
    from ucli.installer.managed import installed_record, shipped_presets

    click.echo("Shipped tools:")
    for name, source in sorted(shipped_presets().items()):
        record = installed_record(name)
        status = f"installed {record['version']}" if record else "available"
        click.echo(f"  {name:<20} {source.name:<12} {status}")
    click.echo("\nConfigured servers:")
    _run_list_servers()


# ---------------------------------------------------------------------------
# scan
# ---------------------------------------------------------------------------

def _run_scan(server_name: str) -> None:
    """Scan an MCP server's tool list."""
    from ucli.scanner import scan_server

    result = scan_server(server_name)
    if result is None:
        raise SystemExit(1)


@mcp_group.command("scan")
@click.argument("server_name")
def mcp_scan_cmd(server_name: str):
    """Scan an MCP server's tool list."""
    _run_scan(server_name)


@cli.command("scan", hidden=True)
@click.argument("server_name")
def scan(server_name: str):
    """Compatibility alias for `ucli mcp scan`."""
    _warn_deprecated("ucli scan", "ucli mcp scan")
    _run_scan(server_name)


# ---------------------------------------------------------------------------
# validate
# ---------------------------------------------------------------------------

def _run_cli_validate(server_name: str) -> bool:
    """Validate a CLI mapping for one server."""
    from ucli.cli.mapping import cli_path

    from ucli.generator.validator import validate_cli_yaml

    cp = cli_path(server_name)
    if not cp.exists():
        click.echo(f"No CLI mapping found for '{server_name}'.")
        return False

    click.echo(f"Validating {cp}...")
    errors = validate_cli_yaml(server_name)
    if errors:
        for e in errors:
            click.echo(f"  ✗ {e}")
        return False

    click.echo("  All CLI checks passed ✓")
    return True


def _run_skill_validate(server_name: str) -> bool:
    """Validate generated skill files for one server."""
    from ucli.generator.validator import validate_skill
    from ucli.utils import skills_path

    sd = skills_path(server_name)
    if not sd.exists():
        click.echo(f"No skill files found for '{server_name}'.")
        return False

    click.echo(f"Validating {sd}...")
    errors = validate_skill(server_name)
    if errors:
        for e in errors:
            click.echo(f"  ✗ {e}")
        return False

    click.echo("  All skill checks passed ✓")
    return True


def _run_validate_all(server_name: str) -> None:
    """Validate CLI mapping and skill files for one server."""
    from ucli.cli.mapping import cli_path
    from ucli.utils import skills_path

    has_errors = False

    cp = cli_path(server_name)
    if cp.exists():
        has_errors = not _run_cli_validate(server_name) or has_errors

    sd = skills_path(server_name)
    if sd.exists():
        has_errors = not _run_skill_validate(server_name) or has_errors

    if not cp.exists() and not sd.exists():
        click.echo(f"No CLI or skill files found for '{server_name}'.")
        has_errors = True

    if has_errors:
        raise SystemExit(1)


@cli_group.command("validate")
@click.argument("server_name")
def cli_validate_cmd(server_name: str):
    """Validate a generated CLI mapping for a server."""
    if not _run_cli_validate(server_name):
        raise SystemExit(1)


@skill_group.command("validate")
@click.argument("server_name")
def skill_validate_cmd(server_name: str):
    """Validate generated skill files for a server."""
    if not _run_skill_validate(server_name):
        raise SystemExit(1)


@cli.command("validate", hidden=True)
@click.argument("server_name")
def validate(server_name: str):
    """Compatibility alias for split CLI and skill validation commands."""
    _warn_deprecated("ucli validate", "ucli cli validate / ucli skill validate")
    _run_validate_all(server_name)


# ---------------------------------------------------------------------------
# generate
# ---------------------------------------------------------------------------

@cli.group("generate", hidden=True)
def generate():
    """Compatibility group for old generation commands."""
    pass


@cli_group.command("generate")
@click.argument("server_name")
@click.option("--merge", is_flag=True, help="Incremental merge for new tools only")
def cli_generate_cmd(server_name: str, merge: bool):
    """Generate CLI command tree YAML via AI."""
    from ucli.generator.cli_gen import generate_cli

    ok = generate_cli(server_name, merge=merge)
    if not ok:
        raise SystemExit(1)
    click.echo(f"Next: run 'ucli skill generate {server_name}' to create a SKILL.md")


@skill_group.command("generate")
@click.argument("server_name")
@click.option("-o", "--output", type=click.Path(), help="Output directory")
def skill_generate_cmd(server_name: str, output: str | None):
    """Generate Skill files (SKILL.md + reference + examples) via AI."""
    from ucli.generator.skill_gen import generate_skill

    output_dir = Path(output) if output else None
    ok = generate_skill(server_name, output_dir=output_dir)
    if not ok:
        raise SystemExit(1)


@generate.command("cli")
@click.argument("server_name")
@click.option("--merge", is_flag=True, help="Incremental merge for new tools only")
def generate_cli_cmd(server_name: str, merge: bool):
    """Compatibility alias for `ucli cli generate`."""
    _warn_deprecated("ucli generate cli", "ucli cli generate")
    cli_generate_cmd.callback(server_name, merge)


@generate.command("skill")
@click.argument("server_name")
@click.option("-o", "--output", type=click.Path(), help="Output directory")
def generate_skill_cmd(server_name: str, output: str | None):
    """Compatibility alias for `ucli skill generate`."""
    _warn_deprecated("ucli generate skill", "ucli skill generate")
    skill_generate_cmd.callback(server_name, output)


@mcp_group.command("add")
@click.argument("server_name")
@click.option("--source", default="auto", help="Config source (auto/claude/cursor/codex)")
@click.option("--skip-disable", is_flag=True, help="Don't disable original MCP config")
@click.option("--no-preset", is_flag=True, help="Skip preset check")
@click.option("--preset-version", default=None, help="Use a specific preset version (e.g. 1.2.3)")
@click.option("--yes", is_flag=True, help="Skip confirmation")
@click.option("--force", is_flag=True, help="Overwrite servers.yaml entry")
def mcp_add(
    server_name: str,
    source: str,
    skip_disable: bool,
    no_preset: bool,
    preset_version: str | None,
    yes: bool,
    force: bool,
):
    """Convert an already-configured MCP server to skill-based usage."""
    from ucli.converter.config_extractor import ServerNotFoundError, extract_server_config

    click.echo(f"Finding {server_name} in config sources...")

    try:
        config, sources = extract_server_config(server_name, source)
    except ServerNotFoundError as e:
        click.echo(str(e), err=True)
        raise SystemExit(1)

    for src in sources:
        click.echo(f"  Found in: {src.config_path} ({src.client})")

    click.echo(f"\nExtracted config:")
    click.echo(f"  command: {config.command}")
    click.echo(f"  args: {config.args}")
    if config.env:
        click.echo(f"  env: {', '.join(config.env.keys())} ({len(config.env)} vars)")

    _run_convert(
        server_name=server_name,
        config=config,
        no_preset=no_preset,
        preset_version=preset_version,
        yes=yes,
        force=force,
        skip_disable=skip_disable,
    )


@mcp_group.command("remove")
@click.argument("server_name")
def mcp_remove(server_name: str):
    """Remove an MCP server from servers.yaml."""
    from ucli.installer.servers_writer import remove_server

    if not remove_server(server_name):
        raise SystemExit(1)


# ---------------------------------------------------------------------------
# exec
# ---------------------------------------------------------------------------

@cli.group("exec")
def exec_group():
    """Manage local file-backed commands."""
    pass


@exec_group.command("add")
@click.argument("server_name")
@click.option("--path", "target_path", required=True, type=click.Path(), help="Go/Python/Shell file or directory")
@click.option("--command-path", default=None, help='Command path, e.g. "bot send"')
@click.option("--no-sync", is_flag=True, help="Don't regenerate and sync skill files after updating cli.yaml")
def exec_add_cmd(server_name: str, target_path: str, command_path: str | None, no_sync: bool):
    """Generate or merge _exec command mappings into cli.yaml."""
    from ucli.file_exec import add_exec

    if not add_exec(server_name, target_path, command_path=command_path, sync=not no_sync):
        raise SystemExit(1)


@exec_group.command("list")
@click.argument("server_name")
def exec_list_cmd(server_name: str):
    """List _exec commands in a server CLI mapping."""
    from ucli.file_exec import list_exec

    if not list_exec(server_name):
        raise SystemExit(1)


@exec_group.command("remove")
@click.argument("server_name")
@click.option("--command-path", required=True, help='Command path, e.g. "bot send"')
@click.option("--no-sync", is_flag=True, help="Don't regenerate and sync skill files after updating cli.yaml")
def exec_remove_cmd(server_name: str, command_path: str, no_sync: bool):
    """Remove one _exec command from a server CLI mapping."""
    from ucli.file_exec import remove_exec

    if not remove_exec(server_name, command_path, sync=not no_sync):
        raise SystemExit(1)


@skill_group.command("sync")
@click.argument("server_name", required=False)
@click.option("--targets", help="Target clients (comma-separated: claude,cursor,codex)")
@click.option("--skip-disable", is_flag=True, help="Don't disable MCP in client configs")
def skill_sync_cmd(server_name: str | None, targets: str | None, skip_disable: bool):
    """Sync skill files to AI client directories."""
    from ucli.constants import SKILLS_DIR
    from ucli.installer.skill_sync import skill_sync

    target_list = targets.split(",") if targets else None

    if server_name:
        ok = skill_sync(server_name, targets=target_list, skip_disable=skip_disable)
        if not ok:
            raise SystemExit(1)
    else:
        if not SKILLS_DIR.exists():
            click.echo("No skill files found.")
            return
        for d in SKILLS_DIR.iterdir():
            if d.is_dir() and (d / "SKILL.md").exists():
                skill_sync(d.name, targets=target_list, skip_disable=skip_disable)


@skill_group.command("unsync")
@click.argument("server_name", required=False)
@click.option("--targets", help="Target clients (comma-separated: claude,cursor,codex)")
@click.option("--skip-re-enable", is_flag=True, help="Don't re-enable MCP in client configs")
def skill_unsync_cmd(server_name: str | None, targets: str | None, skip_re_enable: bool):
    """Remove skill files from AI client directories and re-enable MCP."""
    from ucli.constants import CLIENT_CONFIGS
    from ucli.remover.cleaner import unsync_skills
    from ucli.remover.config_re_enabler import re_enable_server
    from ucli.utils import safe_filename, shared_skills_path

    target_clients = targets.split(",") if targets else list(CLIENT_CONFIGS.keys())

    def _unsync_one(sname: str) -> None:
        copies: list[Path] = []
        for client in target_clients:
            info = CLIENT_CONFIGS.get(client)
            if not info:
                continue
            skill_dir = info["skill_dir"] / safe_filename(sname)
            if skill_dir.exists():
                copies.append(skill_dir)

        agents = shared_skills_path(sname)
        agents_dir = agents if agents.exists() else None

        unsync_skills(sname, copies, agents_dir)

        if not skip_re_enable:
            for client in target_clients:
                info = CLIENT_CONFIGS.get(client)
                if not info:
                    continue
                re_enable_server(sname, info["config_path"], info["format"])

    if server_name:
        _unsync_one(server_name)
    else:
        from ucli.constants import SKILLS_DIR
        if SKILLS_DIR.exists():
            for d in SKILLS_DIR.iterdir():
                if d.is_dir():
                    _unsync_one(d.name)


# ---------------------------------------------------------------------------
# install
# ---------------------------------------------------------------------------

@mcp_group.command("install")
@click.argument("server_name")
@click.option("--env", "env_pairs", multiple=True, help="Env values (KEY=VALUE)")
@click.option("--client", "--skill-targets", "skill_targets", help="Clients, comma-separated: codex,claude,cursor (default: codex)")
@click.option("--no-preset", is_flag=True, help="Skip preset check")
@click.option("--preset-version", default=None, help="Use a specific preset version (e.g. 1.2.3)")
@click.option("--preset-dir", default=None, type=click.Path(exists=True, file_okay=False),
              help="Use a local preset directory instead of GitHub")
@click.option("--yes", is_flag=True, help="Skip confirmation")
@click.option("--force", is_flag=True, help="Replace an existing installation or edited managed files")
def install(
    server_name: str,
    env_pairs: tuple,
    skill_targets: str | None,
    no_preset: bool,
    preset_version: str | None,
    preset_dir: str | None,
    yes: bool,
    force: bool,
):
    """Install a tool, its MCP backend, CLI commands, and skill."""
    from ucli.installer.names import resolve_install_spec

    install_spec = resolve_install_spec(server_name)
    server_name = install_spec.local_name

    preset_envs: dict[str, str] = {}
    for pair in env_pairs:
        if "=" not in pair or not pair.split("=", 1)[0]:
            raise click.BadParameter("Use KEY=VALUE", param_hint="--env")
        k, v = pair.split("=", 1)
        preset_envs[k] = v

    from ucli.constants import CLIENT_CONFIGS
    targets = [t.strip() for t in skill_targets.split(",")] if skill_targets is not None else None
    if targets is not None and (not targets or set(targets) - CLIENT_CONFIGS.keys()):
        raise click.BadParameter("Choose codex, claude, or cursor", param_hint="--client")
    from ucli.installer.managed import install_preset, shipped_presets
    shipped = shipped_presets()
    if not no_preset and preset_dir is None and server_name in shipped:
        source = shipped[server_name]
        if preset_version is not None:
            source = source.parent / preset_version
            if source.parent != shipped[server_name].parent or not (source / "manifest.json").is_file():
                raise click.ClickException(f"No shipped version {preset_version} for {server_name}.")
        try:
            install_preset(server_name, source, clients=targets, env=preset_envs, force=force)
        except click.ClickException:
            raise
        except Exception as exc:
            raise click.ClickException(f"Installation failed: {exc}") from exc
        return
    targets = targets or ["codex"]

    # --- Local preset fast path (--preset-dir) ---
    if preset_dir is not None:
        _display_install_name(install_spec.raw, server_name)
        source = _resolve_local_preset_dir(server_name, Path(preset_dir))
        if source is None:
            raise SystemExit(1)
        import json
        if "runtime" in json.loads((source / "manifest.json").read_text()):
            try:
                install_preset(server_name, source, clients=targets, env=preset_envs, force=force)
            except click.ClickException:
                raise
            except Exception as exc:
                raise click.ClickException(f"Installation failed: {exc}") from exc
            return
        ok = _try_local_preset_install(
            server_name, Path(preset_dir), preset_envs, yes, targets,
        )
        if ok:
            return
        raise SystemExit(1)

    # --- Already configured locally → convert flow ---
    from ucli.converter.config_extractor import ServerNotFoundError, extract_server_config
    try:
        existing_config, existing_sources = extract_server_config(server_name, "auto")
        _run_convert(
            server_name=server_name,
            config=existing_config,
            no_preset=no_preset,
            preset_version=preset_version,
            yes=yes,
            force=force,
            skip_disable=True,
            targets=targets,
        )
        return
    except ServerNotFoundError:
        pass

    # --- Preset-first fast path ---
    if not no_preset:
        for lookup_name in install_spec.lookup_names:
            ok = _try_preset_install(
                lookup_name, preset_envs, preset_version, yes, targets,
            )
            if ok:
                return

    # --- Fallback: AI search flow ---
    from ucli.config.models import ServerConfig
    from ucli.installer.ai_search import ai_search_server, build_server_meta
    from ucli.installer.interactive import collect_env_values
    from ucli.installer.pipeline import build_pipeline, run_pipeline
    from ucli.installer.servers_writer import write_server

    _display_install_name(install_spec.raw, server_name)
    search_result = ai_search_server(server_name, search_query=install_spec.raw)
    if search_result is None or not search_result.found:
        raise SystemExit(1)

    env_values = collect_env_values(search_result.env, preset_envs)

    config = ServerConfig(
        name=server_name,
        command=search_result.command,
        args=search_result.args,
        env=env_values,
    )

    # Build server_meta from AI search result for embedding in tools.json
    server_meta = build_server_meta(search_result)

    if not yes:
        click.echo(f"\nWill write to servers.yaml:")
        click.echo(f"  {server_name}:")
        click.echo(f"    command: {config.command} {' '.join(config.args)}")
        if env_values:
            click.echo(f"    env: {', '.join(env_values.keys())} ({len(env_values)} values set)")
        if search_result.source_url:
            click.echo(f"  Source: {search_result.source_url}")

        # Probe for preset before confirmation
        from ucli.preset.checker import probe_preset

        preset_entry = probe_preset(server_name, version=preset_version, no_preset=no_preset)
        if preset_entry is not None:
            _display_preset_info(preset_entry, preset_version)
        else:
            if not click.confirm("\nProceed?", default=True):
                click.echo("Aborted.")
                return

    pipeline = build_pipeline(
        server_name, config,
        write_step_name="mcp-add",
        no_preset=no_preset,
        preset_version=preset_version,
        server_meta=server_meta,
        targets=targets,
        skip_disable=True,
    )
    results = run_pipeline(pipeline)

    if results.all_ok:
        click.echo("\n✅ Installation complete!")
        click.echo(f"  Use CLI: ucli {server_name} --help")
        click.echo(f"  Skill installed for: {', '.join(targets)}")
        click.echo(f"  Tip: edit ~/.agents/ucli/servers.yaml to change env vars (API keys, etc.)")
    else:
        failed = results.failed_fatal
        click.echo(f"\n⚠ Installation partially complete. Failed steps: {', '.join(failed)}")
        raise SystemExit(1)


cli.add_command(install, "install")


@cli.command("doctor")
@click.argument("server_name")
def doctor_cmd(server_name: str):
    """Check installed files, MCP startup, and application readiness."""
    from ucli.installer.managed import doctor

    if not doctor(server_name):
        raise SystemExit(1)


def _resolve_local_preset_dir(server_name: str, preset_dir: Path) -> Path | None:
    """Resolve the version directory from a user-specified preset directory.

    Priority:
      1. preset_dir itself contains manifest.json → use as version dir
      2. preset_dir/<server_name>/<version>/ structure → pick latest version dir
    """
    from ucli.utils import safe_filename

    if (preset_dir / "manifest.json").exists():
        return preset_dir

    server_dir = preset_dir / safe_filename(server_name)
    if server_dir.exists():
        version_dirs = sorted(
            [d for d in server_dir.iterdir()
             if d.is_dir() and (d / "manifest.json").exists()],
            reverse=True,
        )
        if version_dirs:
            return version_dirs[0]

    click.echo(
        f"Error: no preset found in '{preset_dir}' for server '{server_name}'.",
        err=True,
    )
    click.echo(
        f"  Expected: {preset_dir}/manifest.json, "
        f"or {preset_dir}/{safe_filename(server_name)}/<version>/manifest.json",
        err=True,
    )
    return None


def _try_local_preset_install(
    server_name: str,
    preset_dir: Path,
    preset_envs: dict[str, str],
    yes: bool,
    targets: list[str] | None = None,
) -> bool:
    """Install from a local preset directory.

    Returns True on success, False on failure.
    """
    import json

    version_dir = _resolve_local_preset_dir(server_name, preset_dir)
    if version_dir is None:
        return False

    tools_path = version_dir / "tools.json"
    if not tools_path.exists():
        click.echo(f"Error: no tools.json found in {version_dir}", err=True)
        return False

    try:
        tools_data = json.loads(tools_path.read_text(encoding="utf-8"))
    except Exception as e:
        click.echo(f"Error: could not read tools.json: {e}", err=True)
        return False

    server_meta = tools_data.get("server_meta")
    if not server_meta:
        click.echo("Error: tools.json has no server_meta.", err=True)
        return False

    command = server_meta.get("command", "")
    args = server_meta.get("args", [])
    env_defs = server_meta.get("env", {})

    if not command:
        click.echo("Error: preset server_meta is missing 'command'.", err=True)
        return False

    from ucli.installer.interactive import collect_env_values

    env_values = collect_env_values(env_defs, preset_envs)

    if not yes:
        click.echo(f"\nWill write to servers.yaml:")
        click.echo(f"  {server_name}:")
        click.echo(f"    command: {command} {' '.join(args)}")
        if env_values:
            click.echo(f"    env: {', '.join(env_values.keys())} ({len(env_values)} values set)")
        click.echo(f"  Source: local preset at {version_dir}")
        if not click.confirm("\nProceed?", default=True):
            click.echo("Aborted.")
            raise SystemExit(0)

    from ucli.config.models import ServerConfig
    from ucli.installer.servers_writer import write_server

    config = ServerConfig(
        name=server_name,
        command=command,
        args=args,
        env=env_values,
    )
    if not write_server(config):
        return False

    from ucli.preset.downloader import install_from_local_dir

    click.echo("Installing from local preset...")
    ok = install_from_local_dir(server_name, version_dir, force=True)
    if not ok:
        return False

    from ucli.installer.skill_sync import skill_sync

    click.echo("Syncing skills...")
    skill_sync(server_name, targets=targets, skip_disable=True)

    click.echo("\n✅ Installation complete! (local preset)")
    click.echo(f"  Use CLI: ucli {server_name} --help")
    click.echo(f"  Skill installed for: {', '.join(targets or ['codex'])}")
    click.echo(f"  Tip: edit ~/.agents/ucli/servers.yaml to change env vars (API keys, etc.)")
    return True


def _try_preset_install(
    server_name: str,
    preset_envs: dict[str, str],
    preset_version: str | None,
    yes: bool,
    targets: list[str] | None = None,
) -> bool:
    """Try to install from a remote preset (fast path).

    Returns True if preset install succeeded, False to fall back to AI search.
    """
    from ucli.preset.checker import probe_preset_with_alias

    probe = probe_preset_with_alias(server_name, version=preset_version)
    if probe.entry is None:
        return False

    # Alias resolution feedback
    canonical_name = probe.resolved_name
    if probe.alias_used:
        click.echo(f"  '{server_name}' → '{canonical_name}' (alias match)")

    entry = probe.entry
    click.echo(
        f"\nFound preset: {canonical_name}@{entry.latest} "
        f"({entry.tool_count} tools)"
    )
    if entry.description:
        click.echo(f"  {entry.description}")

    # Fetch server_meta from remote tools.json
    from ucli.preset.checker import fetch_server_meta_from_preset

    server_meta = fetch_server_meta_from_preset(canonical_name, version=preset_version)
    if server_meta is None:
        click.echo("  Preset has no server_meta. Falling back to AI search.")
        return False

    command = server_meta.get("command", "")
    args = server_meta.get("args", [])
    env_defs = server_meta.get("env", {})

    if not command:
        click.echo("  Preset server_meta is incomplete. Falling back to AI search.")
        return False

    # Collect env values interactively
    from ucli.installer.interactive import collect_env_values

    env_values = collect_env_values(env_defs, preset_envs)

    # Show summary
    click.echo(f"\nWill write to servers.yaml:")
    click.echo(f"  {canonical_name}:")
    click.echo(f"    command: {command} {' '.join(args)}")
    if env_values:
        click.echo(f"    env: {', '.join(env_values.keys())} ({len(env_values)} values set)")

    # Write servers.yaml
    from ucli.config.models import ServerConfig
    from ucli.installer.servers_writer import write_server

    config = ServerConfig(
        name=canonical_name,
        command=command,
        args=args,
        env=env_values,
    )
    if not write_server(config):
        return False

    # Pull preset files (tools.json, cli.yaml, skills/)
    from ucli.preset.downloader import pull_preset

    click.echo("Pulling preset...")
    ok = pull_preset(canonical_name, version=preset_version, force=True)
    if not ok:
        click.echo("  Preset download failed.", err=True)
        return False

    # Skill sync
    from ucli.installer.skill_sync import skill_sync

    click.echo("Syncing skills...")
    skill_sync(canonical_name, targets=targets, skip_disable=True)

    click.echo("\n✅ Installation complete! (preset-based, no AI search)")
    click.echo(f"  Use CLI: ucli {canonical_name} --help")
    click.echo(f"  Skill installed for: {', '.join(targets or ['codex'])}")
    click.echo(f"  Tip: edit ~/.agents/ucli/servers.yaml to change env vars (API keys, etc.)")
    return True


# ---------------------------------------------------------------------------
# convert
# ---------------------------------------------------------------------------

def _run_convert(
    server_name: str,
    config,
    no_preset: bool,
    preset_version: str | None,
    yes: bool,
    force: bool,
    skip_disable: bool,
    targets: list[str] | None = None,
) -> None:
    """Core convert logic shared by `install` (local fast-path) and `convert` command."""
    from ucli.installer.pipeline import build_pipeline, run_pipeline
    from ucli.preset.checker import probe_preset

    preset_entry = probe_preset(server_name, version=preset_version, no_preset=no_preset)

    if preset_entry is not None:
        _display_preset_info(preset_entry, preset_version)
    else:
        if not yes:
            if not click.confirm("\nProceed?", default=True):
                click.echo("Aborted.")
                return

    server_meta = config.to_server_meta()

    pipeline = build_pipeline(
        server_name=server_name,
        config=config,
        force_write=force,
        skip_disable=skip_disable,
        no_preset=no_preset,
        preset_version=preset_version,
        server_meta=server_meta,
        targets=targets,
    )
    results = run_pipeline(pipeline)

    if results.all_ok:
        click.echo("\n✅ Convert complete!")
        if not skip_disable:
            click.echo("  Original MCP config disabled (can re-enable manually)")
        else:
            click.echo("  Original MCP config was NOT disabled (--skip-disable)")
        click.echo(f"  Tip: edit ~/.agents/ucli/servers.yaml to change env vars (API keys, etc.)")
    else:
        failed = results.failed_fatal
        click.echo(f"\n⚠ Convert partially complete. Failed steps: {', '.join(failed)}")


# ---------------------------------------------------------------------------
# remove / uninstall
# ---------------------------------------------------------------------------

@cli.command()
@click.argument("server_name")
@click.option("--keep-config", is_flag=True, help="Keep servers.yaml config, only remove generated files")
@click.option("--skip-re-enable", is_flag=True, help="Don't re-enable MCP in client configs")
@click.option("--purge-package", is_flag=True, help="Also uninstall the underlying package")
@click.option("--force", "-f", is_flag=True, help="Skip confirmation prompt")
@click.option("--dry-run", is_flag=True, help="Preview actions without modifying files")
def remove(
    server_name: str,
    keep_config: bool,
    skip_re_enable: bool,
    purge_package: bool,
    force: bool,
    dry_run: bool,
):
    """Remove a server and all its generated artifacts."""
    from ucli.installer.managed import installed_record, uninstall

    if installed_record(server_name):
        uninstall(server_name, force=force, dry_run=dry_run, keep_config=keep_config)
        return
    from ucli.installer.pipeline import run_pipeline
    from ucli.remover.pipeline import build_remove_pipeline
    from ucli.remover.scanner import scan_removal_targets

    click.echo(f"Scanning {server_name} artifacts...")

    plan = scan_removal_targets(server_name)

    if plan.server_name != server_name:
        click.echo(f"  '{server_name}' → '{plan.server_name}' (alias match)")
        server_name = plan.server_name

    if plan.is_empty():
        click.echo(f"\nServer \"{server_name}\" not found.")
        click.echo("  Use `ucli mcp list` to see all configured servers.")
        raise SystemExit(1)

    # Show plan
    lines = plan.summary_lines()
    click.echo(f"\nThe following will be removed:")
    for line in lines:
        click.echo(f"  {line}")

    if keep_config:
        click.echo(f"\n  Config: servers.yaml KEPT (--keep-config)")

    if plan.protected_dirs_with_content and not force:
        protected = ", ".join(
            f"{name}/" for name in sorted(plan.protected_dirs_with_content)
        )
        plan.keep_protected_dirs = not click.confirm(
            f"\n  Protected skill directories have custom content ({protected}). "
            "Delete them too?",
            default=False,
        )

    if dry_run:
        click.echo("\n[DRY RUN] No files were modified.")
        return

    if not force:
        if not click.confirm("\nProceed?", default=True):
            click.echo("Aborted.")
            return

    pipeline = build_remove_pipeline(
        plan,
        keep_config=keep_config,
        skip_re_enable=skip_re_enable,
        purge_package=purge_package,
    )
    results = run_pipeline(pipeline)

    if results.all_ok:
        click.echo(f"\n✅ {server_name} removed successfully!")
    else:
        failed = results.failed_fatal
        click.echo(f"\n⚠ Removal partially complete. Failed steps: {', '.join(failed)}")


# Alias: uninstall = remove
cli.add_command(remove, "uninstall")


# ---------------------------------------------------------------------------
# update
# ---------------------------------------------------------------------------

@mcp_group.command("update")
@click.argument("server_name", required=False)
@click.option("--all", "update_all_flag", is_flag=True, help="Update all registered servers")
@click.option("--yes", "-y", is_flag=True, help="Skip confirmation")
@click.option("--dry-run", is_flag=True, help="Preview changes without writing files")
def update(server_name: str | None, update_all_flag: bool, yes: bool, dry_run: bool):
    """Update server tools and regenerate CLI + skill files."""
    from ucli.updater.pipeline import update_all, update_server

    if update_all_flag:
        ok = update_all(yes=yes, dry_run=dry_run)
    elif server_name:
        ok = update_server(server_name, yes=yes, dry_run=dry_run)
    else:
        click.echo("Error: provide a server name or use --all.", err=True)
        raise SystemExit(1)

    if not ok:
        raise SystemExit(1)


cli.add_command(update, "update")


# ---------------------------------------------------------------------------
# tools (list tools for a server)
# ---------------------------------------------------------------------------

def _run_tools(server_name: str, tool_name: str | None) -> None:
    """List tools or show tool details for an MCP server."""
    from ucli.config.tool_store import load_tools

    tools_json = load_tools(server_name)
    if tools_json is None:
        click.echo(f"No tools found for '{server_name}'. Run `ucli mcp scan {server_name}` first.")
        raise SystemExit(1)

    if tool_name:
        tool = next((t for t in tools_json.tools if t.name == tool_name), None)
        if not tool:
            click.echo(f"Tool '{tool_name}' not found in {server_name}.")
            click.echo(f"Available: {', '.join(t.name for t in tools_json.tools)}")
            raise SystemExit(1)

        click.echo(f"Tool: {tool.name}")
        click.echo(f"Description: {tool.description}")
        props = tool.input_schema.get("properties", {})
        required = set(tool.input_schema.get("required", []))
        if props:
            click.echo(f"\nParameters:")
            for pname, pschema in props.items():
                req = "(required)" if pname in required else "(optional)"
                ptype = pschema.get("type", "")
                pdesc = pschema.get("description", "")
                click.echo(f"  --{pname.replace('_', '-'):<25} {req:<12} {ptype:<8} {pdesc}")
    else:
        click.echo(f"Tools for {server_name} ({len(tools_json.tools)} tools):")
        click.echo(f"{'NAME':<40} {'DESCRIPTION'}")
        click.echo("-" * 80)
        for tool in tools_json.tools:
            desc = (tool.description[:55] + "...") if len(tool.description) > 58 else tool.description
            click.echo(f"{tool.name:<40} {desc}")


@mcp_group.command("tools")
@click.argument("server_name")
@click.argument("tool_name", required=False)
def mcp_tools_cmd(server_name: str, tool_name: str | None):
    """List tools or show tool details for an MCP server."""
    _run_tools(server_name, tool_name)


@cli.command("tools", hidden=True)
@click.argument("server_name")
@click.argument("tool_name", required=False)
def tools_cmd(server_name: str, tool_name: str | None):
    """Compatibility alias for `ucli mcp tools`."""
    _warn_deprecated("ucli tools", "ucli mcp tools")
    _run_tools(server_name, tool_name)


# ---------------------------------------------------------------------------
# call (direct tool call)
# ---------------------------------------------------------------------------

def _run_call(server_name: str, tool_name: str, extra_args: tuple, timeout: int) -> None:
    """Directly call an MCP tool by its raw name."""
    from ucli.cli.resolver import _parse_args
    from ucli.daemon.client import call_tool
    from ucli.daemon.lifecycle import ensure_daemon

    params = _parse_args(list(extra_args), server_name, tool_name)

    if not ensure_daemon():
        click.echo("Error: could not start daemon.", err=True)
        raise SystemExit(1)

    response = call_tool(server_name, tool_name, params, timeout=timeout)

    if response.get("ok"):
        click.echo(response.get("result", ""))
    else:
        error = response.get("error", {})
        click.echo(
            f"Error [{error.get('code', 'UNKNOWN')}]: {error.get('message', '')}",
            err=True,
        )
        raise SystemExit(1)


@mcp_group.command("call")
@click.argument("server_name")
@click.argument("tool_name")
@click.argument("extra_args", nargs=-1, type=click.UNPROCESSED)
@click.option("--timeout", default=60, help="Request timeout in seconds")
def mcp_call_cmd(server_name: str, tool_name: str, extra_args: tuple, timeout: int):
    """Directly call an MCP tool by its raw name."""
    _run_call(server_name, tool_name, extra_args, timeout)


@cli.command("call", hidden=True)
@click.argument("server_name")
@click.argument("tool_name")
@click.argument("extra_args", nargs=-1, type=click.UNPROCESSED)
@click.option("--timeout", default=60, help="Request timeout in seconds")
def call_cmd(server_name: str, tool_name: str, extra_args: tuple, timeout: int):
    """Compatibility alias for `ucli mcp call`."""
    _warn_deprecated("ucli call", "ucli mcp call")
    _run_call(server_name, tool_name, extra_args, timeout)


# ---------------------------------------------------------------------------
# daemon
# ---------------------------------------------------------------------------

@cli.group("daemon")
def daemon_group():
    """Manage the MCP proxy daemon."""
    pass


@daemon_group.command("status")
def daemon_status_cmd():
    """Show daemon status."""
    from ucli.daemon.lifecycle import get_daemon_info

    info = get_daemon_info()
    if info is None:
        click.echo("Daemon is not running.")
        return

    click.echo(f"Daemon is running:")
    click.echo(f"  PID: {info['pid']}")
    click.echo(f"  Socket: {info['socket']}")
    servers = info.get("servers", [])
    if servers:
        click.echo(f"  Active servers: {', '.join(servers)}")
    else:
        click.echo(f"  Active servers: (none)")


@daemon_group.command("stop")
def daemon_stop_cmd():
    """Stop the daemon."""
    from ucli.daemon.lifecycle import stop_daemon

    if stop_daemon():
        click.echo("Daemon stopped.")
    else:
        click.echo("Daemon is not running.")


@daemon_group.command("reconnect")
@click.argument("server_name")
def daemon_reconnect_cmd(server_name: str):
    """Disconnect a server so it reconnects with updated config on next call."""
    from ucli.daemon.client import daemon_disconnect
    from ucli.daemon.lifecycle import is_daemon_running

    if not is_daemon_running():
        click.echo("Daemon is not running.")
        return

    ok = daemon_disconnect(server_name)
    if ok:
        click.echo(f"'{server_name}' disconnected. It will reconnect with new config on next call.")
    else:
        click.echo(f"'{server_name}' was not connected (nothing to disconnect).")


# ---------------------------------------------------------------------------
# preset
# ---------------------------------------------------------------------------

@cli.group("preset")
def preset_group():
    """Manage preset skill files from remote repository."""
    pass


@preset_group.command("list")
@click.argument("server_name", required=False)
@click.option("--local", "local_only", is_flag=True, help="Show only local presets")
def preset_list_cmd(server_name: str | None, local_only: bool):
    """List presets with local and remote status."""
    from ucli.preset.local import scan_local_presets
    from ucli.preset.registry import fetch_index

    local_map = scan_local_presets()
    index = None if local_only else fetch_index()

    # Detail view for a single server
    if server_name:
        local_ver = local_map.get(server_name)
        remote_entry = index.find(server_name) if index else None

        if not local_ver and not remote_entry:
            click.echo(f"No preset found for '{server_name}'.")
            raise SystemExit(1)

        click.echo(f"Preset: {server_name}")
        click.echo(f"  Local:       {local_ver or '-'}")
        if remote_entry:
            click.echo(f"  Remote:      {remote_entry.latest}")
            click.echo(f"  Versions:    {', '.join(remote_entry.versions)}")
            click.echo(f"  Updated:     {remote_entry.updated_at[:10] if remote_entry.updated_at else '-'}")
            if remote_entry.description:
                click.echo(f"  Description: {remote_entry.description}")
        else:
            click.echo(f"  Remote:      -")

        status = _preset_status(local_ver, remote_entry)
        click.echo(f"  Status:      {status}")
        return

    # Unified list view
    all_names: set[str] = set(local_map.keys())
    if index:
        for p in index.presets:
            all_names.add(p.server)

    if not all_names:
        click.echo("No presets found (local or remote).")
        return

    click.echo(f"  {'NAME':<25} {'LOCAL':<12} {'REMOTE':<12} {'STATUS'}")
    click.echo("  " + "-" * 65)
    for name in sorted(all_names):
        local_ver = local_map.get(name)
        remote_entry = index.find(name) if index else None
        remote_ver = remote_entry.latest if remote_entry else None
        status = _preset_status(local_ver, remote_entry)
        click.echo(
            f"  {name:<25} {local_ver or '-':<12} {remote_ver or '-':<12} {status}"
        )

    total = len(all_names)
    local_count = len(local_map)
    remote_count = len(index.presets) if index else 0
    click.echo(f"\n{total} presets ({local_count} local, {remote_count} remote).")


@preset_group.command("pull")
@click.argument("preset_spec")
@click.option(
    "--sync/--no-sync",
    "do_sync",
    default=True,
    help="Sync to AI clients after pull (default: enabled)",
)
@click.option("--force", is_flag=True, help="Overwrite existing local files")
@click.option("--dry-run", is_flag=True, help="Preview files without downloading")
def preset_pull_cmd(preset_spec: str, do_sync: bool, force: bool, dry_run: bool):
    """Pull preset files for a server from remote repository.

    Supports 'name@version' syntax (e.g. mcp-atlassian@1.2.3).
    Without a version, pulls the latest.
    """
    from ucli.preset.downloader import pull_preset
    from ucli.preset.version import parse_preset_spec

    server_name, version = parse_preset_spec(preset_spec)

    ok = pull_preset(server_name, version=version, force=force, dry_run=dry_run)
    if not ok:
        raise SystemExit(1)

    if dry_run:
        return

    if do_sync:
        from ucli.installer.skill_sync import skill_sync
        click.echo("\nSyncing skill to AI clients...")
        skill_sync(server_name)
    else:
        click.echo(f"\nNext: run 'ucli skill sync {server_name}' to copy to AI clients.")


@preset_group.command("export")
@click.argument("server_name")
@click.option("--version", "preset_version", default=None, help="Override version (default: from tools.json)")
@click.option("-o", "--output", "output_dir", default=".", help="Output directory (default: current directory)")
@click.option("--yes", is_flag=True, help="Skip confirmation")
def preset_export_cmd(server_name: str, preset_version: str | None, output_dir: str, yes: bool):
    """Export a preset bundle to a local directory.

    Validates local files and writes the preset bundle (tools.json, cli.yaml,
    skills/, manifest.json) to <output>/<server>/<version>/.
    """
    _run_preset_export(server_name, preset_version, output_dir, yes)


@cli.command("export", hidden=True)
@click.argument("server_name")
@click.option("--version", "preset_version", default=None, help="Override version (default: from tools.json)")
@click.option("-o", "--output", "output_dir", default=".", help="Output directory (default: current directory)")
@click.option("--yes", is_flag=True, help="Skip confirmation")
def preset_export_alias_cmd(server_name: str, preset_version: str | None, output_dir: str, yes: bool):
    """Compatibility alias for `ucli preset export`."""
    _warn_deprecated("ucli export", "ucli preset export")
    _run_preset_export(server_name, preset_version, output_dir, yes)


def _run_preset_export(
    server_name: str,
    preset_version: str | None,
    output_dir: str,
    yes: bool,
) -> None:
    """Run preset export from either the primary command or compatibility alias."""
    from ucli.preset.exporter import export_preset

    ok = export_preset(server_name, version=preset_version, output_dir=output_dir, yes=yes)
    if not ok:
        raise SystemExit(1)


@preset_group.command("push")
@click.argument("server_name")
@click.option("--version", "preset_version", default=None, help="Override version (default: from tools.json)")
@click.option("--yes", is_flag=True, help="Skip confirmation")
def preset_push_cmd(server_name: str, preset_version: str | None, yes: bool):
    """Push local preset files to the remote repository via git SSH.

    Validates local files, assembles the preset bundle, pushes to a new
    branch, then prints a URL to open in your browser to create the PR.

    Requires git and an SSH key configured for the target repository.
    """
    from ucli.preset.pusher import push_preset

    ok = push_preset(server_name, version=preset_version, yes=yes)
    if not ok:
        raise SystemExit(1)


# ---------------------------------------------------------------------------
# batch
# ---------------------------------------------------------------------------

@cli.group("batch")
def batch_group():
    """Batch operations for converting multiple MCP servers."""
    pass


@batch_group.command("fetch")
@click.option(
    "--source", default="mcpmarket",
    help="Data source for server list (default: mcpmarket)",
)
@click.option("--top", default=100, help="Number of top servers to fetch")
@click.option(
    "-o", "--output", "output_file", default="servers.json",
    help="Output file path (default: servers.json)",
)
@click.option(
    "--no-details", is_flag=True,
    help="Skip fetching individual server detail pages (faster but less info)",
)
@click.option(
    "--delay", default=0.5, type=float,
    help="Delay between detail page requests in seconds (default: 0.5)",
)
def batch_fetch_cmd(
    source: str,
    top: int,
    output_file: str,
    no_details: bool,
    delay: float,
):
    """Fetch a list of MCP servers from an online directory.

    Scrapes the mcpmarket.com leaderboard to build a servers.json file
    that can be used with `ucli batch convert`.

    \b
    Example:
      ucli batch fetch --top 50 -o servers.json
      ucli batch fetch --no-details -o servers.json
    """
    if source != "mcpmarket":
        click.echo(f"Error: unsupported source '{source}'. Only 'mcpmarket' is supported.", err=True)
        raise SystemExit(1)

    from ucli.batch.fetcher import fetch_mcpmarket_list
    from ucli.batch.models import save_batch_input

    entries = fetch_mcpmarket_list(
        top=top,
        fetch_details=not no_details,
        delay=delay,
    )

    if not entries:
        click.echo("No servers found.", err=True)
        raise SystemExit(1)

    output_path = Path(output_file)
    save_batch_input(entries, output_path)
    click.echo(f"\nWritten to {output_path}")
    click.echo(f"Review and edit the file, then run:")
    click.echo(f"  ucli batch convert --input {output_path} -o ./presets")


@batch_group.command("convert")
@click.option(
    "--input", "input_file", required=True,
    type=click.Path(exists=True),
    help="Path to servers.json (from `batch fetch` or manually created)",
)
@click.option(
    "-o", "--output", "output_dir", default="./presets",
    help="Output directory for preset bundles (default: ./presets)",
)
@click.option(
    "--skip-existing/--no-skip-existing", default=True,
    help="Skip servers that already have a preset in the output directory (default: enabled)",
)
@click.option(
    "--force", is_flag=True,
    help="Force reconvert even if preset exists (overrides --skip-existing)",
)
@click.option(
    "--concurrency", default=1, type=int,
    help="Number of parallel conversions (default: 1)",
)
def batch_convert_cmd(
    input_file: str,
    output_dir: str,
    skip_existing: bool,
    force: bool,
    concurrency: int,
):
    """Batch convert multiple MCP servers to preset bundles.

    Reads a servers.json file and for each server: scans tools via
    ephemeral npx/uvx, generates CLI mapping and skill files via AI,
    then exports the preset bundle to the output directory.

    \b
    Example:
      ucli batch convert --input servers.json -o ./presets
      ucli batch convert --input servers.json --force
      ucli batch convert --input failed.json -o ./presets
    """
    from ucli.batch.converter import batch_convert
    from ucli.batch.models import load_batch_input

    entries = load_batch_input(Path(input_file))
    click.echo(f"Loaded {len(entries)} servers from {input_file}")

    # Filter out entries without command/args
    valid = [e for e in entries if e.command and e.args]
    skipped_invalid = len(entries) - len(valid)
    if skipped_invalid:
        click.echo(f"  {skipped_invalid} entries skipped (missing command/args)")

    if not valid:
        click.echo("No valid entries to convert.", err=True)
        raise SystemExit(1)

    effective_skip = skip_existing and not force
    results = batch_convert(
        entries=valid,
        output_dir=output_dir,
        skip_existing=effective_skip,
        concurrency=concurrency,
    )

    # Exit with error if any fatal failures
    failed = [r for r in results if r.status == "failed"]
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    cli()
