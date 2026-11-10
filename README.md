# ucli

Turn MCP servers and local scripts into CLI commands and agent skills for Codex, Claude Code, and Cursor.

Instead of loading every MCP tool schema into an agent's context, ucli gives it a skill and commands it can explore with `--help`. The MCP server remains the backend.

## Install

Requires Python 3.11+ and macOS or Linux.

```bash
uv tool install ucli-tools
# Or: pip install ucli-tools
```

The package name is `ucli-tools`; the command is `ucli`. AI discovery and generation require an installed, authenticated Claude Code CLI. Each MCP server may need its own runtime and credentials.

Only install trusted servers, presets, and scripts: they run with your account's permissions. AI generation uses limited tools by default. `UCLI_UNSAFE_AI=1` explicitly bypasses AI permission checks; it is not needed for normal use.

## Quick start

Convert a server already configured in your agent client:

```bash
ucli mcp list
ucli mcp add mcp-atlassian
ucli mcp-atlassian --help
ucli mcp-atlassian jira issue search --jql 'project = DEMO'
```

Conversion generates or reuses CLI mappings and skills, syncs them to detected clients, and disables the original MCP registration. Add `--skip-disable` to keep it enabled. Commands depend on the server's mapping.

Install a new server:

```bash
ucli install mcp-atlassian --client codex
```

`ucli mcp install` does the same thing. Installation keeps existing client MCP registrations enabled. Use `--client codex,claude,cursor` to sync to multiple clients.

## Photoshop example

Photoshop is one shipped integration. On macOS, with Photoshop open and Node.js 22, 24, or 26 installed:

```bash
ucli install ps
ucli ps app ping
ucli ps document create --width 1920 --height 1080
ucli doctor ps
```

This installs a pinned MCP backend and a ready-made CLI and skill without AI generation. See `docs/photoshop.md` in the source package for more details.

## Common commands

| Command | Purpose |
| --- | --- |
| `ucli list` | List shipped integrations and configured servers |
| `ucli update <server>` | Update tools, CLI mappings, and skills |
| `ucli uninstall <server> --dry-run` | Preview removal |
| `ucli mcp tools <server>` | Inspect MCP tools |
| `ucli skill sync <server> --targets codex` | Sync skills and disable the client's original MCP registration |
| `ucli exec add <server> ./report.py --command-path 'report build'` | Add a local Python, shell, or Go helper |

Run `ucli --help` or add `--help` to a command for more options.

Configuration lives in `~/.agents/ucli/servers.yaml`. Skills sync to each client's skill directory; updates preserve your `users/` and `scripts/` content. After changing a running server's configuration, run `ucli daemon reconnect <server>`.

Presets reuse generated CLI mappings and skills. Only `ps` is currently shipped in the Python package. From a repository checkout, use `ucli install <server> --preset-dir ./presets` for other included presets. Remote preset downloads currently require a public GitHub registry.

## Development

```bash
uv sync
uv build
uv run python -m unittest discover -s tests -v
```

`UCLI_USER_HOME` redirects ucli's configuration and skill destinations for isolated development. It does not isolate third-party apps or backends.

## License

MIT. MCP servers and third-party applications have their own licenses and requirements.
