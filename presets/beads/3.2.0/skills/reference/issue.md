# Issue Commands

## create — Create a new issue

```bash
ucli beads issue create --title "Fix memory leak" --issue-type bug
ucli beads issue create --title "Add login page" --issue-type feature --assignee alice
ucli beads issue create --title "API refactor" --issue-type task --deps '["ISSUE-1","ISSUE-2"]'
```

Also supports: `--description`, `--design`, `--acceptance`, `--external-ref`, `--priority`, `--labels`, `--id`, `--deps`, `--workspace-root`

## list — List issues with optional filters

```bash
ucli beads issue list
ucli beads issue list --status open --assignee alice
ucli beads issue list --issue-type bug --priority 1
```

Also supports: `--labels`, `--labels-any`, `--query`, `--unassigned`, `--limit`, `--workspace-root`, `--brief`, `--fields`, `--max-description-length`

## get — Get detailed issue info (including dependencies)

```bash
ucli beads issue get --issue-id ISSUE-1
```

Also supports: `--workspace-root`, `--brief`, `--brief-deps`, `--fields`, `--max-description-length`

## update — Update an existing issue

```bash
ucli beads issue update --issue-id ISSUE-1 --status in_progress
ucli beads issue update --issue-id ISSUE-1 --priority 1 --assignee bob
```

Also supports: `--title`, `--description`, `--design`, `--acceptance-criteria`, `--notes`, `--external-ref`, `--workspace-root`

## close — Close/complete an issue

```bash
ucli beads issue close --issue-id ISSUE-1
ucli beads issue close --issue-id ISSUE-1 --reason "Shipped in v2.3"
```

Also supports: `--workspace-root`

## reopen — Reopen one or more closed issues

```bash
ucli beads issue reopen --issue-ids '["ISSUE-1"]'
ucli beads issue reopen --issue-ids '["ISSUE-1","ISSUE-2"]' --reason "Regression found"
```

Also supports: `--workspace-root`

## claim — Atomically claim an issue for work

Sets assignee + in_progress in one operation (CAS-style).

```bash
ucli beads issue claim --issue-id ISSUE-1
```

Also supports: `--workspace-root`

## ready — Find issues with no blockers

```bash
ucli beads issue ready
ucli beads issue ready --assignee alice --limit 5
ucli beads issue ready --issue-type bug --priority 1
```

Also supports: `--labels`, `--labels-any`, `--unassigned`, `--sort-policy`, `--workspace-root`, `--brief`, `--fields`, `--max-description-length`

## blocked — Get issues blocked by unresolved dependencies

```bash
ucli beads issue blocked
```

Also supports: `--workspace-root`, `--brief`, `--brief-deps`

Use `ucli beads issue <action> --help` for full parameter details.
