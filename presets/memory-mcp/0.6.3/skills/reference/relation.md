# Relation Commands

## create — Create relations between entities

```bash
# Create a single relation
ucli memory relation create --relations '[{"from": "Alice", "to": "Bob", "relationType": "knows"}]'

# Create multiple relations
ucli memory relation create --relations '[{"from": "Alice", "to": "Acme Corp", "relationType": "works_at"}, {"from": "Bob", "to": "Acme Corp", "relationType": "works_at"}]'
```

## delete — Delete relations from the knowledge graph

```bash
# Delete a specific relation
ucli memory relation delete --relations '[{"from": "Alice", "to": "Bob", "relationType": "knows"}]'

# Delete multiple relations
ucli memory relation delete --relations '[{"from": "Alice", "to": "Acme Corp", "relationType": "works_at"}, {"from": "Bob", "to": "Acme Corp", "relationType": "works_at"}]'
```

Use `ucli memory relation <action> --help` for full parameter details.
