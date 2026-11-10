---
name: "browser-mcp"
description: Automate browser navigation, element interaction, and page capture via CLI. Use when user needs to navigate URLs, click/type/select page elements, take screenshots, or extract console logs.
source_version: "0.1.3"
source_cli_hash: "7e4a4a23"
generated_at: "2026-04-06T09:05:20.157997+00:00"
---

# browser-mcp (via ucli)

Automate browser interactions via CLI.

## Shortcuts

- `ucli browser <cmd>` (alias for `ucli browser-mcp`)

## Commands

### Navigate
| Command | Description | Example | Ref |
|---|---|---|---|
| `ucli browser navigate go` | Navigate to a URL | `ucli browser navigate go --url https://example.com` | [ref](reference/navigate.md) |
| `ucli browser navigate back` | Go back to the previous page | `ucli browser navigate back` | [ref](reference/navigate.md) |
| `ucli browser navigate forward` | Go forward to the next page | `ucli browser navigate forward` | [ref](reference/navigate.md) |

### Interact
| Command | Description | Example | Ref |
|---|---|---|---|
| `ucli browser interact click` | Click on a web page element | `ucli browser interact click --element "Submit button" --ref e123` | [ref](reference/interact.md) |
| `ucli browser interact type` | Type text into an editable element | `ucli browser interact type --element "Search box" --ref e456 --text "hello" --submit true` | [ref](reference/interact.md) |
| `ucli browser interact select-option` | Select an option in a dropdown | `ucli browser interact select-option --element "Country" --ref e789 --values '["US"]'` | [ref](reference/interact.md) |
| `ucli browser interact hover` | Hover over a page element | `ucli browser interact hover --element "Menu" --ref e101` | [ref](reference/interact.md) |
| `ucli browser interact press-key` | Press a key on the keyboard | `ucli browser interact press-key --key "Enter"` | [ref](reference/interact.md) |

### Page
| Command | Description | Example | Ref |
|---|---|---|---|
| `ucli browser page snapshot` | Capture accessibility snapshot of the current page | `ucli browser page snapshot` | [ref](reference/page.md) |
| `ucli browser page screenshot` | Take a screenshot of the current page | `ucli browser page screenshot` | [ref](reference/page.md) |
| `ucli browser page console-logs` | Get console logs from the browser | `ucli browser page console-logs` | [ref](reference/page.md) |
| `ucli browser page wait` | Wait for a specified time in seconds | `ucli browser page wait --time 2` | [ref](reference/page.md) |

## Discover Parameters

Append `--help` to any command for full parameter list:

    ucli browser interact click --help

> **Note**: Use Ref links in the Commands table above to view detailed parameter reference and more examples.

## User Notes

> **MUST READ** [users/skill.md](users/skill.md) for custom workflows and tips.
> **Config**: MCP server settings live in `~/.agents/ucli/servers.yaml` - edit there to take effect.
