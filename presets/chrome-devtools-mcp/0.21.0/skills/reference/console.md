# Console Commands

## list — List all console messages for the current page

```bash
# All messages
ucli chrome-devtools console list

# Only errors and warnings
ucli chrome-devtools console list --types '["error","warn"]'

# Paginated
ucli chrome-devtools console list --page-size 50 --page-idx 0
```

Also supports: `--page-size`, `--page-idx`, `--types`, `--include-preserved-messages`

## get — Get a console message by ID

```bash
ucli chrome-devtools console get --msgid 3
```

> Use `list` first to find msgid values.

Use `ucli chrome-devtools console <action> --help` for full parameter details.
