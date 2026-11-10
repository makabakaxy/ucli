# Claims Commands

## claim — Claim an issue for work

```bash
ucli ruflo claims claim --issue-id 123 --claimant "agent:coder-1:coder"
ucli ruflo claims claim --issue-id 456 --claimant "human:user-1:Alice" --context "Working on auth refactor"
```

Also supports: `--context`

## release — Release a claim

```bash
ucli ruflo claims release --issue-id 123 --claimant "agent:coder-1:coder"
ucli ruflo claims release --issue-id 123 --claimant "agent:coder-1:coder" --reason "Blocked on dependency"
```

Also supports: `--reason`

## handoff — Request handoff to another claimant

```bash
ucli ruflo claims handoff --issue-id 123 --from "agent:coder-1:coder" --to "agent:coder-2:coder"
ucli ruflo claims handoff --issue-id 123 --from "agent:coder-1" --to "human:user-1" --progress 60 --reason "Needs human review"
```

Also supports: `--reason`, `--progress`

## accept-handoff — Accept a pending handoff

```bash
ucli ruflo claims accept-handoff --issue-id 123 --claimant "agent:coder-2:coder"
```

## list — List all claims

```bash
ucli ruflo claims list
```

## board — Get visual board view of all claims

```bash
ucli ruflo claims board
```

## load — Get agent load information

```bash
ucli ruflo claims load
```

## stealable — List stealable issues

```bash
ucli ruflo claims stealable
```

## steal — Steal a stealable issue

```bash
ucli ruflo claims steal --issue-id 123 --claimant "agent:coder-2:coder"
```

## mark-stealable — Mark issue as stealable

```bash
ucli ruflo claims mark-stealable --issue-id 123 --claimant "agent:coder-1:coder"
```

## rebalance — Suggest or apply load rebalancing

```bash
ucli ruflo claims rebalance
```

Use `ucli ruflo claims <action> --help` for full parameter details.
