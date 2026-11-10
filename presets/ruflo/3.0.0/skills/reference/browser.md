# Browser Commands

## open — Navigate to URL

```bash
ucli ruflo browser open --url https://example.com
```

## snapshot — Get accessibility tree snapshot

```bash
ucli ruflo browser snapshot
```

## screenshot — Capture a screenshot

```bash
ucli ruflo browser screenshot
```

## click — Click an element

```bash
ucli ruflo browser click --ref elem-123
```

Also supports: CSS selector via `--selector` (check --help)

## fill — Clear and fill an input

```bash
ucli ruflo browser fill --ref input-1 --value "user@example.com"
```

## type — Type text with key events

```bash
ucli ruflo browser type --ref input-1 --text "search term"
```

## press — Press a keyboard key

```bash
ucli ruflo browser press --key Enter
ucli ruflo browser press --key "Control+A"
```

## get-text — Get text content of element

```bash
ucli ruflo browser get-text --ref elem-1
```

## get-url — Get current page URL

```bash
ucli ruflo browser get-url
```

## get-title — Get current page title

```bash
ucli ruflo browser get-title
```

## eval — Execute JavaScript

```bash
ucli ruflo browser eval --script "document.title"
```

## back / forward / reload

```bash
ucli ruflo browser back
ucli ruflo browser forward
ucli ruflo browser reload
```

## close — Close browser session

```bash
ucli ruflo browser close
```

## select — Select dropdown option

```bash
ucli ruflo browser select --ref select-1 --value "option-value"
```

## scroll — Scroll the page

```bash
ucli ruflo browser scroll --direction down --amount 300
```

Use `ucli ruflo browser <action> --help` for full parameter details.
