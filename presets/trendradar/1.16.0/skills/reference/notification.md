# Notification Commands

## send — Send notification to configured channels

```bash
ucli trendradar notification send --message '**测试消息**'
ucli trendradar notification send --message '紧急通知' --title '系统告警' --channels feishu dingtalk
```

Also supports: `--title`, `--channels` (feishu/dingtalk/wework/telegram/email/ntfy/bark/slack/generic_webhook)

## channels — List all configured notification channels

```bash
ucli trendradar notification channels
```

No parameters required.

## format-guide — Get format guide for notification channels

```bash
ucli trendradar notification format-guide
ucli trendradar notification format-guide --channel feishu
```

Also supports: `--channel`

Use `ucli trendradar notification <cmd> --help` for full parameter details.
