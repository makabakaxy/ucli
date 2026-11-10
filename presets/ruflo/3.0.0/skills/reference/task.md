# Task Commands

## create — Create a new task

```bash
ucli ruflo task create --type feature --description "Implement login page"
ucli ruflo task create --type bugfix --description "Fix null pointer" --priority high
ucli ruflo task create --type research --description "Evaluate caching options" --assign-to '["agent-1","agent-2"]'
```

Also supports: `--priority`, `--assign-to`, `--tags` (types: feature, bugfix, research, refactor)

## list — List all tasks

```bash
ucli ruflo task list
ucli ruflo task list --status pending --priority high
ucli ruflo task list --type bugfix --assigned-to agent-1
```

Also supports: `--status`, `--type`, `--assigned-to`, `--priority`, `--limit`

## status — Get task status

```bash
ucli ruflo task status --task-id t1
```

## update — Update task status or progress

```bash
ucli ruflo task update --task-id t1 --status in-progress
ucli ruflo task update --task-id t1 --progress 75
```

Also supports: `--assign-to`

## complete — Mark task as complete

```bash
ucli ruflo task complete --task-id t1
ucli ruflo task complete --task-id t1 --result '{"files": ["auth.ts"]}'
```

Also supports: `--result`

## assign — Assign task to agents

```bash
ucli ruflo task assign --task-id t1 --agent-ids '["agent-1","agent-2"]'
ucli ruflo task assign --task-id t1 --unassign true
```

## cancel — Cancel a task

```bash
ucli ruflo task cancel --task-id t1
ucli ruflo task cancel --task-id t1 --reason "Requirements changed"
```

## summary — Get tasks summary by status

```bash
ucli ruflo task summary
```

Use `ucli ruflo task <action> --help` for full parameter details.
