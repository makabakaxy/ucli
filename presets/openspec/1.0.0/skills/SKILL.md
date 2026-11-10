---
name: openspec
description: Manage OpenSpec change lifecycle and project specs via CLI. Use when user needs to create/archive changes, check artifact status, validate proposals, or browse specs.
source_version: "1.0.0"
source_cli_hash: "9c6172a4"
generated_at: "2026-04-06T08:22:31.209231+00:00"
---

# openspec (via ucli)

Manage OpenSpec change lifecycle — create, track, validate, and archive spec changes.

## Shortcuts

No shortcuts configured. Use: `ucli openspec <group> <cmd>`

## Commands

### project
| Command | Description | Example | Ref |
|---|---|---|---|
| `ucli openspec project init` | Initialize OpenSpec in your project | `ucli openspec project init` | [ref](reference/project.md) |
| `ucli openspec project update` | Update OpenSpec instruction files | `ucli openspec project update` | [ref](reference/project.md) |
| `ucli openspec project refresh-cache` | Force refresh the cached directory listing | `ucli openspec project refresh-cache` | [ref](reference/project.md) |

### change
| Command | Description | Example | Ref |
|---|---|---|---|
| `ucli openspec change create` | Create a new change directory | `ucli openspec change create --name add-dark-mode --description "Add dark mode support"` | [ref](reference/change.md) |
| `ucli openspec change status` | Display artifact completion status | `ucli openspec change status --change-name add-dark-mode` | [ref](reference/change.md) |
| `ucli openspec change instructions` | Output enriched instructions for an artifact | `ucli openspec change instructions --artifact design.md --change-name add-dark-mode` | [ref](reference/change.md) |
| `ucli openspec change archive` | Archive a completed change and update main specs | `ucli openspec change archive --change-name add-dark-mode` | [ref](reference/change.md) |

### content
| Command | Description | Example | Ref |
|---|---|---|---|
| `ucli openspec content list` | List changes or specs | `ucli openspec content list`<br>`ucli openspec content list --specs` | [ref](reference/content.md) |
| `ucli openspec content show` | Show details of a change or spec | `ucli openspec content show --item-name add-dark-mode` | [ref](reference/content.md) |
| `ucli openspec content read-file` | Read any OpenSpec artifact file directly | `ucli openspec content read-file --name add-dark-mode --file-type design.md` | [ref](reference/content.md) |
| `ucli openspec content validate` | Validate a change proposal or spec | `ucli openspec content validate --item-name add-dark-mode` | [ref](reference/content.md) |

## Discover Parameters

Append `--help` to any command for full parameter list:

    ucli openspec change create --help

> **Note**: Use Ref links in the Commands table above to view detailed parameter reference and more examples.

## User Notes

> **MUST READ** [users/skill.md](users/skill.md) for custom workflows and tips.
> **Config**: MCP server settings live in `~/.agents/ucli/servers.yaml` - edit there to take effect.
