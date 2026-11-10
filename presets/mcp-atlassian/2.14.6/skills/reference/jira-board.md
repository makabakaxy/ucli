# JIRA Board Commands

## list — List agile boards

```bash
ucli jira board list
ucli jira board list --project-key INFRA
ucli jira board list --board-type scrum --project-key DEV
```

Also supports: `--board-name`, `--project-key`, `--board-type`, `--start-at`, `--limit`

## issues — Get issues from a board

```bash
ucli jira board issues --board-id 42 --jql "status=Open"
ucli jira board issues --board-id 42 --jql "issuetype=Bug AND priority=High" --limit 20
```

Also supports: `--fields`, `--start-at`, `--limit`, `--expand`

Use `ucli jira board <action> --help` for full parameter details.
