# Analyze Commands

## trend — Analyze topic trend

```bash
ucli trendradar analyze trend --topic 'AI'
ucli trendradar analyze trend --topic '特斯拉' --analysis-type lifecycle
ucli trendradar analyze trend --topic 'AI' --analysis-type viral --date-range '{"start":"2025-01-01","end":"2025-01-07"}'
```

Also supports: `--analysis-type` (trend/lifecycle/viral/predict), `--date-range`, `--granularity`, `--spike-threshold`, `--time-window`, `--lookahead-hours`, `--confidence-threshold`

## sentiment — Analyze news sentiment and heat trends

```bash
ucli trendradar analyze sentiment --topic 'AI'
ucli trendradar analyze sentiment --topic '特斯拉' --date-range '{"start":"2025-01-01","end":"2025-01-07"}'
```

Also supports: `--topic`, `--platforms`, `--date-range`, `--limit`, `--sort-by-weight`, `--include-url`

## insights — Data insights across platforms

```bash
ucli trendradar analyze insights --insight-type platform_compare --topic '人工智能'
ucli trendradar analyze insights --insight-type platform_activity --date-range '{"start":"2025-01-01","end":"2025-01-07"}'
ucli trendradar analyze insights --insight-type keyword_cooccur --top-n 15
```

Also supports: `--insight-type` (platform_compare/platform_activity/keyword_cooccur), `--topic`, `--date-range`, `--min-frequency`, `--top-n`

## compare — Compare two time periods

```bash
ucli trendradar analyze compare --period1 last_week --period2 this_week
ucli trendradar analyze compare --period1 last_month --period2 this_month --compare-type topic_shift
ucli trendradar analyze compare --period1 '{"start":"2025-01-01","end":"2025-01-07"}' --period2 '{"start":"2025-01-08","end":"2025-01-14"}' --topic '人工智能'
```

Also supports: `--topic`, `--compare-type` (overview/topic_shift/platform_activity), `--platforms`, `--top-n`

Use `ucli trendradar analyze <cmd> --help` for full parameter details.
