# Change Commands

## create — Create a new change directory

```bash
ucli openspec change create --name add-dark-mode
ucli openspec change create --name add-dark-mode --description "Add dark mode support to the UI"
```

Also supports: `--description`

## status — Display artifact completion status for a change

```bash
ucli openspec change status
ucli openspec change status --change-name add-dark-mode
```

Also supports: `--change-name`, `--json`

## instructions — Output enriched instructions for an artifact or apply action

```bash
ucli openspec change instructions --artifact design.md
ucli openspec change instructions --artifact design.md --change-name add-dark-mode
ucli openspec change instructions --artifact apply --change-name add-dark-mode
```

Also supports: `--change-name`, `--json`

## archive — Archive a completed change and update main specs

```bash
ucli openspec change archive --change-name add-dark-mode
ucli openspec change archive --change-name add-dark-mode --skip-specs
```

Also supports: `--skip-specs`

Use `ucli openspec change <cmd> --help` for full parameter details.
