# Artboard operations

## list — List artboards in the document

```bash
ucli ps artboard list --document-id 1
```

## create — Create a new artboard

```bash
ucli ps artboard create --width 1920 --height 1080 --document-id 1
```

Also supports: `--name`, `--left`, `--top`

## activate — Select an artboard

```bash
ucli ps artboard activate --document-id 1
```

Also supports: `--artboard-id`, `--name`

## export — Export all artboards to a folder

```bash
ucli ps artboard export --folder /tmp/out --document-id 1
```

Also supports: `--format`, `--quality`

Use `ucli ps artboard <action> --help` for full parameter details.
