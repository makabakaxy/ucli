---
name: "zereight/gitlab-mcp"
description: Manage GitLab repos, MRs, issues, pipelines, deployments, and releases via CLI. Use when user needs to create/search repos, review/merge MRs, manage issues, or run pipelines.
source_version: "2.0.35"
source_cli_hash: "a0ad80a2"
generated_at: "2026-04-05T10:43:44.524105+00:00"
---

# zereight/gitlab-mcp (via ucli)

Manage GitLab projects, merge requests, issues, pipelines, and releases via CLI.

## Shortcuts

- `ucli gitlab <cmd>` (server alias)

## Commands

### Merge Requests
| Command | Description | Example | Ref |
|---|---|---|---|
| `ucli gitlab mr create` | Create a new MR | `ucli gitlab mr create --title "Fix bug" --source-branch feature/fix --target-branch main` | [ref](reference/mr.md) |
| `ucli gitlab mr get` | Get MR details | `ucli gitlab mr get --project-id my-group/my-repo --merge-request-iid 42` | [ref](reference/mr.md) |
| `ucli gitlab mr list` | List merge requests | `ucli gitlab mr list --project-id my-group/my-repo` | [ref](reference/mr.md) |
| `ucli gitlab mr update` | Update a merge request | | [ref](reference/mr.md) |
| `ucli gitlab mr merge` | Merge a merge request | `ucli gitlab mr merge --project-id my-group/my-repo --merge-request-iid 42` | [ref](reference/mr.md) |
| `ucli gitlab mr diff get` | Get MR full diff | | [ref](reference/mr.md) |
| `ucli gitlab mr diff changed-files` | List changed file paths | `ucli gitlab mr diff changed-files --project-id my-group/repo --merge-request-iid 42` | [ref](reference/mr.md) |
| `ucli gitlab mr approval approve` | Approve a merge request | | [ref](reference/mr.md) |

### Issues
| Command | Description | Example | Ref |
|---|---|---|---|
| `ucli gitlab issue create` | Create a new issue | `ucli gitlab issue create --title "Fix memory leak" --project-id my-group/my-repo` | [ref](reference/issue.md) |
| `ucli gitlab issue get` | Get issue details | `ucli gitlab issue get --project-id my-group/my-repo --issue-iid 10` | [ref](reference/issue.md) |
| `ucli gitlab issue list` | List issues | `ucli gitlab issue list --project-id my-group/my-repo` | [ref](reference/issue.md) |
| `ucli gitlab issue my` | List my assigned issues | `ucli gitlab issue my` | [ref](reference/issue.md) |
| `ucli gitlab issue update` | Update an issue | | [ref](reference/issue.md) |
| `ucli gitlab issue delete` | Delete an issue | | [ref](reference/issue.md) |

### Repositories & Files
| Command | Description | Example | Ref |
|---|---|---|---|
| `ucli gitlab repo search` | Search for projects | `ucli gitlab repo search --search my-project` | [ref](reference/repo.md) |
| `ucli gitlab repo get` | Get project details | `ucli gitlab repo get --project-id my-group/my-repo` | [ref](reference/repo.md) |
| `ucli gitlab repo create` | Create a new project | `ucli gitlab repo create --name my-new-repo --visibility private` | [ref](reference/repo.md) |
| `ucli gitlab repo file get` | Get file contents | `ucli gitlab repo file get --project-id my-group/my-repo --file-path src/main.go` | [ref](reference/repo.md) |
| `ucli gitlab repo file update` | Create or update a file | | [ref](reference/repo.md) |
| `ucli gitlab repo tree` | List files/dirs in repo | | [ref](reference/repo.md) |

### Pipelines & CI
| Command | Description | Example | Ref |
|---|---|---|---|
| `ucli gitlab pipeline list` | List pipelines | `ucli gitlab pipeline list --project-id my-group/my-repo` | [ref](reference/pipeline.md) |
| `ucli gitlab pipeline get` | Get pipeline details | | [ref](reference/pipeline.md) |
| `ucli gitlab pipeline create` | Trigger a new pipeline | | [ref](reference/pipeline.md) |
| `ucli gitlab pipeline retry` | Retry a pipeline | | [ref](reference/pipeline.md) |
| `ucli gitlab pipeline job output` | Get job log output | | [ref](reference/pipeline.md) |
| `ucli gitlab pipeline job list` | List pipeline jobs | | [ref](reference/pipeline.md) |

### Releases & Other
| Command | Description | Example | Ref |
|---|---|---|---|
| `ucli gitlab release create` | Create a release | | [ref](reference/release.md) |
| `ucli gitlab release list` | List releases | | [ref](reference/release.md) |
| `ucli gitlab milestone create` | Create a milestone | | [ref](reference/misc.md) |
| `ucli gitlab wiki create` | Create a wiki page | | [ref](reference/wiki.md) |
| `ucli gitlab deployment list` | List deployments | | [ref](reference/misc.md) |
| `ucli gitlab branch create` | Create a branch | | [ref](reference/misc.md) |

## Discover Parameters

Append `--help` to any command for full parameter list:

    ucli gitlab mr create --help

> **Note**: Use Ref links in the Commands table above for detailed parameter reference and more examples.

## User Notes

> **MUST READ** [users/skill.md](users/skill.md) for custom workflows and tips.
> **Config**: MCP server settings live in `~/.agents/ucli/servers.yaml` - edit there to take effect.
