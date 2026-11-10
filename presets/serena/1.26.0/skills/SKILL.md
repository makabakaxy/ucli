---
name: serena
description: Code editing and project management via Serena MCP. Use when user needs to read/write files, find/rename symbols, run shell commands, or manage project memory.
source_version: "1.26.0"
source_cli_hash: "bc6b949c"
generated_at: "2026-04-06T08:49:26.537103+00:00"
---

# serena (via ucli)

Code-aware editing, symbol navigation, memory, and project management.

## Shortcuts

No shortcuts configured. Use `ucli serena <group> <cmd>`.

## Commands

### File
| Command | Description | Example | Ref |
|---|---|---|---|
| `ucli serena file create` | Create or overwrite a text file | `ucli serena file create --relative-path src/new.py --content 'print("hi")'` | [ref](reference/file.md) |
| `ucli serena file get` | Read a file or chunk | `ucli serena file get --relative-path src/main.py`<br>`ucli serena file get --relative-path src/main.py --start-line 10 --end-line 50` | [ref](reference/file.md) |
| `ucli serena file search` | Search regex pattern across codebase | `ucli serena file search --substring-pattern 'def my_func'` | [ref](reference/file.md) |
| `ucli serena file list` | List files in a directory | `ucli serena file list --relative-path . --recursive false` | [ref](reference/file.md) |
| `ucli serena file find` | Find files by name mask | `ucli serena file find --file-mask '*.py' --relative-path src` | [ref](reference/file.md) |
| `ucli serena file replace` | Replace pattern occurrences in a file | | [ref](reference/file.md) |

### Symbol
| Command | Description | Example | Ref |
|---|---|---|---|
| `ucli serena symbol find` | Find symbols by name path pattern | `ucli serena symbol find --name-path-pattern MyClass/my_method` | [ref](reference/symbol.md) |
| `ucli serena symbol overview` | Get high-level symbol overview of a file | `ucli serena symbol overview --relative-path src/main.py` | [ref](reference/symbol.md) |
| `ucli serena symbol replace` | Replace the body of a symbol | | [ref](reference/symbol.md) |
| `ucli serena symbol insert-after` | Insert content after a symbol | | [ref](reference/symbol.md) |
| `ucli serena symbol insert-before` | Insert content before a symbol | | [ref](reference/symbol.md) |
| `ucli serena symbol rename` | Rename a symbol codebase-wide | | [ref](reference/symbol.md) |
| `ucli serena symbol refs` | Find symbols referencing a symbol | | [ref](reference/symbol.md) |
| `ucli serena symbol delete` | Delete a symbol if unreferenced | | [ref](reference/symbol.md) |

### Memory
| Command | Description | Example | Ref |
|---|---|---|---|
| `ucli serena memory write` | Write project info to named memory | `ucli serena memory write --memory-name 'auth/logic' --content 'Auth uses JWT'` | [ref](reference/memory.md) |
| `ucli serena memory get` | Read a memory | `ucli serena memory get --memory-name 'auth/logic'` | [ref](reference/memory.md) |
| `ucli serena memory list` | List available memories | `ucli serena memory list` | [ref](reference/memory.md) |
| `ucli serena memory update` | Edit memory via pattern replacement | | [ref](reference/memory.md) |
| `ucli serena memory rename` | Rename or move a memory | | [ref](reference/memory.md) |
| `ucli serena memory delete` | Delete a memory | | [ref](reference/memory.md) |

### Shell / Project / Session
| Command | Description | Example | Ref |
|---|---|---|---|
| `ucli serena shell` | Execute a shell command | `ucli serena shell --command 'npm test'` | [ref](reference/shell.md) |
| `ucli serena project activate` | Activate a project by name or path | `ucli serena project activate --project my-project` | [ref](reference/project.md) |
| `ucli serena project onboarding` | Perform project onboarding | | [ref](reference/project.md) |
| `ucli serena session config` | Get current agent configuration | | [ref](reference/session.md) |
| `ucli serena session modes` | Switch active agent modes | `ucli serena session modes --modes '["editing","interactive"]'` | [ref](reference/session.md) |
| `ucli serena session instructions` | Get Serena Instructions Manual | | [ref](reference/session.md) |

## Discover Parameters

Append `--help` to any command for full parameter list:

    ucli serena file get --help

> **Note**: Use Ref links in the Commands table above to view detailed parameter reference and more examples.

## User Notes

> **MUST READ** [users/skill.md](users/skill.md) for custom workflows and tips.
> **Config**: MCP server settings live in `~/.agents/ucli/servers.yaml` - edit there to take effect.
