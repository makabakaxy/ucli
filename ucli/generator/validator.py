"""Validation logic for CLI YAML and Skill files."""

from __future__ import annotations

import re
from pathlib import Path

import yaml

from ucli.cli.mapping import cli_path, cli_yaml_hash, extract_tools_from_yaml
from ucli.config.tool_store import load_tools
from ucli.constants import RESERVED_COMMANDS
from ucli.utils import safe_filename, skills_path
from ucli.utils.file_ops import ensure_users_dir, parse_frontmatter


# ---------------------------------------------------------------------------
# CLI YAML Validation
# ---------------------------------------------------------------------------

def validate_cli_yaml(server_name: str) -> list[str]:
    """Validate cli/<server>.yaml. Returns list of error strings (empty = valid)."""
    errors: list[str] = []
    path = cli_path(server_name)

    if not path.exists():
        return [f"CLI file not found: {path}"]

    try:
        text = path.read_text(encoding="utf-8")
        data = yaml.safe_load(text)
    except yaml.YAMLError as e:
        return [f"YAML syntax error: {e}"]

    if not isinstance(data, dict):
        return ["YAML root must be a mapping"]

    # Structure checks
    if "server" not in data:
        errors.append("Missing top-level 'server' field")
    if "commands" not in data:
        errors.append("Missing top-level 'commands' field")
        return errors

    commands = data["commands"]
    if not isinstance(commands, dict) or not commands:
        errors.append("'commands' must be a non-empty mapping")
        return errors

    # Walk the tree
    _validate_tree(commands, [], errors)

    # Tool coverage
    tools_json = load_tools(server_name)
    if tools_json:
        yaml_tools = extract_tools_from_yaml(data)
        json_tools = tools_json.tool_names()

        missing = json_tools - yaml_tools
        invalid = yaml_tools - json_tools

        if missing:
            errors.append(f"Missing tools (in JSON but not YAML): {sorted(missing)}")
        if invalid:
            errors.append(f"Invalid tools (in YAML but not JSON): {sorted(invalid)}")

        # Duplicate check
        all_tool_refs = _collect_all_tools(commands)
        seen: dict[str, int] = {}
        for t in all_tool_refs:
            seen[t] = seen.get(t, 0) + 1
        dups = [t for t, c in seen.items() if c > 1]
        if dups:
            errors.append(f"Duplicate tool mappings: {dups}")

    # Command path checks
    paths = _collect_paths(commands, [])
    path_strs = ["/".join(p) for p in paths]
    if len(path_strs) != len(set(path_strs)):
        errors.append("Duplicate command paths detected")

    for p in paths:
        if len(p) > 4:
            errors.append(f"Path depth > 4: {'/'.join(p)}")

    # Alias/shortcut conflict check
    for field_name, label in (("server_aliases", "Alias"), ("command_shortcuts", "Shortcut")):
        values = data.get(field_name, [])
        if isinstance(values, list):
            for value in values:
                if isinstance(value, str) and value in RESERVED_COMMANDS:
                    errors.append(f"{label} '{value}' conflicts with reserved command")

    return errors


def _validate_tree(node: dict, path: list[str], errors: list[str]) -> None:
    """Recursively validate command tree structure."""
    has_tool = "_tool" in node
    has_exec = "_exec" in node
    has_target = has_tool or has_exec
    children = {k: v for k, v in node.items() if not k.startswith("_") and isinstance(v, dict)}

    path_str = "/".join(path) or "<root>"

    if has_tool and has_exec:
        errors.append(f"Node at {path_str} has both _tool and _exec")

    if has_target and children:
        errors.append(f"Node at {path_str} has both a leaf target and children")

    if not has_target and not children:
        if path:
            errors.append(f"Leaf node at {'/'.join(path)} missing _tool or _exec field")

    if not has_target and "_description" not in node and path:
        errors.append(f"Intermediate node at {'/'.join(path)} missing _description")

    if has_exec:
        _validate_exec_node(node.get("_exec"), path, errors)

    for key, value in node.items():
        if key.startswith("_"):
            continue
        if not re.match(r"^[a-z][a-z0-9-]*$", key):
            errors.append(f"Invalid command name '{key}' at {'/'.join(path)} (must be lowercase, a-z0-9-)")
        if isinstance(value, dict):
            _validate_tree(value, path + [key], errors)


def _validate_exec_node(exec_node, path: list[str], errors: list[str]) -> None:
    """Validate the _exec payload at one leaf node."""
    path_str = "/".join(path) or "<root>"
    if not isinstance(exec_node, dict):
        errors.append(f"_exec at {path_str} must be a mapping")
        return

    command = exec_node.get("command")
    if not isinstance(command, str) or not command.strip():
        errors.append(f"_exec.command at {path_str} must be a non-empty string")

    args = exec_node.get("args", [])
    if args is not None:
        if not isinstance(args, list) or not all(isinstance(item, str) for item in args):
            errors.append(f"_exec.args at {path_str} must be a list of strings")

    params = exec_node.get("params", {})
    if params is not None:
        if not isinstance(params, dict) or not all(
            isinstance(key, str) and isinstance(value, str)
            for key, value in params.items()
        ):
            errors.append(f"_exec.params at {path_str} must map strings to strings")
            params = {}

    positionals = exec_node.get("positionals", [])
    if positionals is not None:
        if not isinstance(positionals, list) or not all(isinstance(item, str) for item in positionals):
            errors.append(f"_exec.positionals at {path_str} must be a list of strings")
            return
        param_keys = set(params.keys()) if isinstance(params, dict) else set()
        for positional in positionals:
            if positional not in param_keys:
                errors.append(
                    f"_exec.positionals at {path_str} references unknown param '{positional}'"
                )


def _collect_all_tools(node: dict) -> list[str]:
    tools: list[str] = []
    for key, value in node.items():
        if key == "_tool" and isinstance(value, str):
            tools.append(value)
        elif isinstance(value, dict) and not key.startswith("_"):
            tools.extend(_collect_all_tools(value))
    return tools


def _collect_paths(node: dict, prefix: list[str]) -> list[list[str]]:
    paths: list[list[str]] = []
    for key, value in node.items():
        if key.startswith("_"):
            continue
        if isinstance(value, dict):
            current = prefix + [key]
            if "_tool" in value or "_exec" in value:
                paths.append(current)
            else:
                paths.extend(_collect_paths(value, current))
    return paths


# ---------------------------------------------------------------------------
# Skill File Validation
# ---------------------------------------------------------------------------

def validate_skill(server_name: str, output_dir: Path | None = None) -> list[str]:
    """Validate skill files for a server. Returns list of error strings."""
    errors: list[str] = []
    skill_dir = output_dir or skills_path(server_name)

    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return [f"SKILL.md not found in {skill_dir}"]

    text = skill_md.read_text(encoding="utf-8")

    # Frontmatter check
    fm = parse_frontmatter(text)
    if fm is None:
        errors.append("SKILL.md missing YAML frontmatter")
    else:
        if "name" not in fm:
            errors.append("Frontmatter missing 'name'")
        elif safe_filename(fm["name"]) != safe_filename(server_name):
            errors.append(f"Frontmatter name '{fm['name']}' != server '{server_name}'")
        if not fm.get("description"):
            errors.append("Frontmatter missing or empty 'description'")
        if "source_cli_hash" not in fm:
            errors.append("Frontmatter missing 'source_cli_hash'")
        if "source_version" not in fm:
            errors.append("Frontmatter missing 'source_version'")

    # source_cli_hash freshness
    if fm and "source_cli_hash" in fm:
        current_hash = cli_yaml_hash(server_name)
        if current_hash and fm["source_cli_hash"] != current_hash:
            errors.append(
                f"source_cli_hash mismatch: skill has '{fm['source_cli_hash']}', "
                f"current CLI YAML hash is '{current_hash}'"
            )

    # Reference directory
    ref_dir = skill_dir / "reference"
    if not ref_dir.exists() or not list(ref_dir.glob("*.md")):
        errors.append("reference/ directory missing or empty")

    # Users directory (create if missing, not an error)
    ensure_users_dir(skill_dir)

    # Workflows placeholder (create if missing, not an error — LLM fills on first gen)
    workflows_md = skill_dir / "users" / "workflows.md"
    if not workflows_md.exists():
        workflows_md.write_text(
            "# Common Workflow Examples\n\n"
            "<!-- Multi-step workflow examples will be generated here on first run. -->\n"
            "<!-- This file is never overwritten by ucli generate/update. -->\n",
            encoding="utf-8",
        )

    return errors
