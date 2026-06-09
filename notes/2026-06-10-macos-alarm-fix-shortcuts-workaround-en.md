---
audio: false
generated: true
image: false
lang: en
layout: post
title: "macOS Alarm Fix: Shortcuts Workaround"
translated: false
type: note
---

## Summary

### The Root Problem

On macOS 26, Clock.app alarms are managed entirely by the `mobiletimerd` daemon via XPC (`com.apple.MobileTimer.alarmserver`). The daemon keeps alarms in-memory. Neither the plist nor the SQLite database is the source of truth — the daemon IS.

**What doesn't work (all tested and confirmed):**
1. Writing to `~/Library/Preferences/com.apple.mobiletimerd.plist` — daemon ignores it, Clock.app shows "No Alarms"
2. Writing to `~/Library/Group Containers/group.com.apple.mobiletimerd/local.sqlite` — same result
3. Calling `MTAlarmManager.addAlarm_()` via pyobjc — XPC rejected: `"not entitled"`
4. Compiled Swift binary calling MobileTimer framework — same `"not entitled"` error
5. Donating `MTCreateAlarmIntent` via `INInteraction` — donates to Siri suggestions but doesn't create the alarm

The entitlements are Apple-private. Only Apple-signed processes (Clock.app, Shortcuts.app, Siri) can talk to `mobiletimerd`.

### What DOES Work

**Shortcuts.app** has the correct entitlements and can create alarms. The `shortcuts` CLI can run shortcuts:
```bash
shortcuts run "shortcut-name" --input-path /tmp/input.txt
```

### What I've Done

1. **Created and signed a `.shortcut` file** — discovered that `.shortcut` is a plain binary plist (not a ZIP), and `shortcuts sign` accepts it
2. **Imported `ww-create-alarm-signed`** into Shortcuts.app — it exists but has no actions
3. **Cleaned up `alarm.py`** — rewrote it to use SQLite (correct approach conceptually, but insufficient without the daemon)

### What's Needed (One-Time Manual Setup)

The user needs to add a "Create Alarm" action to the shortcut in Shortcuts.app:

1. Open Shortcuts.app → find "ww-create-alarm-signed"
2. Click to edit → add action → search "Create Alarm" (from Clock app)
3. Configure it to accept **Shortcut Input** as text (format: `HH:MM label`)
4. Save

Then update `alarm.py` to call:
```python
subprocess.run(["shortcuts", "run", "ww-create-alarm-signed", "--input-path", tmpfile])
```

**Want me to delete the empty shortcut, create a fresh one with proper setup instructions, and update `alarm.py` to use the `shortcuts run` approach?** You'd just need to do a 2-minute manual step in Shortcuts.app to add the "Create Alarm" action.
