---
name: ruflo
description: Manage multi-agent swarms, memory, tasks, hooks, workflows, and browser automation via CLI. Use when spawning agents, storing/searching memory, orchestrating workflows, coordinating hive-minds, or automating browser interactions.
source_version: "3.0.0"
source_cli_hash: "d3fd1093"
generated_at: "2026-04-06T08:38:53.305460+00:00"
---

# ruflo (via ucli)

Multi-agent orchestration, vector memory, task management, and browser automation.

## Shortcuts

No shortcuts configured. Use full form: `ucli ruflo <group> <cmd>`

## Commands

### Agent
| Command | Description | Example | Ref |
|---|---|---|---|
| `ucli ruflo agent spawn` | Spawn a new agent | `ucli ruflo agent spawn --agent-type worker --model sonnet` | [ref](reference/agent.md) |
| `ucli ruflo agent list` | List all agents | `ucli ruflo agent list` | [ref](reference/agent.md) |
| `ucli ruflo agent status` | Get agent status | `ucli ruflo agent status --agent-id agent-1` | [ref](reference/agent.md) |
| `ucli ruflo agent update` | Update agent config | | [ref](reference/agent.md) |
| `ucli ruflo agent terminate` | Terminate an agent | `ucli ruflo agent terminate --agent-id agent-1` | [ref](reference/agent.md) |
| `ucli ruflo agent health` | Check agent health | | [ref](reference/agent.md) |

### Memory
| Command | Description | Example | Ref |
|---|---|---|---|
| `ucli ruflo memory store` | Store value with vector embedding | `ucli ruflo memory store --key mykey --value "data"` | [ref](reference/memory.md) |
| `ucli ruflo memory get` | Retrieve value by key | `ucli ruflo memory get --key mykey` | [ref](reference/memory.md) |
| `ucli ruflo memory search` | Semantic vector search | `ucli ruflo memory search --query "auth patterns"` | [ref](reference/memory.md) |
| `ucli ruflo memory list` | List memory entries | | [ref](reference/memory.md) |
| `ucli ruflo memory delete` | Delete memory entry | `ucli ruflo memory delete --key mykey` | [ref](reference/memory.md) |
| `ucli ruflo memory stats` | Get memory statistics | | [ref](reference/memory.md) |

### Task
| Command | Description | Example | Ref |
|---|---|---|---|
| `ucli ruflo task create` | Create a new task | `ucli ruflo task create --type feature --description "Add login"` | [ref](reference/task.md) |
| `ucli ruflo task list` | List all tasks | `ucli ruflo task list --status pending` | [ref](reference/task.md) |
| `ucli ruflo task status` | Get task status | `ucli ruflo task status --task-id t1` | [ref](reference/task.md) |
| `ucli ruflo task update` | Update task progress | | [ref](reference/task.md) |
| `ucli ruflo task complete` | Mark task complete | `ucli ruflo task complete --task-id t1` | [ref](reference/task.md) |
| `ucli ruflo task assign` | Assign task to agents | | [ref](reference/task.md) |
| `ucli ruflo task cancel` | Cancel a task | | [ref](reference/task.md) |

### Hooks
| Command | Description | Example | Ref |
|---|---|---|---|
| `ucli ruflo hooks pre-task` | Record task start, get agent suggestions | `ucli ruflo hooks pre-task --task-id t1 --description "Fix bug"` | [ref](reference/hooks.md) |
| `ucli ruflo hooks post-task` | Record task completion | `ucli ruflo hooks post-task --task-id t1 --success true` | [ref](reference/hooks.md) |
| `ucli ruflo hooks route` | Route task to optimal agent | `ucli ruflo hooks route --task "implement OAuth"` | [ref](reference/hooks.md) |
| `ucli ruflo hooks pre-edit` | Get context before editing file | `ucli ruflo hooks pre-edit --file-path src/auth.ts` | [ref](reference/hooks.md) |
| `ucli ruflo hooks init` | Initialize hooks in project | `ucli ruflo hooks init --template standard` | [ref](reference/hooks.md) |
| `ucli ruflo hooks metrics` | View learning metrics | | [ref](reference/hooks.md) |

### Hive-Mind
| Command | Description | Example | Ref |
|---|---|---|---|
| `ucli ruflo hive-mind spawn` | Spawn workers and join hive | `ucli ruflo hive-mind spawn --count 3 --role worker` | [ref](reference/hive-mind.md) |
| `ucli ruflo hive-mind init` | Initialize hive-mind collective | `ucli ruflo hive-mind init --topology mesh` | [ref](reference/hive-mind.md) |
| `ucli ruflo hive-mind status` | Get hive-mind status | | [ref](reference/hive-mind.md) |
| `ucli ruflo hive-mind consensus` | Propose or vote on consensus | `ucli ruflo hive-mind consensus --action propose --type config` | [ref](reference/hive-mind.md) |
| `ucli ruflo hive-mind broadcast` | Broadcast to all workers | `ucli ruflo hive-mind broadcast --message "Start phase 2"` | [ref](reference/hive-mind.md) |

### Workflow
| Command | Description | Example | Ref |
|---|---|---|---|
| `ucli ruflo workflow run` | Run workflow from template | `ucli ruflo workflow run --template ci-pipeline` | [ref](reference/workflow.md) |
| `ucli ruflo workflow create` | Create a new workflow | `ucli ruflo workflow create --name my-flow` | [ref](reference/workflow.md) |
| `ucli ruflo workflow list` | List all workflows | | [ref](reference/workflow.md) |
| `ucli ruflo workflow status` | Get workflow status | `ucli ruflo workflow status --workflow-id wf1` | [ref](reference/workflow.md) |
| `ucli ruflo workflow execute` | Execute a workflow | `ucli ruflo workflow execute --workflow-id wf1` | [ref](reference/workflow.md) |

### Claims
| Command | Description | Example | Ref |
|---|---|---|---|
| `ucli ruflo claims claim` | Claim an issue for work | `ucli ruflo claims claim --issue-id 123 --claimant "agent:coder-1:coder"` | [ref](reference/claims.md) |
| `ucli ruflo claims list` | List all claims | | [ref](reference/claims.md) |
| `ucli ruflo claims release` | Release a claim | `ucli ruflo claims release --issue-id 123 --claimant "agent:coder-1:coder"` | [ref](reference/claims.md) |
| `ucli ruflo claims handoff` | Handoff issue to another agent | | [ref](reference/claims.md) |
| `ucli ruflo claims load` | Get agent load info | | [ref](reference/claims.md) |

### Browser
| Command | Description | Example | Ref |
|---|---|---|---|
| `ucli ruflo browser open` | Navigate to URL | `ucli ruflo browser open --url https://example.com` | [ref](reference/browser.md) |
| `ucli ruflo browser snapshot` | Get accessibility tree | | [ref](reference/browser.md) |
| `ucli ruflo browser screenshot` | Capture screenshot | | [ref](reference/browser.md) |
| `ucli ruflo browser click` | Click an element | `ucli ruflo browser click --ref elem-1` | [ref](reference/browser.md) |
| `ucli ruflo browser fill` | Fill an input field | `ucli ruflo browser fill --ref input-1 --value "text"` | [ref](reference/browser.md) |

### Swarm
| Command | Description | Example | Ref |
|---|---|---|---|
| `ucli ruflo swarm init` | Initialize a swarm | `ucli ruflo swarm init --topology hierarchical` | [ref](reference/swarm.md) |
| `ucli ruflo swarm status` | Get swarm status | | [ref](reference/swarm.md) |
| `ucli ruflo swarm health` | Check swarm health | | [ref](reference/swarm.md) |
| `ucli ruflo swarm shutdown` | Shutdown a swarm | | [ref](reference/swarm.md) |

## Discover Parameters

Append `--help` to any command for full parameter list:

    ucli ruflo agent spawn --help

> **Note**: Use Ref links above to view detailed parameter reference and more examples.

## User Notes

> **MUST READ** [users/skill.md](users/skill.md) for custom workflows and tips.
> **Config**: MCP server settings live in `~/.agents/ucli/servers.yaml` - edit there to take effect.
