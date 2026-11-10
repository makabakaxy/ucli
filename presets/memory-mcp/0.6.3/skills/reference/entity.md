# Entity Commands

## create — Create entities in the knowledge graph

```bash
# Create a single entity
ucli memory entity create --entities '[{"name": "Alice", "entityType": "Person", "observations": ["Software engineer"]}]'

# Create multiple entities
ucli memory entity create --entities '[{"name": "Alice", "entityType": "Person", "observations": ["Engineer"]}, {"name": "Acme Corp", "entityType": "Organization", "observations": ["Tech company"]}]'
```

## delete — Delete entities and their associated relations

```bash
# Delete a single entity
ucli memory entity delete --entity-names '["Alice"]'

# Delete multiple entities
ucli memory entity delete --entity-names '["Alice", "Bob"]'
```

Use `ucli memory entity <action> --help` for full parameter details.
