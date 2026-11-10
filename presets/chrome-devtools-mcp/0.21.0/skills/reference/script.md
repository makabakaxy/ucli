# Script Commands

## evaluate — Evaluate a JavaScript function in the current page

```bash
# Get page title
ucli chrome-devtools script evaluate --function '() => document.title'

# Get element text using snapshot UID as argument
ucli chrome-devtools script evaluate --function '(el) => el.innerText' --args '["e5"]'

# Async fetch
ucli chrome-devtools script evaluate --function 'async () => { const r = await fetch("/api/status"); return r.json(); }'
```

Also supports: `--args`

> Returned values must be JSON-serializable.
> UIDs in `--args` refer to elements from the accessibility snapshot.

Use `ucli chrome-devtools script evaluate --help` for full parameter details.
