---
name: "beads"
description: Manage issues, track dependencies, and monitor workspace progress via CLI. Use when user needs to create/list/update issues, manage blockers, claim work, or get project stats.
source_version: "3.2.0"
source_cli_hash: "07387276"
generated_at: "2026-04-06T08:53:07.680832+00:00"
---

# beads (via ucli)

Lightweight issue tracker with dependency management and workspace context.

## Shortcuts

No shortcuts defined. Base command: `ucli beads <cmd>`

## Commands

### Issue
| Command | Description | Example | Ref |
|---|---|---|---|
| `ucli beads issue create` | Create a new issue | `ucli beads issue create --title "Fix memory leak" --issue-type bug`<br>`ucli beads issue create --title "Add login" --issue-type feature --assignee alice` | [ref](reference/issue.md) |
| `ucli beads issue get` | Get detailed issue info | `ucli beads issue get --issue-id ISSUE-1` | [ref](reference/issue.md) |
| `ucli beads issue list` | List issues with filters | `ucli beads issue list --status open --assignee alice` | [ref](reference/issue.md) |
| `ucli beads issue update` | Update issue fields | `ucli beads issue update --issue-id ISSUE-1 --status in_progress` | [ref](reference/issue.md) |
| `ucli beads issue close` | Close/complete an issue | `ucli beads issue close --issue-id ISSUE-1` | [ref](reference/issue.md) |
| `ucli beads issue claim` | Atomically claim an issue for work | `ucli beads issue claim --issue-id ISSUE-1` | [ref](reference/issue.md) |
| `ucli beads issue ready` | Find issues with no blockers | `ucli beads issue ready`<br>`ucli beads issue ready --assignee alice --limit 5` | [ref](reference/issue.md) |
| `ucli beads issue blocked` | Get blocked issues | `ucli beads issue blocked` | [ref](reference/issue.md) |

### Workspace
| Command | Description | Example | Ref |
|---|---|---|---|
| `ucli beads dep` | Add dependency between issues | `ucli beads dep --issue-id ISSUE-2 --depends-on-id ISSUE-1` | [ref](reference/workspace.md) |
| `ucli beads stats` | Get issue statistics | `ucli beads stats` | [ref](reference/workspace.md) |
| `ucli beads context` | Manage workspace context | `ucli beads context --action show` | [ref](reference/workspace.md) |
| `ucli beads admin` | Admin/diagnostic operations | `ucli beads admin --action validate` | [ref](reference/workspace.md) |
| `ucli beads tool list` | List available tools | `ucli beads tool list` | [ref](reference/workspace.md) |

## Discover Parameters

Append `--help` to any command for full parameter list:

    ucli beads issue create --help

> **Note**: Use Ref links in the Commands table above to view detailed parameter reference and more examples.

## User Notes

> **MUST READ** [users/skill.md](users/skill.md) for custom workflows and tips.
> **Config**: MCP server settings live in `~/.agents/ucli/servers.yaml` - edit there to take effect.
