# Node Commands

## search — Search for nodes based on a query

```bash
# Search by entity name
ucli memory node search --query "Alice"

# Search by entity type
ucli memory node search --query "Person"

# Search by observation content
ucli memory node search --query "engineer"
```

Matches against entity names, types, and observation content.

## get — Get specific nodes by their names

```bash
# Get a single node
ucli memory node get --names '["Alice"]'

# Get multiple nodes
ucli memory node get --names '["Alice", "Bob", "Acme Corp"]'
```

Use `ucli memory node <action> --help` for full parameter details.
