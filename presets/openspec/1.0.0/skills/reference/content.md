# Content Commands

## list — List changes or specs

```bash
ucli openspec content list
ucli openspec content list --specs
```

Also supports: `--specs`, `--json`

## show — Show details of a change or spec

```bash
ucli openspec content show --item-name add-dark-mode
ucli openspec content show --item-name my-api-spec --type spec
```

Also supports: `--type`, `--json`

## read-file — Read any OpenSpec artifact file directly

Faster than `show` when you need file contents.

```bash
ucli openspec content read-file --name add-dark-mode --file-type design.md
ucli openspec content read-file --name add-dark-mode --file-type proposal.md
ucli openspec content read-file --name add-dark-mode --file-type tasks.md --type change
```

Available `--file-type` values: `proposal.md`, `design.md`, `tasks.md`, `.openspec.yaml`

Also supports: `--type` (change|spec, to disambiguate if names conflict)

## validate — Validate a change proposal or spec

```bash
ucli openspec content validate
ucli openspec content validate --item-name add-dark-mode
ucli openspec content validate --all --strict
```

Also supports: `--item-name`, `--all`, `--strict`, `--json`

Use `ucli openspec content <cmd> --help` for full parameter details.
