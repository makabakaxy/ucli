"""Manage local file-backed _exec command mappings."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import click

from ucli.cli.mapping import cli_path, load_cli_yaml, save_cli_yaml
from ucli.constants import RESERVED_COMMANDS
from ucli.generator.llm_backend import ClaudeCLIBackend, get_backend
from ucli.generator.validator import validate_cli_yaml

MAX_RETRIES = 2

SUPPORTED_EXEC_SUFFIXES = {
    ".go": ("go", ["run"]),
    ".py": ("python", []),
    ".sh": ("bash", []),
}


@dataclass
class ExecSourceFile:
    """A source file that can become an _exec leaf."""

    path: Path
    display_path: str
    command: str
    args: list[str]
    content: str


def add_exec(
    server_name: str,
    target_path: str | Path,
    *,
    command_path: str | None = None,
    sync: bool = True,
) -> bool:
    """Generate or merge _exec leaves into cli/<server>.yaml via the LLM backend."""
    files = _discover_exec_files(target_path)
    if not files:
        return False

    if command_path and len(files) != 1:
        click.echo("Error: --command-path can only be used with a single file.", err=True)
        return False

    backend = get_backend()
    command_name = "exec add"

    existing_session = backend.find_session(command_name, server_name)
    if existing_session:
        if click.confirm("Found unfinished session. Resume?", default=True):
            result = backend.resume(
                existing_session,
                _build_resume_prompt(server_name),
                show_progress=True,
                progress_message=f"Resuming exec mapping for {server_name}...",
            )
            if not result.is_error:
                return _post_validate(server_name, backend, result.session_id, command_name, files, sync)

    prompt = _build_exec_add_prompt(server_name, files, command_path)
    result = backend.invoke(
        prompt,
        command_name=command_name,
        server_name=server_name,
        show_progress=True,
        progress_message=f"Generating _exec mapping for {server_name}...",
    )

    if result.is_error:
        click.echo(f"LLM error: {result.result}", err=True)
        return False

    return _post_validate(server_name, backend, result.session_id, command_name, files, sync)


def list_exec(server_name: str) -> bool:
    """Print all _exec leaves for a server."""
    data = load_cli_yaml(server_name)
    if data is None:
        click.echo(f"Error: cli/{server_name}.yaml not found.", err=True)
        return False

    entries = _collect_exec_entries(data)
    if not entries:
        click.echo(f"No _exec commands found for {server_name}.")
        return True

    command_width = max(len("COMMAND PATH"), *(len(e[0]) for e in entries))
    exec_width = max(len("EXEC"), *(len(e[1]) for e in entries))

    click.echo(f"{'COMMAND PATH':<{command_width}}  {'EXEC':<{exec_width}}  DESCRIPTION")
    for command, exec_display, description in entries:
        click.echo(f"{command:<{command_width}}  {exec_display:<{exec_width}}  {description}")
    return True


def remove_exec(server_name: str, command_path: str, *, sync: bool = True) -> bool:
    """Remove one _exec leaf from cli/<server>.yaml and prune empty parents."""
    data = load_cli_yaml(server_name)
    if data is None:
        click.echo(f"Error: cli/{server_name}.yaml not found.", err=True)
        return False

    parts = _split_command_path(command_path)
    if not parts:
        click.echo("Error: --command-path cannot be empty.", err=True)
        return False

    commands = data.get("commands")
    if not isinstance(commands, dict):
        click.echo(f"Error: cli/{server_name}.yaml has no commands mapping.", err=True)
        return False

    node = commands
    stack: list[tuple[dict, str]] = []
    for part in parts[:-1]:
        child = node.get(part)
        if not isinstance(child, dict):
            click.echo(f"Error: command path not found: {'/'.join(parts)}", err=True)
            return False
        stack.append((node, part))
        node = child

    leaf_key = parts[-1]
    leaf = node.get(leaf_key)
    if not isinstance(leaf, dict):
        click.echo(f"Error: command path not found: {'/'.join(parts)}", err=True)
        return False

    if "_exec" not in leaf:
        click.echo(f"Error: {'/'.join(parts)} is not an _exec command.", err=True)
        return False

    if "_tool" in leaf:
        click.echo(f"Error: {'/'.join(parts)} also has _tool and cannot be removed as _exec.", err=True)
        return False

    del node[leaf_key]
    _prune_empty_parents(stack)

    output_path = save_cli_yaml(server_name, data)
    click.echo(f"✓ cli/{output_path.name} updated ({'/'.join(parts)} removed)")
    return _sync_or_print_next_step(server_name, sync)


def _discover_exec_files(target_path: str | Path) -> list[ExecSourceFile]:
    path = Path(target_path).expanduser()
    if not path.exists():
        click.echo(f"Error: path not found: {target_path}", err=True)
        return []

    if path.is_file():
        candidates = [path]
    elif path.is_dir():
        candidates = sorted(
            child for child in path.iterdir()
            if child.is_file() and child.suffix in SUPPORTED_EXEC_SUFFIXES
        )
    else:
        click.echo(f"Error: path is not a file or directory: {target_path}", err=True)
        return []

    unsupported = [p for p in candidates if p.suffix not in SUPPORTED_EXEC_SUFFIXES]
    if unsupported:
        click.echo(
            "Error: unsupported file type. Supported suffixes: .go, .py, .sh",
            err=True,
        )
        return []

    if not candidates:
        click.echo("Error: no .go, .py, or .sh files found.", err=True)
        return []

    files: list[ExecSourceFile] = []
    for candidate in candidates:
        command, fixed_prefix = SUPPORTED_EXEC_SUFFIXES[candidate.suffix]
        display_path = _display_path(candidate)
        content = _read_text(candidate)
        files.append(
            ExecSourceFile(
                path=candidate,
                display_path=display_path,
                command=command,
                args=[*fixed_prefix, display_path],
                content=content,
            )
        )
    return files


def _post_validate(
    server_name: str,
    backend: ClaudeCLIBackend,
    session_id: str | None,
    command_name: str,
    files: list[ExecSourceFile],
    sync: bool,
) -> bool:
    for attempt in range(1, MAX_RETRIES + 1):
        errors = validate_cli_yaml(server_name)
        if not errors:
            backend.clear_session(command_name, server_name)
            _print_add_summary(server_name, files)
            return _sync_or_print_next_step(server_name, sync)

        click.echo(f"Program validation failed (attempt {attempt}/{MAX_RETRIES}):")
        for error in errors:
            click.echo(f"  - {error}")

        if attempt >= MAX_RETRIES or session_id is None:
            click.echo("Validation failed. Please fix manually or re-run.", err=True)
            return False

        result = backend.resume(
            session_id,
            _build_retry_prompt(server_name, errors),
            show_progress=True,
            progress_message="Fixing _exec validation errors...",
        )
        if result.is_error:
            click.echo(f"LLM retry error: {result.result}", err=True)
            return False

    return False


def _build_exec_add_prompt(
    server_name: str,
    files: list[ExecSourceFile],
    command_path: str | None,
) -> str:
    output_path = cli_path(server_name)
    existing_mode = output_path.exists()
    existing_text = (
        f"The existing CLI YAML is at {output_path}. Read it and preserve all existing _tool and _exec leaves."
        if existing_mode
        else "No CLI YAML exists yet. Create a complete new CLI YAML file."
    )
    command_path_text = (
        f"Use this exact command path for the file: {command_path}."
        if command_path
        else "Infer a command path for each file from its filename, comments, flags, and code content."
    )
    file_blocks = "\n\n".join(_format_file_for_prompt(file) for file in files)
    reserved = ", ".join(sorted(RESERVED_COMMANDS))
    generated_at = datetime.now(timezone.utc).isoformat()

    return (
        "You are adding local file execution leaves to a ucli command tree.\n\n"
        f"Target server: {server_name}\n"
        f"Output file: {output_path}\n"
        f"Current time: {generated_at}\n\n"
        f"{existing_text}\n"
        f"{command_path_text}\n\n"
        "Source files and default execution settings:\n\n"
        f"{file_blocks}\n\n"
        "Write a complete YAML mapping to the output file. Requirements:\n"
        "- Use the existing cli.yaml structure if present; preserve existing aliases, descriptions, _tool leaves, _exec leaves, and examples unless they are the specific leaf being added or replaced.\n"
        "- If no cli.yaml exists, create top-level fields: server, version, generated_at, generated_by, server_aliases, command_shortcuts, commands.\n"
        "- Use generated_by: ai-exec for a new file, or ai-exec-merge when merging into an existing file.\n"
        "- _tool and _exec are mutually exclusive on a leaf.\n"
        "- For each _exec, use exactly the default command and args shown above.\n"
        "- Infer _exec.params from each program's flag definitions. Parameter keys must be snake_case; parameter values are the underlying program flags such as -text or --text.\n"
        "- Infer _exec.positionals only for natural positional arguments. Every positional name must exist in _exec.params.\n"
        "- Add concise English _description fields and useful _examples when obvious.\n"
        f"- Do not generate server_aliases or command_shortcuts that conflict with reserved commands: {reserved}.\n"
        "- Do not write or modify tools.json or skill files.\n"
        "- Only write the requested YAML file. ucli will validate it after you finish; do not run shell commands.\n"
        "- Output only a short completion summary after the file is written.\n"
    )


def _format_file_for_prompt(file: ExecSourceFile) -> str:
    suffix = file.path.suffix.lstrip(".")
    args_repr = "[" + ", ".join(repr(arg) for arg in file.args) + "]"
    return (
        f"File: {file.path}\n"
        f"Default command: {file.command}\n"
        f"Default args: {args_repr}\n"
        f"Content:\n"
        f"```{suffix}\n"
        f"{file.content}\n"
        f"```"
    )


def _build_retry_prompt(server_name: str, errors: list[str]) -> str:
    output_path = cli_path(server_name)
    error_text = "\n".join(f"- {error}" for error in errors)
    return (
        f"The YAML written to {output_path} has these validation errors:\n\n"
        f"{error_text}\n\n"
        f"Fix only those issues and rewrite {output_path}. ucli will validate it after you finish; do not run shell commands.\n"
        "Keep all correct existing mappings unchanged."
    )


def _build_resume_prompt(server_name: str) -> str:
    return (
        "Continue the unfinished _exec mapping task.\n"
        f"Target server: {server_name}\n"
        "Only write the requested YAML file. ucli will validate it after you finish; do not run shell commands."
    )


def _print_add_summary(server_name: str, files: list[ExecSourceFile]) -> None:
    output_path = cli_path(server_name)
    entries = _collect_exec_entries(load_cli_yaml(server_name) or {})
    changed = _find_entries_for_files(entries, files)
    if len(changed) == 1:
        suffix = f"{changed[0]} added"
    elif changed:
        suffix = f"{len(changed)} exec commands added"
    else:
        suffix = f"{len(files)} file(s) processed"

    click.echo(f"✓ cli/{output_path.name} updated ({suffix})")


def _sync_or_print_next_step(server_name: str, sync: bool) -> bool:
    if sync:
        return _refresh_skill(server_name)

    click.echo("  Skill is now out of sync. Run:")
    click.echo(f"    ucli skill generate {server_name}")
    click.echo(f"    ucli skill sync {server_name} --skip-disable")
    click.echo("  to update and sync SKILL.md.")
    return True


def _refresh_skill(server_name: str) -> bool:
    click.echo("Refreshing generated skill files...")

    from ucli.generator.skill_gen import generate_skill
    from ucli.installer.skill_sync import skill_sync

    if not generate_skill(server_name):
        click.echo(f"Error: failed to generate skill files for {server_name}.", err=True)
        click.echo(f"Retry: ucli skill generate {server_name}", err=True)
        return False

    if not skill_sync(server_name, skip_disable=True):
        click.echo(f"Error: failed to sync skill files for {server_name}.", err=True)
        click.echo(f"Retry: ucli skill sync {server_name} --skip-disable", err=True)
        return False

    return True


def _find_entries_for_files(
    entries: list[tuple[str, str, str]],
    files: list[ExecSourceFile],
) -> list[str]:
    result: list[str] = []
    display_paths = {file.display_path for file in files}
    real_paths = {str(file.path) for file in files}
    for command_path, exec_display, _ in entries:
        if any(path in exec_display for path in display_paths | real_paths):
            result.append(command_path)
    return result


def _collect_exec_entries(data: dict) -> list[tuple[str, str, str]]:
    entries: list[tuple[str, str, str]] = []
    commands = data.get("commands", {})
    if not isinstance(commands, dict):
        return entries

    def _walk(node: dict, path: list[str]) -> None:
        exec_config = node.get("_exec")
        if isinstance(exec_config, dict):
            command = exec_config.get("command", "")
            args = exec_config.get("args") or []
            arg_text = " ".join(str(arg) for arg in args)
            exec_display = f"{command} {arg_text}".strip()
            entries.append(("/".join(path), exec_display, node.get("_description", "")))
            return

        for key, value in node.items():
            if key.startswith("_") or not isinstance(value, dict):
                continue
            _walk(value, path + [key])

    _walk(commands, [])
    return entries


def _prune_empty_parents(stack: list[tuple[dict, str]]) -> None:
    for parent, key in reversed(stack):
        child = parent.get(key)
        if isinstance(child, dict) and _is_empty_command_node(child):
            del parent[key]
        else:
            break


def _is_empty_command_node(node: dict) -> bool:
    if "_tool" in node or "_exec" in node:
        return False
    return not any(
        isinstance(value, dict) and not key.startswith("_")
        for key, value in node.items()
    )


def _split_command_path(command_path: str) -> list[str]:
    if "/" in command_path:
        raw = command_path.replace("/", " ")
    else:
        raw = command_path
    return [part for part in raw.split() if part]


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def _display_path(path: Path) -> str:
    home = Path.home()
    try:
        return f"~/{path.resolve().relative_to(home).as_posix()}"
    except ValueError:
        return str(path)
