---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixing cron's missing image snap tool
translated: false
type: note
---

The latest cron run is **failing**. Here's the summary:

**Error:** `FileNotFoundError: [Errno 2] No such file or directory: 'imagesnap'`

**Root cause:** The cron environment has a minimal PATH (`/usr/bin:/bin`), but `imagesnap` is a Homebrew tool at `/opt/homebrew/bin/`. The `ww` binary itself is found because the cron line uses its full path `/opt/homebrew/bin/ww`, but when `appearance smart-auto` internally calls `subprocess.run(["imagesnap", ...])`, it can't find it.

The cron mail at 17:24:42 shows the full traceback. Every 2-minute run is hitting this.

**Quick fix — either:**

1. Add PATH to your crontab:

```
PATH=/opt/homebrew/bin:/usr/bin:/bin
*/2 * * * * /opt/homebrew/bin/ww appearance smart-auto
```

2. Or symlink imagesnap into a cron-visible path:

```
sudo ln -sf /opt/homebrew/bin/imagesnap /usr/local/bin/imagesnap
```

Option 1 is cleaner. Want me to update your crontab?
