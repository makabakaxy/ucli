# Skill File Collection Example

This file contains a complete Skill file collection example, showing the standard format for the generated files.

## SKILL.md Example

```markdown
---
name: mcp-atlassian
description: Manage JIRA issues, sprints, boards, and Confluence pages via CLI. Use when user needs to create/search/update JIRA tickets, manage sprints, or edit Confluence pages.
source_version: "1.2.3"
source_cli_hash: "a3f8c2d1"
generated_at: "2026-04-02T10:00:00Z"
---

# mcp-atlassian (via ucli)

Manage JIRA and Confluence via CLI.

## Shortcuts

- `ucli jira <cmd>`
- `ucli confluence <cmd>`
- `ucli atlassian <cmd>`

## Commands

### JIRA
| Command | Description | Example | Ref |
|---|---|---|---|
| `ucli jira issue create` | Create a new issue | `ucli jira issue create --project-key INFRA --summary "Fix memory leak" --issue-type Task`<br>`ucli jira issue create --project-key DEV --summary "Add login" --issue-type Story --assignee john@example.com` | [ref](reference/jira-issue.md) |
| `ucli jira issue get` | Get issue details | `ucli jira issue get --issue-key INFRA-1234` | [ref](reference/jira-issue.md) |
| `ucli jira issue search` | Search issues using JQL | `ucli jira issue search --jql "project=INFRA AND status=Open"` | [ref](reference/jira-issue.md) |
| `ucli jira issue update` | Update an existing issue | | [ref](reference/jira-issue.md) |
| `ucli jira sprint create` | Create a sprint | | [ref](reference/jira-sprint.md) |
| `ucli jira sprint list` | List sprints for a board | | [ref](reference/jira-sprint.md) |
| `ucli jira board list` | List agile boards | | [ref](reference/jira-board.md) |
| `ucli jira project list` | List all projects | | [ref](reference/jira-project.md) |

### Confluence
| Command | Description | Example | Ref |
|---|---|---|---|
| `ucli confluence page get` | Get page content | `ucli confluence page get --page-id 12345` | [ref](reference/confluence-page.md) |
| `ucli confluence page create` | Create a new page | `ucli confluence page create --space-key TEAM --title "Meeting Notes" --content "# Notes"` | [ref](reference/confluence-page.md) |
| `ucli confluence page update` | Update page content | | [ref](reference/confluence-page.md) |
| `ucli confluence search` | Search Confluence content | `ucli confluence search --query "project documentation"` | [ref](reference/confluence.md) |

## Discover Parameters

Append `--help` to any command for full parameter list:

    ucli jira issue create --help

> **Note**: Use Ref links in the Commands table above to view detailed parameter reference and more examples.

## User Notes

> **MUST READ** [users/skill.md](users/skill.md) for custom workflows and tips.
> **Config**: MCP server settings live in `~/.agents/ucli/servers.yaml` - edit there to take effect.
```

## reference/jira-issue.md Example

```markdown
# JIRA Issue Commands

## create — Create a new JIRA issue

```bash
# Create a task
ucli jira issue create --project-key INFRA --summary "Fix memory leak" --issue-type Task

# Create with assignee
ucli jira issue create --project-key DEV --summary "Add login" --issue-type Story --assignee john@example.com

# Create with additional fields
ucli jira issue create --project-key INFRA --summary "Bug fix" --issue-type Bug --components "Frontend,API" --additional-fields '{"priority": {"name": "High"}}'
```

Also supports: `--description`, `--components`, `--additional-fields`

## get — Get issue details by key

```bash
ucli jira issue get --issue-key INFRA-1234
```

Also supports: `--fields`, `--expand`, `--comment-limit`, `--properties`, `--update-history`

## search — Search issues using JQL

```bash
ucli jira issue search --jql "project=INFRA AND status=Open"
ucli jira issue search --jql "assignee=currentUser() AND updated >= -7d" --limit 20
```

Also supports: `--fields`, `--limit`, `--start-at`, `--expand`, `--projects-filter`

## update — Update an existing issue

```bash
ucli jira issue update --issue-key INFRA-1234 --fields '{"summary": "New title", "assignee": "user@example.com"}'
```

Also supports: `--additional-fields`, `--components`, `--attachments`

## delete — Delete an issue

```bash
ucli jira issue delete --issue-key INFRA-1234
```

## transition — Transition issue status

```bash
ucli jira issue transition --issue-key INFRA-1234 --transition-id 31
```

Also supports: `--fields`, `--comment`

## link — Create a link between two issues

```bash
ucli jira issue link --link-type "Blocks" --inward-issue-key INFRA-123 --outward-issue-key INFRA-456
```

Also supports: `--comment`, `--comment-visibility`

Use `ucli jira issue <action> --help` for full parameter details.
```

## users/workflows.md Example

Generated on first `skill generate` run, never overwritten afterwards.

```markdown
# Common Workflow Examples

> Multi-step workflow examples. For single-command usage, refer to the Example column in SKILL.md.
> This file is never overwritten by ucli generate/update — feel free to edit and add your own workflows.

## JIRA Workflow

### Create and assign an issue
```bash
ucli jira issue create --project-key INFRA --summary "Fix memory leak" --issue-type Bug --assignee john@example.com
```

### Search and update issues
```bash
# Find open bugs
ucli jira issue search --jql "project=INFRA AND issuetype=Bug AND status=Open"

# Update priority
ucli jira issue update --issue-key INFRA-1234 --fields '{"priority": {"name": "High"}}'

# Transition to In Progress
ucli jira issue transition --issue-key INFRA-1234 --transition-id 21
```

### Sprint management
```bash
# List boards
ucli jira board list --project-key INFRA

# List active sprints
ucli jira sprint list --board-id 42 --state active

# Add issues to sprint
ucli jira sprint add-issues --sprint-id 100 --issue-keys "INFRA-1,INFRA-2"
```

### Project overview
```bash
# List all projects
ucli jira project list

# Get project issues
ucli jira project issues --project-key INFRA --limit 20
```

## Confluence Workflow

### Create and manage pages
```bash
# Create a page
ucli confluence page create --space-key TEAM --title "Meeting Notes" --content "# Notes\n..."

# Get page content
ucli confluence page get --page-id 123456789

# Update a page
ucli confluence page update --page-id 123456789 --title "Updated Notes" --content "# Updated\n..."
```

### Search and navigate
```bash
# Search pages
ucli confluence search --query "project documentation" --limit 10

# Get child pages
ucli confluence page children --parent-id 123456789

# Compare page versions
ucli confluence page diff --page-id 123456789 --from-version 1 --to-version 3
```

### Attachment management
```bash
# List attachments
ucli confluence attachment list --content-id 123456789

# Upload attachment
ucli confluence attachment upload --content-id 123456789 --file-path ./diagram.png
```
```
