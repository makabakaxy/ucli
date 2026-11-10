# Hooks Commands

## pre-task — Record task start and get agent suggestions

```bash
ucli ruflo hooks pre-task --task-id t1 --description "Fix memory leak in auth module"
ucli ruflo hooks pre-task --task-id t1 --description "Refactor API layer" --file-path src/api.ts
```

Also supports: `--file-path`

## post-task — Record task completion for learning

```bash
ucli ruflo hooks post-task --task-id t1 --success true
ucli ruflo hooks post-task --task-id t1 --success false --quality 0.4 --agent coder-1
```

Also supports: `--agent`, `--quality`, `--task`, `--store-decisions`

## pre-edit — Get context before editing a file

```bash
ucli ruflo hooks pre-edit --file-path src/auth.ts
ucli ruflo hooks pre-edit --file-path src/api.ts --operation refactor
```

Also supports: `--operation`, `--context` (operations: create, update, delete, refactor)

## post-edit — Record editing outcome

```bash
ucli ruflo hooks post-edit --file-path src/auth.ts --success true
ucli ruflo hooks post-edit --file-path src/auth.ts --success false --agent coder-1
```

Also supports: `--agent`

## pre-command — Assess risk before executing a command

```bash
ucli ruflo hooks pre-command --command "git reset --hard HEAD~3"
```

## post-command — Record command execution outcome

```bash
ucli ruflo hooks post-command --command "npm test" --exit-code 0
```

Also supports: `--exit-code`

## route — Route task to optimal agent

```bash
ucli ruflo hooks route --task "implement OAuth flow"
ucli ruflo hooks route --task "fix CSS layout bug" --context "React app, mobile-first"
```

Also supports: `--context`, `--use-semantic-router`

## init — Initialize hooks in project

```bash
ucli ruflo hooks init
ucli ruflo hooks init --template standard --path /path/to/project
```

Also supports: `--path`, `--template`, `--force` (templates: minimal, standard, full)

## metrics — View learning metrics dashboard

```bash
ucli ruflo hooks metrics
ucli ruflo hooks metrics --period 7d --include-v3 true
```

Also supports: `--period` (1h, 24h, 7d, 30d), `--include-v3`

## pretrain — Bootstrap intelligence from repo

```bash
ucli ruflo hooks pretrain
ucli ruflo hooks pretrain --depth deep --path /path/to/repo
```

Also supports: `--path`, `--depth`, `--skip-cache`

## Session hooks

```bash
ucli ruflo hooks session start
ucli ruflo hooks session start --restore-latest true
ucli ruflo hooks session end --save-state true
ucli ruflo hooks session restore --session-id sess-abc
```

## notify — Send cross-agent notification

```bash
ucli ruflo hooks notify --message "Phase 1 complete" --target all
ucli ruflo hooks notify --message "Urgent: build failed" --target agent-1 --priority urgent
```

Also supports: `--target`, `--priority`, `--data`

Use `ucli ruflo hooks <action> --help` for full parameter details.
