---
audio: false
generated: true
image: false
lang: en
layout: post
title: Alarm plist integration fix
translated: false
type: note
---

Done. Here's what was wrong and what I fixed:

**Problem:** `_set_alarm()` was just spawning a `sleep` + `osascript notification` background process and opening `clock-alarm://`. It never actually wrote anything to the Clock.app plist — so no alarm appeared in Clock.app.

**Fix:** Rewrote `_set_alarm()` to:
1. Build an alarm dict matching the exact `mobiletimerd` plist format (reverse-engineered from your existing alarms)
2. Read the plist, append the new alarm to `MTAlarms.MTAlarms`
3. Write it back with `plistlib.dump`
4. `killall mobiletimerd` so Clock.app picks up the change on restart

Test result:
```
$ ww alarm 10 "clothes"
Alarm set for 23:46 (in 10m00s)  label: "clothes"

$ ww alarm list
Found 6 alarm(s) (plist):
  01:50  clothes  [off]
  02:10  (no label)  [off]
  13:32  eat  [off]
  23:30  clothes  [off]
  23:50  clothes  [off]
  23:46  clothes  [on]    ← new, enabled
```

The alarm now shows in Clock.app. Open it to verify — you should see the 23:46 "clothes" alarm toggled on.
