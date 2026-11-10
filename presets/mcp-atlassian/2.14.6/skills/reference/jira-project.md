# JIRA Project Commands

## list — List all accessible projects

```bash
ucli jira project list
ucli jira project list --include-archived
```

Also supports: `--include-archived`

## issues — Get all issues in a project

```bash
ucli jira project issues --project-key INFRA
ucli jira project issues --project-key INFRA --limit 20
```

Also supports: `--limit`, `--start-at`

## components — Get project components

```bash
ucli jira project components --project-key INFRA
```

## versions — Get project fix versions

```bash
ucli jira project versions --project-key INFRA
```

Use `ucli jira project <action> --help` for full parameter details.
