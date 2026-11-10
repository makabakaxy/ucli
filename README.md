# ucli

Turn MCP servers and local scripts into CLI commands and agent skills for Codex, Claude Code, and Cursor.

## Why

MCP servers can expose dozens or hundreds of tools. Loading all their schemas into an agent's context takes space before the agent starts working. ucli lets the agent read a compact skill, explore commands with `--help`, and call the tools it needs.

- **Less context overhead:** use skills and CLI commands instead of loading the full MCP tool catalog. Disable the client's direct MCP registration to avoid loading both interfaces.
- **One backend to maintain:** generate the CLI from an MCP server, then refresh its mappings when tools change.
- **Skills included:** sync usage instructions and references to Codex, Claude Code, and Cursor. Add local scripts for your own workflows.

## Install

Requires Python 3.11+ and macOS or Linux.

```bash
uv tool install ucli-tools
# Or: pip install ucli-tools
```

The package name is `ucli-tools`; the command is `ucli`. AI discovery and generation require an installed, authenticated Claude Code CLI. Each MCP server may need its own runtime and credentials.

## Quick start

Try Photoshop as a concrete example. On macOS, open Photoshop and install Node.js 22, 24, or 26, then run:

```bash
# Install the Photoshop backend, CLI commands, and agent skill
ucli install ps

# Check the connection
ucli ps app ping

# Create a 1920 x 1080 document and list its layers
ucli ps document create --width 1920 --height 1080
ucli ps layer list
```

`ps` is the CLI name for Photoshop. ucli translates these commands into calls to the Photoshop MCP server. The skill is installed for Codex by default; use `--client codex,claude,cursor` to select multiple clients.

The Photoshop preset is included, so this example needs no AI generation. Use `ucli ps --help` to explore more commands or `ucli doctor ps` to check the installation. Details are in [the Photoshop guide](docs/photoshop.md).

## Use another MCP server

To convert a server already configured in your agent client:

```bash
ucli mcp list
ucli mcp add mcp-atlassian
```

The Atlassian preset provides short commands for Jira and Confluence:

```bash
ucli jira issue search --jql 'project = DEMO'
ucli jira issue get --issue-key DEMO-123
```

`mcp-atlassian` identifies the backend during setup; `jira` is a command shortcut for everyday use. Names and shortcuts come from each server's CLI mapping.

Conversion syncs skills to detected clients and disables the original MCP registration. Add `--skip-disable` to keep it enabled.

For a new server, run `ucli install mcp-atlassian --client codex`. `ucli mcp install` does the same thing; both keep existing client MCP registrations enabled.

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
