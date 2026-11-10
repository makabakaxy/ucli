---
name: playwright-mcp
description: Automate browser interactions via CLI. Use when user needs to navigate websites, click elements, fill forms, take screenshots, capture accessibility snapshots, or run JavaScript in a browser.
source_version: "1.60.0-alpha-1774999321000"
source_cli_hash: "2905aebc"
generated_at: "2026-04-06T08:28:46.507071+00:00"
---

# playwright-mcp (via ucli)

Browser automation via Playwright: navigate, interact, screenshot, and inspect web pages.

## Shortcuts

- `ucli playwright <cmd>` (alias for `playwright-mcp`)

## Commands

### Browser
| Command | Description | Example | Ref |
|---|---|---|---|
| `ucli playwright browser navigate go` | Navigate to a URL | `ucli playwright browser navigate go --url https://example.com` | [ref](reference/browser-navigate.md) |
| `ucli playwright browser navigate back` | Go back in browser history | | [ref](reference/browser-navigate.md) |
| `ucli playwright browser page snapshot` | Capture accessibility snapshot (use for actions) | `ucli playwright browser page snapshot`<br>`ucli playwright browser page snapshot --filename snap.md` | [ref](reference/browser-page.md) |
| `ucli playwright browser page screenshot` | Take a screenshot of the current page | `ucli playwright browser page screenshot --type png --filename page.png` | [ref](reference/browser-page.md) |
| `ucli playwright browser interact click` | Click an element on the page | `ucli playwright browser interact click --ref e1` | [ref](reference/browser-interact.md) |
| `ucli playwright browser interact type` | Type text into an editable element | `ucli playwright browser interact type --ref e1 --text "hello"` | [ref](reference/browser-interact.md) |
| `ucli playwright browser interact fill-form` | Fill multiple form fields at once | | [ref](reference/browser-interact.md) |
| `ucli playwright browser wait` | Wait for text or a specified time | `ucli playwright browser wait --text "Loaded"`<br>`ucli playwright browser wait --time 2` | [ref](reference/browser-misc.md) |

## Discover Parameters

Append `--help` to any command for full parameter list:

    ucli playwright browser interact click --help

> **Note**: Use Ref links in the Commands table above to view detailed parameter reference and more examples.

## User Notes

> **MUST READ** [users/skill.md](users/skill.md) for custom workflows and tips.
> **Config**: MCP server settings live in `~/.agents/ucli/servers.yaml` - edit there to take effect.
