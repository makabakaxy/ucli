# Page Commands

## navigate — Navigate to a URL

```bash
ucli puppeteer page navigate --url https://example.com
ucli puppeteer page navigate --url https://example.com --launch-options '{"headless": true}'
```

Also supports: `--launch-options`, `--allow-dangerous`

## screenshot — Take a screenshot of the current page or element

```bash
# Full page screenshot
ucli puppeteer page screenshot --name my-screenshot

# Screenshot a specific element
ucli puppeteer page screenshot --name header-shot --selector "header"

# Screenshot with custom dimensions
ucli puppeteer page screenshot --name wide-shot --width 1280 --height 720
```

Also supports: `--selector`, `--width`, `--height`, `--encoded`

## evaluate — Execute JavaScript in the browser console

```bash
# Get page title
ucli puppeteer page evaluate --script "document.title"

# Get element count
ucli puppeteer page evaluate --script "document.querySelectorAll('a').length"

# Scroll to bottom
ucli puppeteer page evaluate --script "window.scrollTo(0, document.body.scrollHeight)"
```

Use `ucli puppeteer page <action> --help` for full parameter details.
