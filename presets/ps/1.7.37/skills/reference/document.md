# Document operations

## create — Create a new empty document

```bash
ucli ps document create --width 1920 --height 1080
```

Also supports: `--width`, `--height`, `--resolution`, `--color-mode`, `--document-id`

## open — Open an image file as a new document

```bash
ucli ps document open --filePath /tmp/photo.jpg
```

Also supports: `--document-id`

## get — Get info about the active document

```bash
ucli ps document get --document-id 1
```

## list — List all open documents

```bash
ucli ps document list
```

## activate — Switch the active document tab

```bash
ucli ps document activate
```

Also supports: `--document-id`, `--index`, `--document-name`

## save — Save the active document to disk

```bash
ucli ps document save --path /tmp/file.png --document-id 1
```

Also supports: `--format`, `--quality`

## close — Close a document tab

```bash
ucli ps document close --document-id 1
```

Also supports: `--save`

## resize — Resample the document to new pixel dimensions

```bash
ucli ps document resize --width 1920 --height 1080 --document-id 1
```

## crop — Crop the document to a pixel rectangle

```bash
ucli ps document crop --left 10 --top 10 --right 10 --bottom 10 --document-id 1
```

## flatten — Flatten the document into a single background layer

```bash
ucli ps document flatten --document-id 1
```

## place — Place an image file as a new layer

```bash
ucli ps document place --file-path /tmp/file.png --document-id 1
```

Also supports: `--x`, `--y`

## export — Export a copy as PNG, JPEG, WebP or AVIF

```bash
ucli ps document export --path /tmp/file.png --document-id 1
```

Also supports: `--format`, `--quality`, `--artboard-id`

## stack — Load images into a smart object with a stack mode

```bash
ucli ps document stack --files '[]' --document-id 1
```

Also supports: `--mode`

Use `ucli ps document <action> --help` for full parameter details.
