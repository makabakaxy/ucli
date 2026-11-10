---
name: ps
description: Control Adobe Photoshop via CLI — documents, layers, text, selections, masks, filters, adjustments, generative AI and export recipes. Use when user needs to edit images, compose layers, retouch, or export assets in Photoshop.
source_version: "1.7.37"
source_cli_hash: "1aa67726"
generated_at: "2026-11-09T10:47:56.608791+00:00"
---

# ps (via ucli)


## Shortcuts

- `ucli ps <group> <cmd>` (no aliases or shortcuts defined)

## Commands

### Document & App
| Command | Description | Example | Ref |
|---|---|---|---|
| `ucli ps document create` | New empty document | `ucli ps document create --width 1920 --height 1080` | [ref](reference/document.md) |
| `ucli ps document open` | Open image file | `ucli ps document open --filePath /tmp/photo.jpg` | [ref](reference/document.md) |
| `ucli ps document export` | Export PNG/JPEG/WebP/AVIF | | [ref](reference/document.md) |
| `ucli ps app ping` | Check Photoshop responds | | [ref](reference/app.md) |

### Layers & Text
| Command | Description | Example | Ref |
|---|---|---|---|
| `ucli ps layer create` | New empty layer | | [ref](reference/layer.md) |
| `ucli ps layer list` | List layers | | [ref](reference/layer.md) |
| `ucli ps layer set opacity` | Set opacity | | [ref](reference/layer-set.md) |
| `ucli ps text create` | New text layer | `ucli ps text create --text 'Hello' --fontSize 48` | [ref](reference/text.md) |
| `ucli ps fill color` | Solid fill | `ucli ps fill color --red 255 --green 0 --blue 0` | [ref](reference/fill.md) |

### Selection, Mask, Filter, Adjust
| Command | Description | Example | Ref |
|---|---|---|---|
| `ucli ps selection subject` | Select main subject | | [ref](reference/selection.md) |
| `ucli ps mask create` | Mask from selection | | [ref](reference/mask.md) |
| `ucli ps filter blur` | Gaussian blur | | [ref](reference/filter.md) |
| `ucli ps adjust hue-saturation` | Hue/saturation/lightness | | [ref](reference/adjust.md) |

### AI & Recipes
| Command | Description | Example | Ref |
|---|---|---|---|
| `ucli ps ai fill` | Generative Fill | | [ref](reference/ai.md) |
| `ucli ps ai generate-image` | Image from prompt | | [ref](reference/ai.md) |
| `ucli ps recipe remove-background` | Isolate subject | | [ref](reference/recipe.md) |
| `ucli ps recipe prepare-for-web` | Web-optimized export | | [ref](reference/recipe.md) |

Also: `history`, `artboard`, `dataset`, `smart-object` — see reference/.

## Discover Parameters

Append `--help` to any command for full parameter list:

    ucli ps layer create --help

## User Notes

> Read `users/skill.md` if it exists for custom workflows and tips.
> **Config**: MCP server settings live in `~/.agents/ucli/servers.yaml` - edit there to take effect.

## Connection and Capabilities

- Run `ucli ps app ping` once at session start. If it fails, resolve the connection before editing.
- Use `ucli ps app capabilities` to check optional features. Neural Filters need the UXP bridge plugin running in Photoshop.
- Run `ucli doctor ps` to check installation and Photoshop readiness.
- For long operations, set `UCLI_TIMEOUT=700` before running the command. Do not retry a timed-out edit until you check its result in Photoshop.
