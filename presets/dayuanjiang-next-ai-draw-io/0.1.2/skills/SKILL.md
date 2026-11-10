---
name: "dayuanjiang/next-ai-draw-io"
description: Create, edit, and export draw.io diagrams via CLI with real-time browser preview. Use when user needs to create or modify diagrams, generate mxGraphModel XML, or export diagrams as PNG/SVG.
source_version: "0.1.2"
source_cli_hash: "7a303472"
generated_at: "2026-04-05T08:11:21.312972+00:00"
---

# dayuanjiang/next-ai-draw-io (via ucli)

Create and edit draw.io diagrams with real-time browser preview.

## Shortcuts

- `ucli diagram <cmd>`
- `ucli session <cmd>`
- `ucli next-ai-draw-io <cmd>`

## Commands

### Session
| Command | Description | Example | Ref |
|---|---|---|---|
| `ucli session start` | Start session and open browser preview | `ucli session start` | [ref](reference/session.md) |

### Diagram
| Command | Description | Example | Ref |
|---|---|---|---|
| `ucli diagram create` | Create a new diagram from mxGraphModel XML | `ucli diagram create --xml '<mxGraphModel>...</mxGraphModel>'` | [ref](reference/diagram.md) |
| `ucli diagram get` | Get current diagram XML from browser | `ucli diagram get` | [ref](reference/diagram.md) |
| `ucli diagram edit` | Edit diagram using ID-based cell operations | `ucli diagram edit --operations '[{"operation":"add","cell_id":"rect-1","new_xml":"..."}]'` | [ref](reference/diagram.md) |
| `ucli diagram export` | Export diagram to file (.drawio/.png/.svg) | `ucli diagram export --path ./diagram.png` | [ref](reference/diagram.md) |

## Discover Parameters

Append `--help` to any command for full parameter list:

    ucli diagram create --help

> **Note**: Use Ref links above to view detailed parameter reference and examples.

## User Notes

> **MUST READ** [users/skill.md](users/skill.md) for custom workflows and tips.
> **Config**: MCP server settings live in `~/.agents/ucli/servers.yaml` - edit there to take effect.
