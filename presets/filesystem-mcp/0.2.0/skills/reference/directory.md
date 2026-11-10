# Directory Commands

## create — Create a directory

```bash
# Create a single directory
ucli filesystem directory create --path /new/dir

# Create nested directories in one operation
ucli filesystem directory create --path /new/deep/nested/dir
```

## list — List directory contents

```bash
ucli filesystem directory list --path /project
```

## list-sizes — List with size information

```bash
# List sorted by name (default)
ucli filesystem directory list-sizes --path /project

# List sorted by size
ucli filesystem directory list-sizes --path /project --sort-by size
```

Also supports: `--sort-by` (name|size)

## tree — Get recursive directory tree

```bash
# Full tree view
ucli filesystem directory tree --path /project

# Exclude certain patterns
ucli filesystem directory tree --path /project --exclude-patterns '["node_modules","__pycache__"]'
```

Also supports: `--exclude-patterns`

## list-allowed — List accessible directories

```bash
ucli filesystem directory list-allowed
```

Use `ucli filesystem directory <action> --help` for full parameter details.
