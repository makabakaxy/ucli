---
name: memory-mcp
description: Manage a persistent knowledge graph with entities, relations, and observations via CLI. Use when user needs to store, retrieve, search, or update structured memory/knowledge.
source_version: "0.6.3"
source_cli_hash: "c015fc36"
generated_at: "2026-04-06T09:11:02.618250+00:00"
---

# memory-mcp (via ucli)

Manage a persistent knowledge graph: entities, relations, observations.

## Shortcuts

- `ucli memory <cmd>` (alias for `ucli memory-mcp`)

## Commands

### Entity
| Command | Description | Example | Ref |
|---|---|---|---|
| `ucli memory entity create` | Create entities in the knowledge graph | `ucli memory entity create --entities '[{"name": "Alice", "entityType": "Person", "observations": ["Engineer"]}]'` | [ref](reference/entity.md) |
| `ucli memory entity delete` | Delete entities and their relations | `ucli memory entity delete --entity-names '["Alice"]'` | [ref](reference/entity.md) |

### Relation
| Command | Description | Example | Ref |
|---|---|---|---|
| `ucli memory relation create` | Create relations between entities | `ucli memory relation create --relations '[{"from": "Alice", "to": "Bob", "relationType": "knows"}]'` | [ref](reference/relation.md) |
| `ucli memory relation delete` | Delete relations from the graph | | [ref](reference/relation.md) |

### Observation
| Command | Description | Example | Ref |
|---|---|---|---|
| `ucli memory observation add` | Add observations to existing entities | `ucli memory observation add --observations '[{"entityName": "Alice", "contents": ["Joined 2024"]}]'` | [ref](reference/observation.md) |
| `ucli memory observation delete` | Delete observations from entities | | [ref](reference/observation.md) |

### Graph & Node
| Command | Description | Example | Ref |
|---|---|---|---|
| `ucli memory graph get` | Read the entire knowledge graph | `ucli memory graph get` | [ref](reference/graph.md) |
| `ucli memory node search` | Search nodes by query | `ucli memory node search --query "Alice"` | [ref](reference/node.md) |
| `ucli memory node get` | Get specific nodes by name | `ucli memory node get --names '["Alice", "Bob"]'` | [ref](reference/node.md) |

## Discover Parameters

Append `--help` to any command for full parameter list:

    ucli memory entity create --help

> **Note**: Use Ref links in the Commands table above to view detailed parameter reference and more examples.

## User Notes

> **MUST READ** [users/skill.md](users/skill.md) for custom workflows and tips.
> **Config**: MCP server settings live in `~/.agents/ucli/servers.yaml` - edit there to take effect.
