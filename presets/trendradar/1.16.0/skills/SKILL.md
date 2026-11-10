---
name: trendradar
description: Monitor trending news, analyze topics, aggregate cross-platform content, and send notifications via CLI. Use when user needs to get latest news, search trends, analyze sentiment, compare periods, or generate reports.
source_version: "1.16.0"
source_cli_hash: "e137b324"
generated_at: "2026-04-06T08:19:01.222788+00:00"
---

# trendradar (via ucli)

Monitor trending news and analyze cross-platform content via CLI.

## Shortcuts

No shortcuts configured. Use full form: `ucli trendradar <group> <cmd>`

## Commands

### News
| Command | Description | Example | Ref |
|---|---|---|---|
| `ucli trendradar news get` | Get latest crawled news | `ucli trendradar news get --platforms zhihu weibo --limit 50` | [ref](reference/news.md) |
| `ucli trendradar news search` | Search news (keyword/fuzzy/entity) | `ucli trendradar news search --query 'AI'`<br>`ucli trendradar news search --query '特斯拉' --include-rss true` | [ref](reference/news.md) |
| `ucli trendradar news by-date` | Get news by date range | `ucli trendradar news by-date --date-range '{"start":"2025-01-01","end":"2025-01-07"}'` | [ref](reference/news.md) |
| `ucli trendradar news find-related` | Find related news by title | `ucli trendradar news find-related --reference-title '特斯拉降价'` | [ref](reference/news.md) |
| `ucli trendradar news aggregate` | Cross-platform dedup aggregation | | [ref](reference/news.md) |
| `ucli trendradar trending list` | List trending topics by frequency | `ucli trendradar trending list --top-n 20 --extract-mode auto_extract` | [ref](reference/trending.md) |

### Analyze
| Command | Description | Example | Ref |
|---|---|---|---|
| `ucli trendradar analyze trend` | Analyze topic trend/lifecycle/viral | `ucli trendradar analyze trend --topic 'AI' --analysis-type trend`<br>`ucli trendradar analyze trend --topic '特斯拉' --analysis-type lifecycle` | [ref](reference/analyze.md) |
| `ucli trendradar analyze sentiment` | Analyze sentiment and heat trends | `ucli trendradar analyze sentiment --topic 'AI'` | [ref](reference/analyze.md) |
| `ucli trendradar analyze insights` | Data insights across platforms | `ucli trendradar analyze insights --insight-type platform_compare --topic '人工智能'` | [ref](reference/analyze.md) |
| `ucli trendradar analyze compare` | Compare two time periods | `ucli trendradar analyze compare --period1 last_week --period2 this_week` | [ref](reference/analyze.md) |

### Report & Article
| Command | Description | Example | Ref |
|---|---|---|---|
| `ucli trendradar report generate` | Generate daily/weekly summary report | `ucli trendradar report generate --report-type daily` | [ref](reference/report.md) |
| `ucli trendradar article read` | Read article URL as Markdown | `ucli trendradar article read --url 'https://example.com/news/123'` | [ref](reference/article.md) |
| `ucli trendradar article batch-read` | Batch read multiple article URLs | | [ref](reference/article.md) |

### RSS
| Command | Description | Example | Ref |
|---|---|---|---|
| `ucli trendradar rss list` | Get latest RSS subscription data | `ucli trendradar rss list --days 7 --feeds hacker-news 36kr` | [ref](reference/rss.md) |
| `ucli trendradar rss search` | Search RSS by keyword | `ucli trendradar rss search --keyword 'machine learning' --days 14` | [ref](reference/rss.md) |

### Notification & Utils
| Command | Description | Example | Ref |
|---|---|---|---|
| `ucli trendradar notification send` | Send to configured channels | `ucli trendradar notification send --message '**测试**' --channels feishu dingtalk` | [ref](reference/notification.md) |
| `ucli trendradar date resolve` | Resolve natural language date expression | `ucli trendradar date resolve --expression '本周'` | [ref](reference/date.md) |
| `ucli trendradar system status` | Get system health status | | [ref](reference/system.md) |
| `ucli trendradar storage sync` | Sync data from remote storage | `ucli trendradar storage sync --days 30` | [ref](reference/storage.md) |

## Discover Parameters

Append `--help` to any command for full parameter list:

    ucli trendradar news search --help

> **Note**: Use Ref links above to view detailed parameters and examples.

## User Notes

> **MUST READ** [users/skill.md](users/skill.md) for custom workflows and tips.
> **Config**: MCP server settings live in `~/.agents/ucli/servers.yaml` - edit there to take effect.
