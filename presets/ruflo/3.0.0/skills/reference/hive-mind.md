# Hive-Mind Commands

## spawn — Spawn workers and join hive-mind

```bash
ucli ruflo hive-mind spawn --count 3
ucli ruflo hive-mind spawn --count 5 --role specialist --agent-type analyst
```

Also supports: `--count`, `--role`, `--agent-type`, `--prefix` (roles: worker, specialist, scout)

## init — Initialize hive-mind collective

```bash
ucli ruflo hive-mind init
ucli ruflo hive-mind init --topology mesh --queen-id queen-1
```

Also supports: `--topology`, `--queen-id` (topologies: mesh, hierarchical, ring, star)

## status — Get hive-mind status

```bash
ucli ruflo hive-mind status
ucli ruflo hive-mind status --verbose true
```

## join — Join an agent to the hive-mind

```bash
ucli ruflo hive-mind join --agent-id agent-1
ucli ruflo hive-mind join --agent-id agent-2 --role specialist
```

Also supports: `--role`

## leave — Remove agent from hive-mind

```bash
ucli ruflo hive-mind leave --agent-id agent-1
```

## consensus — Propose or vote on consensus

```bash
ucli ruflo hive-mind consensus --action propose --type config-update --value '{"timeout": 30}'
ucli ruflo hive-mind consensus --action vote --proposal-id p1 --vote true --voter-id agent-1
ucli ruflo hive-mind consensus --action status --proposal-id p1
```

Also supports: `--strategy`, `--quorum-preset`, `--term`, `--timeout-ms` (strategies: bft, raft, quorum)

## broadcast — Broadcast to all workers

```bash
ucli ruflo hive-mind broadcast --message "Start phase 2"
ucli ruflo hive-mind broadcast --message "Critical: abort" --priority critical
```

Also supports: `--priority`, `--from-id`

## memory — Access hive shared memory

```bash
ucli ruflo hive-mind memory --action set --key shared-state --value '{"phase": 2}'
ucli ruflo hive-mind memory --action get --key shared-state
ucli ruflo hive-mind memory --action list
```

## shutdown — Shutdown hive-mind

```bash
ucli ruflo hive-mind shutdown
ucli ruflo hive-mind shutdown --graceful false --force true
```

Use `ucli ruflo hive-mind <action> --help` for full parameter details.
