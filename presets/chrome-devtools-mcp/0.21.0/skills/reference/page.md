# Page Commands

## create — Open a new tab and load a URL

```bash
ucli chrome-devtools page create --url https://example.com

# Open in background
ucli chrome-devtools page create --url https://example.com --background true
```

Also supports: `--background`, `--isolated-context`, `--timeout`

## list — List all open pages

```bash
ucli chrome-devtools page list
```

## navigate — Navigate to URL or go back/forward/reload

```bash
ucli chrome-devtools page navigate --type url --url https://example.com
ucli chrome-devtools page navigate --type back
ucli chrome-devtools page navigate --type reload
```

Also supports: `--ignore-cache`, `--handle-before-unload`, `--init-script`, `--timeout`

## select — Select a page as active context

```bash
# First list pages to find the ID
ucli chrome-devtools page list

ucli chrome-devtools page select --page-id 1
```

Also supports: `--bring-to-front`

## close — Close a page by ID

```bash
ucli chrome-devtools page close --page-id 2
```

## wait — Wait for text to appear on the page

```bash
ucli chrome-devtools page wait --text '["Submit"]'

# Wait for any of multiple texts
ucli chrome-devtools page wait --text '["Loaded", "Ready", "Done"]'
```

Also supports: `--timeout`

## emulate — Emulate network conditions, CPU, geolocation, or viewport

```bash
# Slow network
ucli chrome-devtools page emulate --network-conditions "Slow 3G"

# Mobile viewport
ucli chrome-devtools page emulate --viewport "375x667x2,mobile,touch"

# Dark mode
ucli chrome-devtools page emulate --color-scheme dark
```

Also supports: `--cpu-throttling-rate`, `--geolocation`, `--user-agent`

## resize — Resize page window

```bash
ucli chrome-devtools page resize --width 1280 --height 720
ucli chrome-devtools page resize --width 375 --height 812
```

Use `ucli chrome-devtools page <action> --help` for full parameter details.
