---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Wake the Machine: Tap Power Button"
translated: false
type: note
---

Right now, just one simple physical action:

## Wake the machine

1. **Press the power button once, briefly** (tap it — do **NOT** hold it down, or you'll force a hard shutdown).
2. OR move the mouse / press any keyboard key.
3. Wait ~15–20 seconds for it to come back. The screen should light up (maybe a lock screen — password is `lizhiwei17` if it asks).

Then tell me "woke up" — I'll immediately:

1. ✅ Verify it's reachable
2. ✅ **Permanently disable auto-suspend** (systemd + desktop power settings) so this never happens again
3. ✅ Restart `llama-server` (it'll then stay up 24/7)

---

**How to tell the state right now:**

- Power LED **blinking slowly** → asleep (normal) → just tap power button
- Power LED **solid on** but screen black → tap power button anyway
- If tapping power button does nothing for 30s → press **Ctrl+Alt+F1** (switch to a TTY), which often wakes it

Just tap the power button and tell me when you've done it — I'll take it from there. 👍
