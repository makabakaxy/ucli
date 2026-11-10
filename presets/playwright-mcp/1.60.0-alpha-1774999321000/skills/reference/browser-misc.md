# Browser Miscellaneous Commands

## tab — Manage browser tabs

```bash
# List all tabs
ucli playwright browser tab --action list

# Open new tab
ucli playwright browser tab --action new

# Select tab by index
ucli playwright browser tab --action select --index 1

# Close tab by index (omit --index to close current)
ucli playwright browser tab --action close --index 0
```

Also supports: `--index`

## console list — Get console messages

```bash
# Get info-level messages (default)
ucli playwright browser console list --level info

# Get all errors
ucli playwright browser console list --level error

# Save to file
ucli playwright browser console list --level debug --filename console.txt
```

Also supports: `--all`, `--filename`

## network list — Get network requests

```bash
# Basic request list (no static assets, no body/headers)
ucli playwright browser network list --static false --request-body false --request-headers false

# Filter by URL pattern
ucli playwright browser network list --static false --request-body false --request-headers false --filter "/api/.*"
```

Also supports: `--filter`, `--filename`

## dialog handle — Handle a browser dialog (alert/confirm/prompt)

```bash
# Accept dialog
ucli playwright browser dialog handle --accept true

# Dismiss dialog
ucli playwright browser dialog handle --accept false

# Accept prompt with text
ucli playwright browser dialog handle --accept true --prompt-text "my answer"
```

Also supports: `--prompt-text`

## file upload — Upload files

```bash
ucli playwright browser file upload --paths '["/absolute/path/to/file.pdf"]'

# Upload multiple files
ucli playwright browser file upload --paths '["/path/file1.png","/path/file2.png"]'
```

## script evaluate — Evaluate JavaScript on the page

```bash
# Run JS expression
ucli playwright browser script evaluate --function "() => document.title"

# Run on element
ucli playwright browser script evaluate --function "(el) => el.textContent" --ref e1 --element "heading text"
```

Also supports: `--element`, `--ref`, `--filename`

## script run — Run a Playwright code snippet

```bash
ucli playwright browser script run --code "async (page) => { await page.getByRole('button', { name: 'Submit' }).click(); }"

# Load code from file
ucli playwright browser script run --filename ./script.js
```

Also supports: `--code`, `--filename`

## wait — Wait for text or a specified time

```bash
# Wait for text to appear
ucli playwright browser wait --text "Page loaded"

# Wait for text to disappear
ucli playwright browser wait --text-gone "Loading..."

# Wait for a fixed time (seconds)
ucli playwright browser wait --time 2
```

Also supports: `--time`, `--text`, `--text-gone`

Use `ucli playwright browser <cmd> --help` for full parameter details.
