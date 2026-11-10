# Auth Commands

## auth — Authorize with AgentOps API key

```bash
# Authorize using API key directly
ucli agentops auth --api-key YOUR_API_KEY

# Authorize using environment variable (AGENTOPS_API_KEY must be set)
ucli agentops auth
```

Also supports: `--api-key` (optional if `AGENTOPS_API_KEY` env var is set)

Use `ucli agentops auth --help` for full parameter details.
