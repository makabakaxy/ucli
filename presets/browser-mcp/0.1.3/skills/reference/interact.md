# Interact Commands

## click — Click on a web page element

```bash
# Click a button (get ref from page snapshot first)
ucli browser interact click --element "Submit button" --ref e123

# Click a link
ucli browser interact click --element "Sign in link" --ref e456
```

## type — Type text into an editable element

```bash
# Type and submit (press Enter)
ucli browser interact type --element "Search box" --ref e101 --text "hello world" --submit true

# Type without submitting
ucli browser interact type --element "Username field" --ref e102 --text "admin" --submit false
```

## select-option — Select an option in a dropdown

```bash
ucli browser interact select-option --element "Country dropdown" --ref e200 --values '["US"]'

# Multi-select
ucli browser interact select-option --element "Tags" --ref e201 --values '["tag1", "tag2"]'
```

## hover — Hover over a page element

```bash
ucli browser interact hover --element "Navigation menu" --ref e300
```

## press-key — Press a key on the keyboard

```bash
ucli browser interact press-key --key "Enter"
ucli browser interact press-key --key "Escape"
ucli browser interact press-key --key "ArrowDown"
```

> **Tip**: Always run `ucli browser page snapshot` first to get element refs before interacting.

Use `ucli browser interact <action> --help` for full parameter details.
