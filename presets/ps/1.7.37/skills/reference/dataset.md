# Data set operations

## list — List data sets in the document

```bash
ucli ps dataset list --document-id 1
```

## import — Import a data sets XML file

```bash
ucli ps dataset import --xml-path /tmp/file.png --document-id 1
```

## generate — Export one file per data set

```bash
ucli ps dataset generate --output-dir /tmp/out --document-id 1
```

Also supports: `--format`, `--dataset-names`

Use `ucli ps dataset <action> --help` for full parameter details.
