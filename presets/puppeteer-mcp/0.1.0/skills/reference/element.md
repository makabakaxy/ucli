# Element Commands

## click — Click an element on the page

```bash
ucli puppeteer element click --selector "#submit-btn"
ucli puppeteer element click --selector "button[type='submit']"
```

## fill — Fill out an input field

```bash
ucli puppeteer element fill --selector "#username" --value "john"
ucli puppeteer element fill --selector "input[name='email']" --value "user@example.com"
```

## select — Select a dropdown option

```bash
ucli puppeteer element select --selector "#country" --value "US"
ucli puppeteer element select --selector "select[name='role']" --value "admin"
```

## hover — Hover over an element

```bash
ucli puppeteer element hover --selector ".dropdown-menu"
ucli puppeteer element hover --selector "nav .menu-item:first-child"
```

Use `ucli puppeteer element <action> --help` for full parameter details.
