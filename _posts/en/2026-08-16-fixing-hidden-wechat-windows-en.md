---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixing Hidden WeChat Windows
translated: false
type: note
---

Done. The helper script is saved at `~/.local/bin/fix-wechat.sh` and works — it mapped 4 hidden WeChat windows and activated the main one.

## Summary

| Item | Status |
| --- | --- |
| **Cause** | WeChat was running (since Aug 13) but its windows were hidden/unmapped; the launcher icon just spawned dead second instances (single-instance app), so nothing appeared |
| **Not the cause** | No crash, no segfault, no hung threads, no corrupt logs — the process tree was healthy |
| **Fix applied** | Force-mapped the hidden windows via X (`xdotool windowmap`) — app not killed, your session untouched |
| **Helper** | `~/.local/bin/fix-wechat.sh` — run anytime WeChat's window goes missing again |

**If it happens again**, just run:

```bash
fix-wechat.sh
```

**Optional clean-up** (recommended since it's been running 3 days with a zombie child):

```bash
pkill -f '/opt/wechat' ; sleep 2 ; nohup /usr/bin/wechat >/dev/null 2>&1 &
```

Let me know if the WeChat window is now showing correctly on your screen.
