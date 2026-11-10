# Workflow Commands

## run — Run a workflow from template or file

```bash
ucli ruflo workflow run --template ci-pipeline
ucli ruflo workflow run --file ./workflows/deploy.yaml
ucli ruflo workflow run --template code-review --task "Review PR #42"
```

Also supports: `--file`, `--task`, `--options` (options: parallel, maxAgents, timeout, dryRun)

## create — Create a new workflow

```bash
ucli ruflo workflow create --name my-flow
ucli ruflo workflow create --name release-flow --description "Full release process"
```

Also supports: `--description`, `--steps`, `--variables`

## execute — Execute a workflow

```bash
ucli ruflo workflow execute --workflow-id wf1
ucli ruflo workflow execute --workflow-id wf1 --variables '{"env": "prod"}'
```

Also supports: `--variables`, `--start-from-step`

## status — Get workflow status

```bash
ucli ruflo workflow status --workflow-id wf1
ucli ruflo workflow status --workflow-id wf1 --verbose true
```

## list — List all workflows

```bash
ucli ruflo workflow list
```

## pause — Pause a running workflow

```bash
ucli ruflo workflow pause --workflow-id wf1
```

## resume — Resume a paused workflow

```bash
ucli ruflo workflow resume --workflow-id wf1
```

## cancel — Cancel a workflow

```bash
ucli ruflo workflow cancel --workflow-id wf1
```

## delete — Delete a workflow

```bash
ucli ruflo workflow delete --workflow-id wf1
```

## template — Save or load workflow template

```bash
ucli ruflo workflow template --workflow-id wf1
```

Use `ucli ruflo workflow <action> --help` for full parameter details.
