---
name: mcp-atlassian
description: Manage JIRA issues, sprints, boards, and Confluence pages via CLI. Use when user needs to create/search/update JIRA tickets, manage sprints, or edit Confluence pages.
source_version: "null"
source_cli_hash: "7c573e11"
generated_at: "2026-04-03T10:56:14.617163+00:00"
---

# mcp-atlassian (via ucli)

Manage JIRA and Confluence via CLI.

## Shortcuts

| Alias | Expands to |
|---|---|
| `ucli jira` | `ucli mcp-atlassian jira` |
| `ucli confluence` | `ucli mcp-atlassian confluence` |
| `ucli atlassian` | `ucli mcp-atlassian` |

## Commands

### JIRA
| Command | Description | Example | Ref |
|---|---|---|---|
| `ucli jira issue create` | Create a new issue | `ucli jira issue create --project-key INFRA --summary "Fix bug" --issue-type Task`<br>`ucli jira issue create --project-key DEV --summary "Add login" --issue-type Story --assignee john@example.com` | [ref](reference/jira-issue.md) |
| `ucli jira issue get` | Get issue details | `ucli jira issue get --issue-key INFRA-1234` | [ref](reference/jira-issue.md) |
| `ucli jira issue search` | Search issues via JQL | `ucli jira issue search --jql "project=INFRA AND status=Open"` | [ref](reference/jira-issue.md) |
| `ucli jira issue update` | Update an issue | `ucli jira issue update --issue-key INFRA-1234 --fields '{"summary":"New title"}'` | [ref](reference/jira-issue.md) |
| `ucli jira issue transition` | Change issue status | `ucli jira issue transition --issue-key INFRA-1234 --transition-id 31` | [ref](reference/jira-issue.md) |
| `ucli jira sprint create` | Create a sprint | `ucli jira sprint create --board-id 42 --name "Sprint 1" --start-date 2026-04-01 --end-date 2026-04-14` | [ref](reference/jira-sprint.md) |
| `ucli jira board list` | List agile boards | `ucli jira board list --project-key INFRA` | [ref](reference/jira-board.md) |
| `ucli jira project list` | List all projects | `ucli jira project list` | [ref](reference/jira-project.md) |

### Confluence
| Command | Description | Example | Ref |
|---|---|---|---|
| `ucli confluence page create` | Create a new page | `ucli confluence page create --space-key TEAM --title "Notes" --content "# Notes"` | [ref](reference/confluence-page.md) |
| `ucli confluence page get` | Get page by ID or title | `ucli confluence page get --page-id 123456789`<br>`ucli confluence page get --title "Meeting Notes" --space-key TEAM` | [ref](reference/confluence-page.md) |
| `ucli confluence page update` | Update page content | | [ref](reference/confluence-page.md) |
| `ucli confluence search` | Search content (CQL) | `ucli confluence search --query "project documentation"` | [ref](reference/confluence.md) |
| `ucli confluence page children` | Get child pages | `ucli confluence page children --parent-id 123456789` | [ref](reference/confluence-page.md) |

## Discover Parameters

Append `--help` to any command for full parameter list:

    ucli jira issue create --help

> Use Ref links above to view detailed parameter reference and more examples.

## User Notes

> **MUST READ** [users/skill.md](users/skill.md) for custom workflows and tips.
> **Config**: MCP server settings live in `~/.agents/ucli/servers.yaml` - edit there to take effect.
