# System Commands

## status — Get system running status and health info

```bash
ucli trendradar system status
```

No parameters required.

## config — Get current system configuration

```bash
ucli trendradar system config
ucli trendradar system config --section crawler
```

Also supports: `--section` (all/crawler/push/keywords/weights)

## version — Check for version updates

```bash
ucli trendradar system version
ucli trendradar system version --proxy-url 'http://127.0.0.1:7890'
```

Also supports: `--proxy-url`

## crawl — Manually trigger a crawl task

```bash
ucli trendradar system crawl
ucli trendradar system crawl --platforms zhihu weibo
ucli trendradar system crawl --save-to-local true
```

Also supports: `--platforms`, `--save-to-local`, `--include-url`

## dates — List available date ranges

```bash
ucli trendradar system dates
ucli trendradar system dates --source local
```

Also supports: `--source` (local/remote/both)

Use `ucli trendradar system <cmd> --help` for full parameter details.
