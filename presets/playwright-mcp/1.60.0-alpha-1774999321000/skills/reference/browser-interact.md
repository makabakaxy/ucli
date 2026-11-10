# Browser Interact Commands

## click — Click an element on the page

```bash
# Click by element ref (get ref from snapshot)
ucli playwright browser interact click --ref e1

# Right-click
ucli playwright browser interact click --ref e1 --button right

# Double-click
ucli playwright browser interact click --ref e1 --double-click
```

Also supports: `--element`, `--button`, `--double-click`, `--modifiers`

## type — Type text into an editable element

```bash
ucli playwright browser interact type --ref e1 --text "hello world"

# Submit after typing (press Enter)
ucli playwright browser interact type --ref e1 --text "search query" --submit
```

Also supports: `--element`, `--submit`, `--slowly`

## fill-form — Fill multiple form fields at once

```bash
ucli playwright browser interact fill-form --fields '[{"name":"Username","type":"textbox","ref":"e1","value":"user@example.com"},{"name":"Password","type":"textbox","ref":"e2","value":"secret"}]'
```

Required: `--fields` (JSON array with name, type, ref, value per field)

## hover — Hover over an element

```bash
ucli playwright browser interact hover --ref e1
```

Also supports: `--element`

## press-key — Press a keyboard key

```bash
ucli playwright browser interact press-key --key Enter
ucli playwright browser interact press-key --key Escape
ucli playwright browser interact press-key --key ArrowDown
```

## select-option — Select an option in a dropdown

```bash
ucli playwright browser interact select-option --ref e1 --values '["Option A"]'

# Select multiple options
ucli playwright browser interact select-option --ref e1 --values '["Option A","Option B"]'
```

Also supports: `--element`

## drag — Drag and drop between two elements

```bash
ucli playwright browser interact drag --start-element "source item" --start-ref e1 --end-element "target area" --end-ref e2
```

Required: `--start-element`, `--start-ref`, `--end-element`, `--end-ref`

Use `ucli playwright browser interact <cmd> --help` for full parameter details.
