---
audio: false
generated: true
image: false
lang: en
layout: post
title: Launchd Jobs Running Successfully
translated: false
type: note
---

Both launchd jobs are running. Here's the summary:

```
com.lzwjava.ww-update-check      — every 1hr, logs new commits
com.lzwjava.ww-projects-update   — every 1hr, runs `ww projects update`
```

Both are active (exit code 0). The check script already fired via `RunAtLoad` and logged 6 recent commits.

What was set up:

- `/Users/lzwjava/projects/ww/cron-logs/cron-check-ww-updates.sh` — checks `git log --since="60 minutes ago"` and logs to `ww-update-check.log`
- `~/Library/LaunchAgents/com.lzwjava.ww-update-check.plist` — runs the check script hourly
- `~/Library/LaunchAgents/com.lzwjava.ww-projects-update.plist` — runs `ww projects update` hourly (migrated from the broken crontab entry)

Logs go to `/Users/lzwjava/projects/ww/cron-logs/` instead of `/dev/null`, so you can verify runs anytime:

```
cat ~/projects/ww/cron-logs/ww-update-check.log
```

Note: `crontab` hangs on macOS 26.5 — launchd is the correct approach here. The old crontab entries are still there but won't run reliably.
