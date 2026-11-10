---
name: "postgres-mcp"
description: Run read-only SQL queries against a PostgreSQL database via CLI. Use when user needs to query, inspect, or retrieve data from a Postgres database.
source_version: "0.1.0"
source_cli_hash: "04fa3686"
generated_at: "2026-04-06T09:14:02.467594+00:00"
---

# postgres-mcp (via ucli)

Run read-only SQL queries against a PostgreSQL database.

## Shortcuts

- `ucli postgres <cmd>` (alias for `ucli postgres-mcp`)

## Commands

### Query
| Command | Description | Example | Ref |
|---|---|---|---|
| `ucli postgres query` | Run a read-only SQL query | `ucli postgres query --sql 'SELECT * FROM users LIMIT 10'`<br>`ucli postgres query --sql 'SELECT table_name FROM information_schema.tables WHERE table_schema='"'"'public'"'"''` | [ref](reference/query.md) |

## Discover Parameters

Append `--help` to any command for full parameter list:

    ucli postgres query --help

> **Note**: Use Ref links in the Commands table above to view detailed parameter reference and more examples.

## User Notes

> **MUST READ** [users/skill.md](users/skill.md) for custom workflows and tips.
> **Config**: MCP server settings live in `~/.agents/ucli/servers.yaml` - edit there to take effect.
