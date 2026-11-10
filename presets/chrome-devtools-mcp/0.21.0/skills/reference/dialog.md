# Dialog Commands

## handle — Accept or dismiss a browser dialog

```bash
# Accept dialog (OK / Confirm)
ucli chrome-devtools dialog handle --action accept

# Dismiss dialog (Cancel)
ucli chrome-devtools dialog handle --action dismiss

# Accept with prompt text
ucli chrome-devtools dialog handle --action accept --prompt-text "my input"
```

Also supports: `--prompt-text`

> Use this when a browser dialog (alert, confirm, prompt) appears after an action.

Use `ucli chrome-devtools dialog handle --help` for full parameter details.
