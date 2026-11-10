# Confluence Page Commands

## get — Get page content by ID or title

```bash
ucli confluence page get --page-id 123456789
ucli confluence page get --title "Meeting Notes" --space-key TEAM
```

Also supports: `--page-id`, `--title`, `--space-key`, `--include-metadata`, `--convert-to-markdown`

## create — Create a new page

```bash
ucli confluence page create --space-key TEAM --title "Meeting Notes" --content "# Notes\n..."
ucli confluence page create --space-key DEV --title "API Design" --content "# API" --parent-id 123456789
```

Also supports: `--parent-id`, `--content-format`, `--enable-heading-anchors`, `--emoji`

## update — Update page content

```bash
ucli confluence page update --page-id 123456789 --title "Updated Notes" --content "# Updated\n..."
```

Also supports: `--is-minor-edit`, `--version-comment`, `--parent-id`, `--content-format`, `--enable-heading-anchors`, `--emoji`

## delete — Delete a page

```bash
ucli confluence page delete --page-id 123456789
```

## move — Move a page to a new parent or space

```bash
ucli confluence page move --page-id 123456789 --target-parent-id 987654321
ucli confluence page move --page-id 123456789 --target-space-key NEWSPACE
```

Also supports: `--target-parent-id`, `--target-space-key`, `--position`

## children — Get child pages

```bash
ucli confluence page children --parent-id 123456789
ucli confluence page children --parent-id 123456789 --limit 25 --include-content
```

Also supports: `--expand`, `--limit`, `--include-content`, `--convert-to-markdown`, `--start`, `--include-folders`

## history — Get a historical version of a page

```bash
ucli confluence page history --page-id 123456789 --version 3
```

Also supports: `--convert-to-markdown`

## diff — Get diff between two versions

```bash
ucli confluence page diff --page-id 123456789 --from-version 1 --to-version 3
```

## views — Get page view statistics

```bash
ucli confluence page views --page-id 123456789
```

Also supports: `--include-title`

## images — Get all images from a page

```bash
ucli confluence page images --content-id 123456789
```

Use `ucli confluence page <action> --help` for full parameter details.
