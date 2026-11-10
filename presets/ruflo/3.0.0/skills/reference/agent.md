# Agent Commands

## spawn — Spawn a new agent with intelligent model selection

```bash
ucli ruflo agent spawn --agent-type worker
ucli ruflo agent spawn --agent-type analyst --model sonnet
ucli ruflo agent spawn --agent-type coder --task "Implement OAuth flow" --model opus
```

Also supports: `--agent-id`, `--config`, `--domain`

## list — List all agents

```bash
ucli ruflo agent list
ucli ruflo agent list --status active
```

Also supports: `--domain`, `--include-terminated`

## status — Get agent status

```bash
ucli ruflo agent status --agent-id agent-1
```

## update — Update agent status or configuration

```bash
ucli ruflo agent update --agent-id agent-1 --status idle
ucli ruflo agent update --agent-id agent-1 --health 0.9 --task-count 2
```

Also supports: `--config`

## terminate — Terminate an agent

```bash
ucli ruflo agent terminate --agent-id agent-1
ucli ruflo agent terminate --agent-id agent-1 --force true
```

## health — Check agent health

```bash
ucli ruflo agent health
ucli ruflo agent health --agent-id agent-1 --threshold 0.7
```

## pool — Manage agent pool

```bash
ucli ruflo agent pool --action status
ucli ruflo agent pool --action scale --target-size 5 --agent-type worker
```

Also supports: `--target-size`, `--agent-type` (actions: status, scale, drain, fill)

Use `ucli ruflo agent <action> --help` for full parameter details.
