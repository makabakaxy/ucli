---
name: filesystem-mcp
description: Read, write, edit, move, and search files and directories via CLI. Use when user needs to access file contents, manage directory structures, or search for files by pattern.
source_version: "0.2.0"
source_cli_hash: "6687ec79"
generated_at: "2026-04-06T09:00:48.172488+00:00"
---

# filesystem-mcp (via ucli)

Read, write, edit, move, and search files and directories via CLI.

## Shortcuts

- `ucli filesystem <cmd>` (alias for `ucli filesystem-mcp`)

## Commands

### File
| Command | Description | Example | Ref |
|---|---|---|---|
| `ucli filesystem file get` | Read text file contents | `ucli filesystem file get --path /path/to/file.txt`<br>`ucli filesystem file get --path /path/to/file.txt --head 50` | [ref](reference/file.md) |
| `ucli filesystem file write` | Create or overwrite a file | `ucli filesystem file write --path /path/to/file.txt --content 'Hello World'` | [ref](reference/file.md) |
| `ucli filesystem file edit` | Make line-based edits to a file | `ucli filesystem file edit --path /path/to/file.txt --edits '[{"oldText":"foo","newText":"bar"}]'` | [ref](reference/file.md) |
| `ucli filesystem file search` | Search files by glob pattern | `ucli filesystem file search --path /project --pattern '**/*.py'` | [ref](reference/file.md) |
| `ucli filesystem file get-multiple` | Read multiple files at once | `ucli filesystem file get-multiple --paths '["file1.txt","file2.txt"]'` | [ref](reference/file.md) |
| `ucli filesystem file get-media` | Read image/audio as base64 | `ucli filesystem file get-media --path /path/to/image.png` | [ref](reference/file.md) |
| `ucli filesystem file move` | Move or rename a file | `ucli filesystem file move --source /old/path --destination /new/path` | [ref](reference/file.md) |
| `ucli filesystem file info` | Get file metadata | `ucli filesystem file info --path /path/to/file.txt` | [ref](reference/file.md) |

### Directory
| Command | Description | Example | Ref |
|---|---|---|---|
| `ucli filesystem directory create` | Create a directory | `ucli filesystem directory create --path /new/dir` | [ref](reference/directory.md) |
| `ucli filesystem directory list` | List directory contents | `ucli filesystem directory list --path /project` | [ref](reference/directory.md) |
| `ucli filesystem directory tree` | Get recursive directory tree | `ucli filesystem directory tree --path /project` | [ref](reference/directory.md) |
| `ucli filesystem directory list-sizes` | List with size information | `ucli filesystem directory list-sizes --path /project` | [ref](reference/directory.md) |
| `ucli filesystem directory list-allowed` | List accessible directories | `ucli filesystem directory list-allowed` | [ref](reference/directory.md) |

## Discover Parameters

Append `--help` to any command for full parameter list:

    ucli filesystem file get --help

> **Note**: Use Ref links in the Commands table above to view detailed parameter reference and more examples.

## User Notes

> **MUST READ** [users/skill.md](users/skill.md) for custom workflows and tips.
> **Config**: MCP server settings live in `~/.agents/ucli/servers.yaml` - edit there to take effect.
