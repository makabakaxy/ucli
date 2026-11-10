"""Hierarchical command resolution with alias routing and JSON input support."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import click
import yaml

from ucli.cli.mapping import load_cli_yaml
from ucli.config.tool_store import load_tools
from ucli.constants import CLI_DIR, RESERVED_COMMANDS


@dataclass
class AliasEntry:
    """A single entry in the global alias index."""

    server: str
    yaml_path: Path
    command_prefix: list[str]
    alias_type: str  # "canonical" | "server_alias" | "shortcut"


@dataclass
class ToolResult:
    """Resolved _tool leaf for daemon-backed MCP execution."""

    server: str
    tool: str
    params: dict
    cli_yaml_path: Path


@dataclass
class ExecResult:
    """Resolved _exec leaf for local subprocess execution."""

    command: str
    args: list[str]
    exec_params: dict
    param_map: dict[str, str]
    cli_yaml_path: Path
    command_path: list[str]


ResolveResult = ToolResult | ExecResult


def build_alias_index() -> dict[str, AliasEntry]:
    """Load all cli/*.yaml and build a global alias index.

    Priority (highest first):
      1. canonical server name (filename stem)
      2. server_aliases
      3. command_shortcuts
    """
    index: dict[str, AliasEntry] = {}

    if not CLI_DIR.exists():
        return index

    yaml_files = sorted(CLI_DIR.glob("*.yaml"))
    for yf in yaml_files:
        try:
            data = yaml.safe_load(yf.read_text(encoding="utf-8"))
        except (yaml.YAMLError, OSError):
            continue
        if not isinstance(data, dict):
            continue

        server = data.get("server", yf.stem)
        if not isinstance(server, str):
            server = yf.stem

        # Canonical
        if server not in RESERVED_COMMANDS:
            _try_register(index, server, AliasEntry(
                server=server, yaml_path=yf,
                command_prefix=[], alias_type="canonical",
            ))

        # Server aliases
        for alias in data.get("server_aliases", []):
            if not isinstance(alias, str):
                continue
            if alias in RESERVED_COMMANDS:
                continue
            _try_register(index, alias, AliasEntry(
                server=server, yaml_path=yf,
                command_prefix=[], alias_type="server_alias",
            ))

        # Command shortcuts
        for shortcut in data.get("command_shortcuts", []):
            if not isinstance(shortcut, str):
                continue
            if shortcut in RESERVED_COMMANDS:
                continue
            _try_register(index, shortcut, AliasEntry(
                server=server, yaml_path=yf,
                command_prefix=[shortcut], alias_type="shortcut",
            ))

    return index


def _try_register(
    index: dict[str, AliasEntry],
    token: str,
    entry: AliasEntry,
) -> None:
    """Register an alias entry, respecting priority."""
    priority = {"canonical": 0, "server_alias": 1, "shortcut": 2}
    if token in index:
        existing = index[token]
        if priority.get(entry.alias_type, 9) >= priority.get(existing.alias_type, 9):
            click.echo(
                f"Warning: alias '{token}' for {entry.server} conflicts with "
                f"{existing.server} ({existing.alias_type}), ignored.",
                err=True,
            )
            return
    index[token] = entry


def resolve_command(tokens: list[str]) -> ResolveResult | None:
    """Resolve a token sequence into a tool or exec call.

    Returns ResolveResult or None if resolution fails.
    """
    if not tokens:
        return None

    first = tokens[0]
    index = build_alias_index()

    entry = index.get(first)
    if entry is None:
        click.echo(f"Error: unknown command '{first}'.", err=True)
        click.echo("Use `ucli --help` to see available commands.", err=True)
        return None

    data = load_cli_yaml(entry.server)
    if data is None:
        click.echo(f"Error: could not load CLI mapping for '{entry.server}'.", err=True)
        return None

    commands = data.get("commands", {})
    remaining_tokens = entry.command_prefix + tokens[1:]

    # Walk the command tree
    node = commands
    path: list[str] = []
    consumed = 0

    for i, tok in enumerate(remaining_tokens):
        if "_tool" in node or "_exec" in node:
            break
        if tok.startswith("-"):
            break
        if tok.startswith("{"):
            break

        children = {k: v for k, v in node.items()
                    if not k.startswith("_") and isinstance(v, dict)}

        if tok in children:
            node = children[tok]
            path.append(tok)
            consumed = i + 1
        else:
            # Fallback: treat remaining tokens as MCP tool name
            potential_tool = tok
            tools_json = load_tools(entry.server)
            if tools_json and potential_tool in tools_json.tool_names():
                remaining_args = remaining_tokens[i + 1:]
                params = _parse_tool_args(remaining_args, entry.server, potential_tool)
                return ToolResult(
                    server=entry.server,
                    tool=potential_tool,
                    params=params,
                    cli_yaml_path=entry.yaml_path,
                )
            click.echo(f"Error: unknown sub-command '{tok}' under {'/'.join(path) or entry.server}.", err=True)
            _show_help(node, entry.server, path)
            return None

    remaining_args = remaining_tokens[consumed:]

    has_tool = "_tool" in node
    has_exec = "_exec" in node
    if has_tool and has_exec:
        click.echo(
            f"Error: command '{'/'.join(path) or entry.server}' has both _tool and _exec.",
            err=True,
        )
        return None

    tool = node.get("_tool")
    if tool:
        params = _parse_tool_args(remaining_args, entry.server, tool)
        return ToolResult(
            server=entry.server,
            tool=tool,
            params=params,
            cli_yaml_path=entry.yaml_path,
        )

    exec_config = node.get("_exec")
    if exec_config:
        return _resolve_exec_leaf(
            exec_config=exec_config,
            remaining_args=remaining_args,
            server_name=entry.server,
            path=path,
            node=node,
            cli_yaml_path=entry.yaml_path,
        )

    # Intermediate node — show help
    _show_help(node, entry.server, path)
    return None


def _resolve_exec_leaf(
    exec_config: dict,
    remaining_args: list[str],
    server_name: str,
    path: list[str],
    node: dict,
    cli_yaml_path: Path,
) -> ExecResult | None:
    """Build an ExecResult from a resolved _exec leaf."""
    if not isinstance(exec_config, dict):
        click.echo(f"Error: invalid _exec config at {'/'.join(path)}.", err=True)
        return None

    command = exec_config.get("command")
    if not isinstance(command, str) or not command.strip():
        click.echo(f"Error: invalid _exec.command at {'/'.join(path)}.", err=True)
        return None

    fixed_args = exec_config.get("args", [])
    if fixed_args is None:
        fixed_args = []
    if not isinstance(fixed_args, list) or not all(isinstance(arg, str) for arg in fixed_args):
        click.echo(f"Error: invalid _exec.args at {'/'.join(path)}.", err=True)
        return None

    param_map = exec_config.get("params", {})
    if param_map is None:
        param_map = {}
    if not isinstance(param_map, dict) or not all(
        isinstance(key, str) and isinstance(value, str)
        for key, value in param_map.items()
    ):
        click.echo(f"Error: invalid _exec.params at {'/'.join(path)}.", err=True)
        return None

    exec_params = _parse_exec_args(
        remaining_args,
        server_name=server_name,
        path=path,
        node=node,
        exec_config=exec_config,
        param_map=param_map,
    )
    return ExecResult(
        command=command,
        args=fixed_args,
        exec_params=exec_params,
        param_map=param_map,
        cli_yaml_path=cli_yaml_path,
        command_path=path,
    )


def _parse_tool_args(
    tokens: list[str],
    server_name: str,
    tool_name: str,
) -> dict:
    """Parse remaining tokens into tool parameters.

    Supports --flag-name value and JSON positional argument.
    """
    json_params: dict = {}
    flag_params: dict = {}
    i = 0

    # Load input schema for type-aware parsing
    tools_json = load_tools(server_name)
    schema_props: dict = {}
    if tools_json:
        for t in tools_json.tools:
            if t.name == tool_name:
                schema_props = t.input_schema.get("properties", {})
                break

    while i < len(tokens):
        tok = tokens[i]

        if tok.startswith("{"):
            if json_params:
                click.echo("Error: only one JSON argument allowed.", err=True)
                raise SystemExit(1)
            try:
                json_params = json.loads(tok)
            except json.JSONDecodeError as e:
                click.echo(f"Error: invalid JSON argument: {e}", err=True)
                raise SystemExit(1)
            i += 1

        elif tok == "--help" or tok == "-h":
            _show_tool_help(server_name, tool_name)
            raise SystemExit(0)

        elif tok.startswith("--"):
            key = tok.lstrip("-")
            param_name = key.replace("-", "_")

            if i + 1 < len(tokens) and not tokens[i + 1].startswith("--"):
                raw_value = tokens[i + 1]
                i += 2
            else:
                raw_value = "true"
                i += 1

            # Auto-parse JSON for object/array schema types
            prop_schema = schema_props.get(param_name, {})
            prop_type = prop_schema.get("type", "string")
            if prop_type in ("object", "array") and raw_value not in ("true", "false"):
                try:
                    flag_params[param_name] = json.loads(raw_value)
                    continue
                except json.JSONDecodeError:
                    pass

            flag_params[param_name] = raw_value

        else:
            click.echo(f"Error: unexpected argument: {tok}", err=True)
            raise SystemExit(1)

    # Merge: flags override JSON
    return {**json_params, **flag_params}


def _parse_args(
    tokens: list[str],
    server_name: str,
    tool_name: str,
) -> dict:
    """Backward-compatible wrapper for direct MCP tool argument parsing."""
    return _parse_tool_args(tokens, server_name, tool_name)


def _parse_exec_args(
    tokens: list[str],
    *,
    server_name: str,
    path: list[str],
    node: dict,
    exec_config: dict,
    param_map: dict[str, str],
) -> dict:
    """Parse flags and positionals for an _exec leaf."""
    positionals = exec_config.get("positionals", [])
    if positionals is None:
        positionals = []
    if not isinstance(positionals, list) or not all(isinstance(p, str) for p in positionals):
        click.echo(f"Error: invalid _exec.positionals at {'/'.join(path)}.", err=True)
        raise SystemExit(1)

    flag_params: dict[str, str] = {}
    positional_values: list[str] = []
    force_next_positional = False
    i = 0

    while i < len(tokens):
        tok = tokens[i]

        if tok in ("--help", "-h"):
            _show_exec_help(server_name, path, node, exec_config)
            raise SystemExit(0)

        if force_next_positional:
            positional_values.append(tok)
            force_next_positional = False
            i += 1
            continue

        if tok == "--":
            if i + 1 >= len(tokens):
                click.echo("Error: expected positional argument after '--'.", err=True)
                _show_exec_help(server_name, path, node, exec_config)
                raise SystemExit(1)
            force_next_positional = True
            i += 1
            continue

        if tok.startswith("--"):
            key = tok[2:]
            param_name = key.replace("-", "_")
            if param_name not in param_map:
                click.echo(f"Error: unknown option '--{key}'.", err=True)
                _show_exec_help(server_name, path, node, exec_config)
                raise SystemExit(1)

            if i + 1 < len(tokens) and not tokens[i + 1].startswith("--"):
                raw_value = tokens[i + 1]
                i += 2
            else:
                raw_value = "true"
                i += 1

            flag_params[param_name] = raw_value
            continue

        if tok.startswith("-"):
            click.echo(f"Error: unexpected positional argument '{tok}'.", err=True)
            _show_exec_help(server_name, path, node, exec_config)
            raise SystemExit(1)

        positional_values.append(tok)
        i += 1

    if len(positional_values) > len(positionals):
        unexpected = positional_values[len(positionals)]
        click.echo(f"Error: unexpected positional argument '{unexpected}'.", err=True)
        _show_exec_help(server_name, path, node, exec_config)
        raise SystemExit(1)

    positional_params: dict[str, str] = {}
    for index, value in enumerate(positional_values):
        positional_params[positionals[index]] = value

    # Flags override positionals.
    return {**positional_params, **flag_params}


def _show_help(node: dict, server_name: str, path: list[str]) -> None:
    """Show help for an intermediate command node."""
    if path:
        cmd_path = f"ucli {server_name} {' '.join(path)}"
    else:
        cmd_path = f"ucli {server_name}"

    desc = node.get("_description", "")
    click.echo(f"Usage: {cmd_path} <command> [OPTIONS]")
    if desc:
        click.echo(f"\n  {desc}")

    children = {k: v for k, v in node.items()
                if not k.startswith("_") and isinstance(v, dict)}
    if children:
        click.echo("\nCommands:")
        for name, child in children.items():
            child_desc = child.get("_description", "")
            tool = child.get("_tool", "")
            exec_config = child.get("_exec")
            suffix = ""
            if tool:
                suffix = f"  → {tool}"
            elif isinstance(exec_config, dict):
                exec_command = exec_config.get("command", "")
                suffix = f"  → exec:{exec_command}" if exec_command else "  → exec"
            click.echo(f"  {name:<20} {child_desc}{suffix}")

    click.echo(f"\nRun '{cmd_path} <command> --help' for more information.")


def _show_tool_help(server_name: str, tool_name: str) -> None:
    """Show help for a leaf command (tool)."""
    tools_json = load_tools(server_name)
    if not tools_json:
        click.echo(f"No tool information available for {server_name}.")
        return

    tool = None
    for t in tools_json.tools:
        if t.name == tool_name:
            tool = t
            break

    if not tool:
        click.echo(f"Tool '{tool_name}' not found.")
        return

    click.echo(f"  {tool.description or tool_name}\n")

    props = tool.input_schema.get("properties", {})
    required = set(tool.input_schema.get("required", []))

    if props:
        click.echo("Options:")
        for pname, pschema in props.items():
            flag_name = pname.replace("_", "-")
            ptype = pschema.get("type", "")
            pdesc = pschema.get("description", "")
            req_str = "(required)" if pname in required else ""
            default = pschema.get("default")
            def_str = f" (default: {default})" if default is not None else ""
            click.echo(f"  --{flag_name:<25} {req_str:<12} {pdesc}{def_str}")

    click.echo(
        f"\nJSON Input:\n"
        f"  ucli ... '{{\"{list(props.keys())[0] if props else 'key'}\":\"value\"}}'\n"
        f"  Flags override JSON keys."
    )


def _show_exec_help(server_name: str, path: list[str], node: dict, exec_config: dict) -> None:
    """Show help for a leaf command backed by _exec."""
    cmd_path = f"ucli {server_name} {' '.join(path)}" if path else f"ucli {server_name}"
    param_map = exec_config.get("params") or {}
    positionals = exec_config.get("positionals") or []

    usage_args = " ".join(f"[{p.upper()}]" for p in positionals)
    usage = f"Usage: {cmd_path}"
    if usage_args:
        usage += f" {usage_args}"
    usage += " [OPTIONS]"
    click.echo(usage)

    desc = node.get("_description", "")
    if desc:
        click.echo(f"\n  {desc}")

    if positionals:
        click.echo("\nArguments:")
        for pname in positionals:
            flag = param_map.get(pname, "")
            suffix = f"maps to {flag}" if flag else ""
            click.echo(f"  {pname.upper():<20} {suffix}")

    option_names = [p for p in param_map if p not in positionals]
    if option_names:
        click.echo("\nOptions:")
        for pname in option_names:
            flag_name = pname.replace("_", "-")
            flag = param_map[pname]
            click.echo(f"  --{flag_name:<23} TEXT    maps to {flag} (optional)")

    examples = node.get("_examples") or []
    if examples:
        click.echo("\nExamples:")
        for example in examples:
            click.echo(f"  {example}")


def list_dynamic_commands() -> list[tuple[str, str]]:
    """Return (name, description) pairs for all registered servers."""
    if not CLI_DIR.exists():
        return []
    result = []
    for yf in sorted(CLI_DIR.glob("*.yaml")):
        try:
            data = yaml.safe_load(yf.read_text(encoding="utf-8"))
        except (yaml.YAMLError, OSError):
            continue
        if not isinstance(data, dict):
            continue
        server = data.get("server", yf.stem)
        commands = data.get("commands", {})
        groups = [k for k in commands if not k.startswith("_")]
        desc = ", ".join(groups[:3])
        if len(groups) > 3:
            desc += f", ... ({len(groups)} groups)"
        result.append((server, desc))
    return result
