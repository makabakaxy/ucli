# ucli

Turn MCP servers and local scripts into CLI commands and agent skills.

The Python distribution is named `ucli-tools`. The command and Python module are named `ucli`.

ucli gives AI agents a command-line interface to the tools you already use. It discovers MCP tools, generates a hierarchical CLI, and creates skills for Codex, Claude Code, and Cursor. You can also add local scripts to the same command tree.

Use it for developer tools, project management, databases, desktop apps, or your own automation. Photoshop is one shipped integration.

## Why

An MCP server can expose many tools. Loading every tool schema into an agent's context can use a large part of its input budget before any work begins.

ucli gives the agent a skill with usage instructions and references. The agent discovers commands through help and calls the CLI, while ucli talks to the MCP server. To avoid loading both interfaces, use skill-based access with the original MCP registration disabled.

- **One backend:** reuse an MCP server instead of maintaining a separate CLI implementation.
- **Commands on demand:** explore a command tree with `--help` and load relevant skill references as needed.
- **Reusable skills:** generate once and sync to supported agent clients.
- **Local extensions:** add Python, shell, or Go helpers alongside MCP commands.
- **Repeatable installation:** use presets for existing CLI mappings and skills; shipped presets can also manage a backend runtime.

## Install

Python 3.11+ and [uv](https://docs.astral.sh/uv/) are required. The runtime uses Unix sockets; Windows support is not currently provided.

The first PyPI release of `ucli-tools` is not published yet. Once published, install it with:

```bash
uv tool install ucli-tools
```

Until then, install from this private repository with GitHub SSH access:

```bash
uv tool install 'git+ssh://git@github.com/makabakaxy/ucli.git@main'
ucli --help
```

Or install from a local checkout:

```bash
uv tool install .
```

Run `uv tool update-shell` and open a new terminal if `ucli` is not on PATH. For a reproducible installation, replace `main` with a published tag or commit.

AI discovery and generation currently use the Claude Code CLI. Install and authenticate it before generating new mappings or skills. Shipped presets such as `ps` do not require AI generation. Each MCP server may also require its own runtime, credentials, or application.

## Quick start

### Convert an existing MCP server

List servers already configured in Codex, Claude Code, or Cursor, then convert one by its configured name:

```bash
ucli mcp list
ucli mcp add mcp-atlassian
ucli mcp-atlassian --help
```

Conversion reads the server configuration, reuses a preset or generates CLI mappings and skills, then syncs the skills to detected clients. By default, skill sync disables the original MCP registration in those clients. Use `--skip-disable` to keep it enabled.

For example, with the Atlassian preset installed:

```bash
ucli mcp-atlassian jira issue search --jql 'project = DEMO'
ucli mcp-atlassian jira issue get --issue-key DEMO-123
```

Generated command names depend on the server and mapping. Use `--help` to inspect them.

### Install a new MCP server

```bash
ucli install mcp-atlassian --client codex
```

Installation checks for a shipped preset, existing local configuration, or a remote preset before falling back to AI discovery and generation. It prompts for required configuration. `--client codex,claude,cursor` selects multiple skill destinations; the default is Codex.

`ucli mcp install` is also supported. Both install forms keep existing client MCP registrations enabled. To switch fully to skill-based access, use `ucli skill sync <server> --targets <clients>` without `--skip-disable`.

### Try a shipped integration

```bash
ucli install ps
ucli ps app ping
ucli doctor ps
```

The current shipped integration is Photoshop on macOS. It installs a pinned MCP backend, CLI mappings, and a skill in one step. Photoshop and a supported Node.js version must already be installed. See the [Photoshop guide](docs/photoshop.md) for requirements, examples, and lifecycle details.

## How it works

```text
MCP configuration -> discover tools -> cli.yaml + skill files -> agent clients
                                          |
Agent -> ucli <server> <command> -> resolve mapping -> daemon -> MCP server
                                          |
                                    local script
```

The CLI mapping connects command paths to MCP tools or local helpers. MCP calls use a daemon that starts on demand and keeps server connections available. Local helpers run as subprocesses.

Configuration and generated files live under `~/.agents/ucli/`:

| Path | Contents |
| --- | --- |
| `servers.yaml` | MCP commands, arguments, and environment values |
| `tools/` | Discovered tool schemas |
| `cli/` | Command mappings |
| `skills/` | Generated skills and references |

Edit `servers.yaml` to update credentials or endpoints. If a backend is already running, use `ucli daemon reconnect <server>` to reload its connection.

| Client | Synced skill directory |
| --- | --- |
| Codex | `~/.agents/skills/<server>` |
| Claude Code | `~/.claude/skills/<server>` |
| Cursor | `~/.cursor/skills/<server>` |

Skill updates preserve custom content in `users/` and `scripts/`.

## Presets

A preset contains tool schemas, CLI mappings, and skill files. It lets you reuse generated results without running AI generation again.

From a checkout, install one of the repository's presets directly:

```bash
ucli install mcp-atlassian --preset-dir ./presets --client codex
```

Inspect or export your local generated results:

```bash
ucli preset list --local
ucli preset export mcp-atlassian
```

`ucli preset pull` and `ucli preset push` support remote preset workflows. The current download path uses public GitHub raw URLs and does not authenticate to private registries. For this private repository, use a local checkout with `--preset-dir`, or the shipped `ps` preset. Only `ps` is currently included in the Python distribution.

## Local scripts

Add a helper to a server's command tree:

```bash
ucli exec add mcp-atlassian ./scripts/report.py --command-path 'report build'
ucli exec list mcp-atlassian
ucli mcp-atlassian report build --help
```

ucli uses AI to generate the mapping and sync the skill. Python (`.py`), shell (`.sh`), and Go (`.go`) files are supported; their runtimes must be installed locally.

## Commands

| Command | Purpose |
| --- | --- |
| `ucli list` | List shipped integrations and configured MCP servers |
| `ucli mcp add <server>` | Convert an already-configured MCP server |
| `ucli install <server>` | Install or convert a server and sync its skill |
| `ucli update <server>` | Update tool schemas, CLI mappings, and skills |
| `ucli uninstall <server>` | Remove an integration; use `--dry-run` to preview |
| `ucli mcp tools <server>` | Inspect raw MCP tools |
| `ucli mcp call <server> <tool>` | Call an MCP tool directly |
| `ucli cli generate <server>` | Generate CLI mappings |
| `ucli cli validate <server>` | Validate CLI mappings against tool schemas |
| `ucli skill generate <server>` | Generate skill files |
| `ucli skill sync <server> --targets codex` | Sync skills to selected clients |
| `ucli exec add <server> <path>` | Add local script commands |
| `ucli doctor <server>` | Check a managed installation and backend readiness |
| `ucli batch fetch` / `ucli batch convert` | Prepare and process your own batch input file |

`ucli mcp install` and `ucli mcp update` are also available. Managed presets update to the version shipped with ucli; other servers use the scan and generation workflow. Managed backend installation and `doctor` currently require a preset with runtime metadata.

## Development

```bash
uv sync
uv build
uv run python -m unittest discover -s tests -v
```

Set `UCLI_USER_HOME` to a short temporary directory to isolate ucli configuration, generated files, daemon files, and skill destinations. This does not isolate third-party applications or backend state.

After upgrading ucli, let active commands finish and run `ucli daemon stop` so the next call loads the new code.

## License

MIT. Third-party MCP servers and applications have their own licenses and requirements.
