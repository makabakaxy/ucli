# History operations

## undo — Step back through history

```bash
ucli ps history undo --document-id 1
```

Also supports: `--steps`

## redo — Redo undone operations

```bash
ucli ps history redo --document-id 1
```

Also supports: `--steps`

## list — Get the history stack

```bash
ucli ps history list --document-id 1
```

Use `ucli ps history <action> --help` for full parameter details.
