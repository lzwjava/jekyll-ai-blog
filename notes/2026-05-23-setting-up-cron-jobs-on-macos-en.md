---
audio: false
generated: true
image: false
lang: en
layout: post
title: Setting Up Cron Jobs on macOS
translated: false
type: note
---

**Question:** How do you set up a crontab job on macOS?

**Answer:**

macOS uses `cron` just like Linux. The standard workflow:

```bash
# Open your crontab for editing (uses $EDITOR, default vi)
crontab -e

# List current crontab
crontab -l

# Remove all crontab entries
crontab -r
```

**Crontab syntax:**

```
# ┌─ minute (0-59)
# │ ┌─ hour (0-23)
# │ │ ┌─ day of month (1-31)
# │ │ │ ┌─ month (1-12)
# │ │ │ │ ┌─ day of week (0-7, 0 and 7 = Sunday)
# │ │ │ │ │
# * * * * *  command
```

**Common examples:**

```bash
# Every minute
* * * * * /usr/local/bin/python3 /Users/zhiwei/scripts/job.py

# Every 5 minutes
*/5 * * * * /path/to/script.sh

# Every day at 2am
0 2 * * * /path/to/backup.sh

# Every Monday at 9am
0 9 * * 1 /path/to/weekly.sh

# Every hour, log output
0 * * * * /path/to/script.sh >> /tmp/cron.log 2>&1
```

**macOS-specific gotchas:**

**1. Full Disk Access for cron** — macOS Catalina+ requires you to grant `/usr/sbin/cron` Full Disk Access in System Settings → Privacy & Security → Full Disk Access. Otherwise cron silently fails on file access.

**2. PATH is minimal in cron** — cron runs with a bare `PATH=/usr/bin:/bin`. Always use absolute paths:

```bash
# Bad
* * * * * python3 script.py

# Good
* * * * * /usr/bin/env python3 /Users/zhiwei/scripts/script.py

# Or set PATH explicitly at top of crontab
PATH=/usr/local/bin:/usr/bin:/bin
* * * * * python3 /Users/zhiwei/scripts/script.py
```

**3. No shell expansion** — `~` doesn't work. Use full paths like `/Users/zhiwei/`.

**4. Environment variables missing** — your `.zshrc`, conda, pyenv, etc. are not sourced. If you depend on a venv:

```bash
* * * * * /Users/zhiwei/.venv/bin/python /Users/zhiwei/scripts/job.py
```

**5. cron vs launchd** — Apple prefers `launchd` (plist-based), but `cron` works fine for simple jobs. Only use launchd if you need:
- Run on login/boot
- Dependency management
- Throttling/keepalive

**Quick launchd equivalent** for reference (daily at 2am):

```xml
<!-- ~/Library/LaunchAgents/com.zhiwei.myjob.plist -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "...">
<plist version="1.0">
<dict>
  <key>Label</key><string>com.zhiwei.myjob</string>
  <key>ProgramArguments</key>
  <array>
    <string>/usr/bin/env</string>
    <string>python3</string>
    <string>/Users/zhiwei/scripts/job.py</string>
  </array>
  <key>StartCalendarInterval</key>
  <dict><key>Hour</key><integer>2</integer><key>Minute</key><integer>0</integer></dict>
  <key>StandardOutPath</key><string>/tmp/myjob.log</string>
  <key>StandardErrorPath</key><string>/tmp/myjob.err</string>
</dict>
</plist>
```

```bash
launchctl load ~/Library/LaunchAgents/com.zhiwei.myjob.plist
launchctl list | grep zhiwei  # verify
```

**Debug cron not running:**

```bash
# Check system log for cron errors
log show --predicate 'process == "cron"' --last 1h

# Or
grep cron /var/log/system.log 2>/dev/null || log show --last 30m | grep cron
```

For your use case (AI scripts, CLI agents, automation tools), `cron` with absolute venv paths is the fastest path. Reserve `launchd` for anything that needs to survive reboots or run at login.
