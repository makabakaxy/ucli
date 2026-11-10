---
name: "bigquery-mcp"
description: Run read-only BigQuery SQL queries via CLI. Use when user needs to query BigQuery datasets, run SQL against Google BigQuery, or retrieve data from BigQuery tables.
source_version: "0.1.0"
source_cli_hash: "ec2935ab"
generated_at: "2026-04-06T09:15:59.471919+00:00"
---

# bigquery-mcp (via ucli)

Run read-only BigQuery SQL queries via CLI.

## Shortcuts

- `ucli bigquery <cmd>`

## Commands

### Query
| Command | Description | Example | Ref |
|---|---|---|---|
| `ucli bigquery query` | Run a read-only BigQuery SQL query | `ucli bigquery query --sql 'SELECT * FROM dataset.table LIMIT 10'`<br>`ucli bigquery query --sql 'SELECT COUNT(*) FROM project.dataset.table'` | [ref](reference/query.md) |

## Discover Parameters

Append `--help` to any command for full parameter list:

    ucli bigquery query --help

> **Note**: Use Ref links in the Commands table above to view detailed parameter reference and more examples.

## User Notes

> **MUST READ** [users/skill.md](users/skill.md) for custom workflows and tips.
> **Config**: MCP server settings live in `~/.agents/ucli/servers.yaml` - edit there to take effect.
