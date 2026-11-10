# News Commands

## get — Get latest crawled news

```bash
ucli trendradar news get
ucli trendradar news get --platforms zhihu weibo --limit 50
ucli trendradar news get --limit 100 --include-url true
```

Also supports: `--platforms`, `--limit`, `--include-url`

## search — Search news with multiple modes

```bash
ucli trendradar news search --query 'AI'
ucli trendradar news search --query '特斯拉' --include-rss true
ucli trendradar news search --query 'AI' --date-range '{"start":"2025-01-01","end":"2025-01-07"}' --limit 20
```

Also supports: `--search-mode` (keyword/fuzzy/entity), `--date-range`, `--platforms`, `--limit`, `--sort-by`, `--threshold`, `--include-url`, `--include-rss`, `--rss-limit`

## by-date — Get news by date range

```bash
ucli trendradar news by-date --date-range '{"start":"2025-01-01","end":"2025-01-07"}'
ucli trendradar news by-date --date-range '昨天' --platforms zhihu
```

Also supports: `--date-range`, `--platforms`, `--limit`, `--include-url`

## find-related — Find related news by reference title

```bash
ucli trendradar news find-related --reference-title '特斯拉降价'
ucli trendradar news find-related --reference-title 'AI突破' --date-range 'last_week' --limit 20
```

Also supports: `--date-range`, `--threshold`, `--limit`, `--include-url`

## aggregate — Cross-platform news aggregation (dedup)

```bash
ucli trendradar news aggregate
ucli trendradar news aggregate --similarity-threshold 0.8
```

Also supports: `--date-range`, `--platforms`, `--similarity-threshold`, `--limit`, `--include-url`

Use `ucli trendradar news <cmd> --help` for full parameter details.
