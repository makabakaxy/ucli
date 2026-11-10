# RSS Commands

## list — Get latest RSS subscription data

```bash
ucli trendradar rss list
ucli trendradar rss list --days 7 --feeds hacker-news 36kr
ucli trendradar rss list --days 30 --limit 100 --include-summary true
```

Also supports: `--feeds`, `--days`, `--limit`, `--include-summary`

## search — Search RSS by keyword

```bash
ucli trendradar rss search --keyword 'machine learning'
ucli trendradar rss search --keyword 'AI' --feeds hacker-news --days 14
```

Also supports: `--feeds`, `--days`, `--limit`, `--include-summary`

## status — Get RSS feed status and statistics

```bash
ucli trendradar rss status
```

No parameters required.

Use `ucli trendradar rss <cmd> --help` for full parameter details.
