# Browser Page Commands

## snapshot — Capture accessibility snapshot (preferred for element interaction)

```bash
# Capture snapshot to response
ucli playwright browser page snapshot

# Save snapshot to file
ucli playwright browser page snapshot --filename snap.md
```

Also supports: `--depth`

## screenshot — Take a screenshot of the current page

```bash
# Default PNG screenshot
ucli playwright browser page screenshot --type png

# Save to file
ucli playwright browser page screenshot --type png --filename page.png

# Full page screenshot
ucli playwright browser page screenshot --type png --full-page
```

Also supports: `--filename`, `--element`, `--ref`, `--full-page`

> Note: Use `snapshot` to identify element refs for interactions; use `screenshot` for visual capture only.

## close — Close the current page

```bash
ucli playwright browser page close
```

## resize — Resize the browser window

```bash
ucli playwright browser page resize --width 1280 --height 720
```

Use `ucli playwright browser page <cmd> --help` for full parameter details.
