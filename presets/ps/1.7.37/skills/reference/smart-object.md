# Smart object operations

## convert — Convert a layer to a smart object

```bash
ucli ps smart-object convert --document-id 1
```

Also supports: `--layer-name`

## replace — Replace smart object contents from a file

```bash
ucli ps smart-object replace --file-path /tmp/file.png --document-id 1
```

Also supports: `--layer-name`

## edit — Open a smart object for editing

```bash
ucli ps smart-object edit --document-id 1
```

Also supports: `--layer-name`

## copy — Create an independent smart object copy

```bash
ucli ps smart-object copy --document-id 1
```

Also supports: `--layer-name`

Use `ucli ps smart-object <action> --help` for full parameter details.
