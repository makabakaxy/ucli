# ucli

Install tools for AI agents. Each tool includes CLI commands, a skill, and an MCP backend.

```bash
ucli list
ucli install ps
ucli ps app ping
ucli doctor ps
ucli update ps --yes
ucli uninstall ps
```

## Install ucli

Python 3.11+ is required. Use an isolated tool environment with [uv](https://docs.astral.sh/uv/).

From a local checkout:

```bash
uv tool install .
ucli install ps
```

For a private GitHub release, after the repository and tag have been published:

```bash
uv tool install 'git+ssh://git@github.com/makabakaxy/ucli.git@v1.1.0' && ucli install ps
```

This example requires access to that private repository, GitHub SSH authentication, uv, and uv's tool directory on PATH. The repository and tag must exist before using it. Run `uv tool update-shell` if the tool directory is not on PATH, then open a new terminal. A successful wheel build alone does not publish a release.

The ps preset ships inside the Python package. Installing it does not access a private raw-content registry, run AI search, or generate commands with an LLM. Python and npm dependency downloads still need network access on the first installation.

## Photoshop

The initial shipped tool supports macOS. Install Adobe Photoshop and Node.js with npm first. The preset accepts Node.js 22, 24, and 26; Node.js 24 is recommended for new installations. Native npm dependencies may need a compiler when a prebuilt binary is unavailable. The installer does not install Photoshop, Node.js, or Adobe accounts.

```bash
ucli install ps                         # Default client: Codex
ucli install ps --client claude,cursor  # Select additional clients
ucli install ps --env PHOTOSHOP_PATH='/Applications/Adobe Photoshop 2026/Adobe Photoshop 2026.app'
ucli doctor ps
```

Installation:

1. Validate the shipped CLI, tool schema, and file checksums.
2. Install `@alisaitteke/photoshop-mcp@1.7.37` with its committed npm lockfile in a private runtime directory.
3. Start the MCP backend and check that all 128 mapped tools exist.
4. Write ucli configuration and copy the skill to the selected clients. Restore touched files if this step fails.
5. Check Photoshop connectivity and report whether the application is ready.

The installer calls the backend through an absolute Node path and a local JS entrypoint. Normal CLI use does not run `npx` or download a package. Backend analytics, feedback nudges, and update checks are disabled by default.

Photoshop must be open for the readiness check. macOS may ask for Automation permission. Installation can succeed while Photoshop is not ready; `ucli doctor ps` exits nonzero until its checks pass. Neural Filters also require the upstream UXP bridge plugin loaded in Photoshop. Generative features depend on Photoshop capabilities and the Adobe account. See the [upstream development guide](https://github.com/alisaitteke/photoshop-mcp/blob/v1.7.37/docs/development.md).

```bash
ucli ps document create --width 1920 --height 1080
ucli ps layer list
ucli ps text create --text 'Hello' --fontSize 48
ucli ps document export --help
```

The Photoshop preset allows 700 seconds per CLI request. Override this with `UCLI_TIMEOUT=900 ucli ps ...`. A timed-out edit may still be running. Inspect Photoshop before retrying; ucli does not automatically retry edits.

## Skills and configuration

| Client | Skill directory |
| --- | --- |
| Codex | `~/.agents/skills/ps` |
| Claude Code | `~/.claude/skills/ps` |
| Cursor | `~/.cursor/skills/ps` |

MCP configuration is stored in `~/.agents/ucli/servers.yaml`. The agent uses `ucli ps ...`, and ucli starts the MCP backend. Installing a shipped tool does not register or disable MCP servers in client configuration files.

User notes in `users/` and local helpers in `scripts/` are preserved. Managed skill files are replaced on update. Newly selected clients are added to the existing installation.

If ps already exists from an earlier conversion, the installer stops instead of replacing it silently. Back up any edits to generated files, then adopt it with:

```bash
ucli install ps --force
```

The installer preserves existing backend environment variables when adopting an installation. `--env KEY=VALUE` overrides a value. Do not include credentials in a published preset.

## Update and uninstall

```bash
ucli update ps --dry-run
ucli update ps --yes
ucli uninstall ps --dry-run
ucli uninstall ps --force
```

`update ps` installs the preset shipped with the currently installed ucli version. It does not follow npm's latest release or regenerate the skill. Upgrade ucli to a newer Git tag or wheel first to receive a new shipped preset. Runtime dependencies are reused when the lockfile and Node ABI match.

An update refuses to overwrite edited managed files or configuration. Use `ucli install ps --force` after reviewing those edits. Configuration and skills are restored on an exception during installation. This is rollback for handled failures, not recovery from power loss or `SIGKILL`.

Uninstall removes the recorded generated files, ps configuration, and managed backend. User notes and modified files are kept. If the ps configuration was edited, use `--keep-config` to keep both the configuration and its runtime. Other tools and client MCP settings are not changed.

If ucli itself is upgraded while its daemon is running, wait for active commands to finish and run `ucli daemon stop` before the next tool call so the daemon loads the new code.

## Other MCP servers

Existing discovery, generation, and conversion workflows remain available:

```bash
ucli mcp list
ucli mcp add existing-server --skip-disable
ucli install other-server --client codex
ucli mcp scan existing-server
ucli mcp tools existing-server
ucli mcp call existing-server tool_name --help
ucli cli generate existing-server
ucli cli validate existing-server
ucli skill generate existing-server
ucli skill sync existing-server --targets codex --skip-disable
```

For tools without a shipped preset, installation uses the existing preset or AI discovery flow. That flow may require an AI CLI and interactive configuration. `ucli mcp install` and `ucli mcp update` remain available as aliases. The managed backend lifecycle described above currently applies to shipped presets with runtime metadata.

Maintainer commands are also available under `ucli preset`, `ucli exec`, and `ucli batch`. The legacy remote preset reader supports public GitHub raw URLs; private preset registries are not required or implemented for the shipped ps workflow.

## Development and verification

```bash
uv lock
uv build
python -m unittest discover -s tests -v
```

`presets/ps/1.7.37/` is the source for the shipped ps files. Hatch includes it as `ucli/_presets/ps/` in the wheel. Both the source distribution and wheel contain the npm lockfile and skill references. Update the manifest checksums whenever a preset file changes.

Use `UCLI_USER_HOME` to redirect all ucli configuration, generated files, daemon files, and client skill destinations for an isolated smoke run:

```bash
UCLI_USER_HOME=/tmp/ucli-smoke ucli install ps
UCLI_USER_HOME=/tmp/ucli-smoke ucli doctor ps
UCLI_USER_HOME=/tmp/ucli-smoke ucli uninstall ps --force
```

This setting does not isolate Photoshop itself or third-party backend state. Keep the path short because the daemon uses a Unix socket.

## License

MIT. The Photoshop backend is a separate upstream project with its own license and notices. ucli installs it from npm; it does not include Adobe Photoshop.
