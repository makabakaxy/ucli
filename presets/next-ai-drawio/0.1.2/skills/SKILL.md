---
name: "next-ai-drawio"
description: Create, edit, and export draw.io diagrams via CLI with real-time browser preview. Use when user needs to create flowcharts, diagrams, or edit mxGraphModel XML diagrams.
source_version: "0.1.2"
source_cli_hash: "43de5f35"
generated_at: "2026-04-06T08:44:27.228580+00:00"
---

# next-ai-drawio (via ucli)

Create and manage draw.io diagrams via CLI with live browser preview.

## Shortcuts

- `ucli drawio <cmd>` (alias for `next-ai-drawio`)

## Commands

### Session
| Command | Description | Example | Ref |
|---|---|---|---|
| `ucli drawio session start` | Start diagram session and open browser for live preview | `ucli drawio session start` | [ref](reference/session.md) |

### Diagram
| Command | Description | Example | Ref |
|---|---|---|---|
| `ucli drawio diagram create` | Create a new diagram from mxGraphModel XML | `ucli drawio diagram create --xml '<mxGraphModel>...</mxGraphModel>'` | [ref](reference/diagram.md) |
| `ucli drawio diagram get` | Get the current diagram XML from browser | `ucli drawio diagram get` | [ref](reference/diagram.md) |
| `ucli drawio diagram edit` | Edit diagram by ID-based cell operations (add/update/delete) | | [ref](reference/diagram.md) |
| `ucli drawio diagram export` | Export diagram to file (.drawio/.png/.svg) | `ucli drawio diagram export --path ./diagram.png` | [ref](reference/diagram.md) |

## Discover Parameters

Append `--help` to any command for full parameter list:

    ucli drawio diagram create --help

> **Note**: Use Ref links in the Commands table above to view detailed parameter reference and more examples.

## User Notes

> **MUST READ** [users/skill.md](users/skill.md) for custom workflows and tips.
> **Config**: MCP server settings live in `~/.agents/ucli/servers.yaml` - edit there to take effect.
