# Observation Commands

## add — Add observations to existing entities

```bash
# Add observations to a single entity
ucli memory observation add --observations '[{"entityName": "Alice", "contents": ["Joined company in 2024"]}]'

# Add observations to multiple entities
ucli memory observation add --observations '[{"entityName": "Alice", "contents": ["Promoted to senior"]}, {"entityName": "Bob", "contents": ["Started new project"]}]'
```

## delete — Delete specific observations from entities

```bash
# Delete an observation from an entity
ucli memory observation delete --deletions '[{"entityName": "Alice", "observations": ["Old job title"]}]'

# Delete observations from multiple entities
ucli memory observation delete --deletions '[{"entityName": "Alice", "observations": ["Stale fact"]}, {"entityName": "Bob", "observations": ["Outdated note"]}]'
```

Use `ucli memory observation <action> --help` for full parameter details.
