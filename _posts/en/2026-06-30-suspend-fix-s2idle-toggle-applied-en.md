---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Suspend Fix: s2idle Toggle Applied"
translated: false
type: note
---

Both changes applied and verified:

| Check | Before | After |
|---|---|---|
| `/sys/power/mem_sleep` | `s2idle [deep]` | **`[s2idle] deep`** |
| Config file | didn't exist | `/etc/systemd/sleep.conf.d/disable-deep-suspend.conf` → `SleepMode=s2idle` |

- **Instant fix**: the live kernel already switched — `s2idle` is now active, `[deep]` is the fallback.
- **Persistent**: survives reboot via the systemd drop-in.

s2idle uses slightly more battery at idle, but wakes reliably on Apple hardware since the keyboard/trackpad controllers stay powered. Next time the lid closes or the power key is pressed, the system should suspend and resume normally instead of crashing into a hard freeze.