---
audio: false
generated: true
image: false
lang: en
layout: post
title: Vibe Coding Notification Loop
translated: false
type: note
---

Yes, that works — but a timer means *you* poll the agent. Better: make the task notify *you* when it's done, so you don't context-switch on a schedule at all.

On your MacBook Air, append a notification to whatever long-running command:

```bash
# macOS native notification + sound when done
long_task && osascript -e 'display notification "Task done" with title "Copilot" sound name "Glass"'

# or just an audible ping
long_task; say "done"
```

If the agent runs in Warp, Warp also has built-in "notify when command completes" for unfocused tabs (Settings → Features), so any command over a few seconds triggers a macOS notification automatically — zero setup per task.

For agents you can't wrap (e.g. Copilot running inside an IDE), your Clock-app snooze is a reasonable fallback, though a 10-min `sleep` one-liner keeps you in the terminal:

```bash
sleep 600 && say "check copilot"
```

And yes — filling that gap with AI news reading is fine, but it's the classic attention trap: 10 minutes of browsing often becomes 25, and the agent finished at minute 7. The notification approach inverts it: read freely, get interrupted the moment the task ends. That's the higher-throughput loop for vibe coding — you want the agent's idle time to be zero, not yours.

One more pattern worth building, given you make CLI agents: have `ww`/`zz` post to a local webhook or `terminal-notifier` on completion, so every long task in your stack pings you uniformly.
