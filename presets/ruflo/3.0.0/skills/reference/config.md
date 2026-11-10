# Config Commands

## get — Get a configuration value

```bash
ucli ruflo config get --key model.default
ucli ruflo config get --key memory.namespace --scope project
```

Also supports: `--scope` (scopes: project, user, system)

## update — Set a configuration value

```bash
ucli ruflo config update --key model.default --value sonnet
ucli ruflo config update --key memory.ttl --value 3600 --scope project
```

Also supports: `--scope`

## list — List all configuration values

```bash
ucli ruflo config list
ucli ruflo config list --scope project --prefix model
```

Also supports: `--scope`, `--prefix`, `--include-defaults`

## reset — Reset configuration to defaults

```bash
ucli ruflo config reset
ucli ruflo config reset --key model.default --scope project
```

Also supports: `--scope`, `--key`

## download — Export configuration to JSON

```bash
ucli ruflo config download
ucli ruflo config download --scope project --include-defaults true
```

Also supports: `--scope`, `--include-defaults`

## upload — Import configuration from JSON

```bash
ucli ruflo config upload --config '{"model": {"default": "sonnet"}}'
ucli ruflo config upload --config '{"memory": {"ttl": 3600}}' --merge true
```

Also supports: `--scope`, `--merge`

Use `ucli ruflo config <action> --help` for full parameter details.
