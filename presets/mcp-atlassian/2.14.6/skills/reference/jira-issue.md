# JIRA Issue Commands

## create — Create a new JIRA issue

```bash
ucli jira issue create --project-key INFRA --summary "Fix memory leak" --issue-type Task
ucli jira issue create --project-key DEV --summary "Add login" --issue-type Story --assignee john@example.com
ucli jira issue create --project-key INFRA --summary "Bug fix" --issue-type Bug --components "Frontend,API" --additional-fields '{"priority": {"name": "High"}}'
```

Also supports: `--description`, `--components`, `--additional-fields`

## get — Get issue details by key

```bash
ucli jira issue get --issue-key INFRA-1234
ucli jira issue get --issue-key INFRA-1234 --fields "summary,status,assignee" --comment-limit 5
```

Also supports: `--fields`, `--expand`, `--comment-limit`, `--properties`, `--update-history`

## search — Search issues using JQL

```bash
ucli jira issue search --jql "project=INFRA AND status=Open"
ucli jira issue search --jql "assignee=currentUser() AND updated >= -7d" --limit 20
```

Also supports: `--fields`, `--limit`, `--start-at`, `--expand`, `--projects-filter`, `--page-token`

## update — Update an existing issue

```bash
ucli jira issue update --issue-key INFRA-1234 --fields '{"summary": "New title", "assignee": "user@example.com"}'
```

Also supports: `--additional-fields`, `--components`, `--attachments`

## delete — Delete an issue

```bash
ucli jira issue delete --issue-key INFRA-1234
```

## transition — Transition issue to new status

```bash
ucli jira issue transition --issue-key INFRA-1234 --transition-id 31
ucli jira issue transition --issue-key INFRA-1234 --transition-id 31 --comment "Moving to done"
```

Also supports: `--fields`, `--comment`

## transitions — List available transitions

```bash
ucli jira issue transitions --issue-key INFRA-1234
```

## link — Link two issues

```bash
ucli jira issue link --link-type "Blocks" --inward-issue-key INFRA-123 --outward-issue-key INFRA-456
```

Also supports: `--comment`, `--comment-visibility`

## unlink — Remove a link between issues

```bash
ucli jira issue unlink --link-id 12345
```

## epic-link — Link issue to an epic

```bash
ucli jira issue epic-link --issue-key INFRA-123 --epic-key INFRA-100
```

## remote-link — Create a remote web link

```bash
ucli jira issue remote-link --issue-key INFRA-123 --url "https://docs.example.com" --title "Documentation"
```

Also supports: `--summary`, `--relationship`, `--icon-url`

## batch-create — Batch create multiple issues

```bash
ucli jira issue batch-create --issues '[{"project_key":"INFRA","summary":"Task 1","issue_type":"Task"},{"project_key":"INFRA","summary":"Task 2","issue_type":"Bug"}]'
```

Also supports: `--validate-only`

## batch-changelogs — Get changelogs for multiple issues

```bash
ucli jira issue batch-changelogs --issue-ids-or-keys "INFRA-1,INFRA-2"
```

Also supports: `--fields`, `--limit`

## dates — Get date and transition history

```bash
ucli jira issue dates --issue-key INFRA-1234
```

Also supports: `--include-status-changes`, `--include-status-summary`

## sla — Calculate SLA metrics

```bash
ucli jira issue sla --issue-key INFRA-1234
ucli jira issue sla --issue-key INFRA-1234 --metrics "cycle_time,time_in_status"
```

Also supports: `--metrics`, `--working-hours-only`, `--include-raw-dates`

## dev-info — Get development info (PRs, commits, branches)

```bash
ucli jira issue dev-info --issue-key INFRA-1234
```

Also supports: `--application-type`, `--data-type`

## comment add — Add a comment

```bash
ucli jira issue comment add --issue-key INFRA-1234 --body "This is a comment"
```

Also supports: `--visibility`, `--public`

## comment edit — Edit a comment

```bash
ucli jira issue comment edit --issue-key INFRA-1234 --comment-id 56789 --body "Updated comment"
```

Also supports: `--visibility`

## watcher list/add/remove — Manage watchers

```bash
ucli jira issue watcher list --issue-key INFRA-1234
ucli jira issue watcher add --issue-key INFRA-1234 --user-identifier user@example.com
ucli jira issue watcher remove --issue-key INFRA-1234 --account-id abc123
```

## worklog list/add — Manage worklogs

```bash
ucli jira issue worklog list --issue-key INFRA-1234
ucli jira issue worklog add --issue-key INFRA-1234 --time-spent "2h 30m"
```

Also supports: `--comment`, `--started`, `--original-estimate`, `--remaining-estimate`

Use `ucli jira issue <action> --help` for full parameter details.
