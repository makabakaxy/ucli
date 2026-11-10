# Workspace Commands

## dep — Add a dependency between issues

Dependency types: `blocks` (hard blocker), `related` (soft link), `parent-child` (epic/subtask), `discovered-from` (found during work).

```bash
ucli beads dep --issue-id ISSUE-2 --depends-on-id ISSUE-1
ucli beads dep --issue-id ISSUE-3 --depends-on-id ISSUE-2 --dep-type related
ucli beads dep --issue-id ISSUE-4 --depends-on-id ISSUE-1 --dep-type parent-child
```

Also supports: `--workspace-root`

## stats — Get issue statistics

Returns: total, open, in_progress, closed, blocked, ready, average lead time.

```bash
ucli beads stats
```

Also supports: `--workspace-root`

## context — Manage workspace context

Actions: `show` (current context), `set` (set workspace root), `init` (initialize beads in workspace).

```bash
ucli beads context --action show
ucli beads context --action set --workspace-root /path/to/project
ucli beads context --action init
ucli beads context --action init --workspace-root /path/to/project --prefix PROJ
```

Also supports: `--prefix`

## admin — Administrative and diagnostic operations

Actions: `validate`, `repair`, `schema`, `debug`, `migration`, `pollution`.

```bash
ucli beads admin --action validate
ucli beads admin --action validate --checks "orphans,duplicates"
ucli beads admin --action repair --fix true
ucli beads admin --action pollution
ucli beads admin --action pollution --clean true
ucli beads admin --action debug
ucli beads admin --action schema
ucli beads admin --action migration
```

Also supports: `--checks`, `--fix-all`, `--fix`, `--clean`, `--workspace-root`

## tool list — List available beads tools

```bash
ucli beads tool list
```

## tool get — Get detailed info about a specific tool

```bash
ucli beads tool get --tool-name create
ucli beads tool get --tool-name dep
```

Use `ucli beads <cmd> --help` for full parameter details.
