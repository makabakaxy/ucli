# Memory Commands

## store — Store value with vector embedding

```bash
ucli ruflo memory store --key mykey --value "some data to remember"
ucli ruflo memory store --key auth-pattern --value "JWT refresh token pattern" --namespace patterns
```

Also supports: `--namespace`, `--tags`, `--ttl`, `--upsert`

## get — Retrieve a value by key

```bash
ucli ruflo memory get --key mykey
ucli ruflo memory get --key auth-pattern --namespace patterns
```

Also supports: `--namespace`

## search — Semantic vector search (HNSW-powered)

```bash
ucli ruflo memory search --query "authentication patterns"
ucli ruflo memory search --query "caching strategies" --limit 5 --threshold 0.5
```

Also supports: `--namespace`, `--limit`, `--threshold`

## list — List memory entries

```bash
ucli ruflo memory list
ucli ruflo memory list --namespace patterns --limit 20
```

Also supports: `--namespace`, `--limit`, `--offset`

## delete — Delete a memory entry

```bash
ucli ruflo memory delete --key mykey
ucli ruflo memory delete --key auth-pattern --namespace patterns
```

Also supports: `--namespace`

## stats — Get memory storage statistics

```bash
ucli ruflo memory stats
```

## migrate — Migrate to sql.js backend

```bash
ucli ruflo memory migrate
ucli ruflo memory migrate --force true
```

Use `ucli ruflo memory <action> --help` for full parameter details.
