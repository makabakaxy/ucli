# Memory Commands

## write — Write project info to a named memory

```bash
# Write a simple memory
ucli serena memory write --memory-name 'auth/logic' --content 'Auth uses JWT tokens stored in Redis'

# Write with topic organization
ucli serena memory write --memory-name 'global/python/style_guide' --content 'Use Black formatter, max line length 88'
```

Also supports: `--max-chars`

## get — Read a memory

```bash
ucli serena memory get --memory-name 'auth/logic'
```

## list — List available memories

```bash
# List all memories
ucli serena memory list

# Filter by topic
ucli serena memory list --topic auth
```

Also supports: `--topic`

## update — Edit memory via pattern replacement

```bash
# Literal replacement
ucli serena memory update --memory-name 'auth/logic' --needle 'Redis' --repl 'PostgreSQL' --mode literal

# Regex replacement
ucli serena memory update --memory-name 'auth/logic' --needle 'JWT.*tokens' --repl 'session cookies' --mode regex
```

Also supports: `--allow-multiple-occurrences`

## rename — Rename or move a memory

```bash
ucli serena memory rename --old-name 'auth/logic' --new-name 'security/auth/logic'
```

## delete — Delete a memory

```bash
ucli serena memory delete --memory-name 'auth/logic'
```

Use `ucli serena memory <action> --help` for full parameter details.
