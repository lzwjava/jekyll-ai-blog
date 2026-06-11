---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Launchd作业成功运行
translated: true
type: note
---

两个 launchd 任务正在运行。摘要如下：

```
com.lzwjava.ww-update-check      — 每小时一次，记录新提交
com.lzwjava.ww-projects-update   — 每小时一次，运行 `ww projects update`
```

两者均为活跃状态（退出码 0）。检查脚本已通过 `RunAtLoad` 触发，并记录了最近 6 次提交。

已设置的内容：

- `/Users/lzwjava/projects/ww/cron-logs/cron-check-ww-updates.sh` — 检查 `git log --since="60 minutes ago"` 并将结果记录到 `ww-update-check.log`
- `~/Library/LaunchAgents/com.lzwjava.ww-update-check.plist` — 每小时运行一次检查脚本
- `~/Library/LaunchAgents/com.lzwjava.ww-projects-update.plist` — 每小时运行一次 `ww projects update`（从损坏的 crontab 条目迁移而来）

日志输出到 `/Users/lzwjava/projects/ww/cron-logs/` 而非 `/dev/null`，因此你可以随时验证运行情况：

```
cat ~/projects/ww/cron-logs/ww-update-check.log
```

注意：`crontab` 在 macOS 26.5 上会挂起 — 此处使用 launchd 是正确的方式。旧的 crontab 条目仍然存在，但无法可靠运行。