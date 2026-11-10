---
name: "puppeteer-mcp"
description: Automate browser interactions via Puppeteer CLI — navigate pages, take screenshots, click/fill/hover elements, and execute JavaScript. Use when user needs to browse URLs, capture screenshots, fill forms, or run JS in a browser.
source_version: "0.1.0"
source_cli_hash: "3c7e9966"
generated_at: "2026-04-06T09:07:19.574380+00:00"
---

# puppeteer-mcp (via ucli)

Control a Puppeteer-driven browser: navigate, screenshot, interact with elements, and run JavaScript.

## Shortcuts

- `ucli puppeteer <cmd>` (alias for `ucli puppeteer-mcp`)

## Commands

### page
| Command | Description | Example | Ref |
|---|---|---|---|
| `ucli puppeteer page navigate` | Navigate to a URL | `ucli puppeteer page navigate --url https://example.com` | [ref](reference/page.md) |
| `ucli puppeteer page screenshot` | Take a screenshot of the page or element | `ucli puppeteer page screenshot --name my-shot`<br>`ucli puppeteer page screenshot --name elem-shot --selector "#main"` | [ref](reference/page.md) |
| `ucli puppeteer page evaluate` | Execute JavaScript in browser console | `ucli puppeteer page evaluate --script "document.title"` | [ref](reference/page.md) |

### element
| Command | Description | Example | Ref |
|---|---|---|---|
| `ucli puppeteer element click` | Click an element | `ucli puppeteer element click --selector "#submit-btn"` | [ref](reference/element.md) |
| `ucli puppeteer element fill` | Fill an input field | `ucli puppeteer element fill --selector "#email" --value "user@example.com"` | [ref](reference/element.md) |
| `ucli puppeteer element select` | Select a dropdown option | `ucli puppeteer element select --selector "#country" --value "US"` | [ref](reference/element.md) |
| `ucli puppeteer element hover` | Hover over an element | `ucli puppeteer element hover --selector ".menu-item"` | [ref](reference/element.md) |

## Discover Parameters

Append `--help` to any command for full parameter list:

    ucli puppeteer page navigate --help

> **Note**: Use Ref links in the Commands table above to view detailed parameter reference and more examples.

## User Notes

> **MUST READ** [users/skill.md](users/skill.md) for custom workflows and tips.
> **Config**: MCP server settings live in `~/.agents/ucli/servers.yaml` - edit there to take effect.
