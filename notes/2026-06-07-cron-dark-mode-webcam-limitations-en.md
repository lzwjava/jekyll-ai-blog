---
audio: false
generated: true
image: false
lang: en
layout: post
title: Cron Dark Mode Webcam Limitations
translated: false
type: note
---

Here's the full picture:

**Your crontab:**
```
*/10 * * * * /opt/homebrew/bin/ww appearance smart-auto
0 * * * * /opt/homebrew/bin/ww projects update
```

**What `smart-auto` does** (appearance.py line 96-181):
- Captures a webcam photo via `imagesnap` or `ffmpeg`
- Analyzes average luminance (numpy/PIL)
- If brightness < 80/255 → dark mode; otherwise → light mode

**When lid is closed — it will FAIL for two reasons:**

1. **macOS sleeps by default when lid closes.** Cron jobs don't execute during sleep. The `*/10` cron simply won't fire unless you've disabled sleep (`sudo pmset -a disablesleep 1`) or the machine is connected to an external display/keyboard in clamshell mode.

2. **Webcam is physically inaccessible.** Even if the machine stays awake (clamshell mode with external display), the built-in FaceTime camera on MacBook Air M2 is disabled when the lid is closed. `imagesnap` / `ffmpeg` will fail with a capture error, and the script exits with code 1 at line 158-160:
   ```
   Error capturing webcam: ...
   Make sure a webcam is connected and not in use by another app.
   ```

**Bottom line:** The cron job will NOT succeed with the lid closed. It needs both an awake machine AND an accessible webcam.

**If you want it to work in clamshell mode**, you'd need an external webcam connected, and the machine must not sleep. Alternatively, if the goal is just time-based dark/light switching, the built-in `ww appearance auto` (sunrise/sunset) doesn't need a webcam at all — you could swap the cron to use that instead.
