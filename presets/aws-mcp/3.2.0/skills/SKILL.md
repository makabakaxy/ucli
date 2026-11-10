---
name: "aws-mcp"
description: Execute and suggest AWS CLI commands across all AWS services via natural language or direct CLI syntax. Use when user needs to manage EC2, S3, IAM, Lambda, RDS, or any other AWS resource.
source_version: "3.2.0"
source_cli_hash: "383d90d9"
generated_at: "2026-04-06T09:17:32.833960+00:00"
---

# aws-mcp (via ucli)

Execute AWS CLI commands or get suggestions for AWS operations via natural language.

## Shortcuts

- `ucli aws <cmd>` (alias for `ucli aws-mcp <cmd>`)

## Commands

### AWS
| Command | Description | Example | Ref |
|---|---|---|---|
| `ucli aws call` | Execute AWS CLI commands directly | `ucli aws call --cli-command 'aws s3api list-buckets --region us-east-1'`<br>`ucli aws call --cli-command 'aws ec2 describe-instances --region us-east-1'` | [ref](reference/aws.md) |
| `ucli aws suggest` | Suggest AWS CLI commands from natural language | `ucli aws suggest --query 'List all running EC2 instances in us-east-1'`<br>`ucli aws suggest --query 'Create an S3 bucket with versioning enabled'` | [ref](reference/aws.md) |

## Discover Parameters

Append `--help` to any command for full parameter list:

    ucli aws call --help

> **Note**: Use Ref links in the Commands table above to view detailed parameter reference and more examples.

## User Notes

> **MUST READ** [users/skill.md](users/skill.md) for custom workflows and tips.
> **Config**: MCP server settings live in `~/.agents/ucli/servers.yaml` - edit there to take effect.
