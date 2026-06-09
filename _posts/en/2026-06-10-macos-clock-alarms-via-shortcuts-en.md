---
audio: false
generated: true
image: false
lang: en
layout: post
title: macOS Clock alarms via Shortcuts
translated: false
type: note
---

Here's the full investigation summary:

## What's happening

**macOS 26 Clock.app does NOT read alarms from the plist or SQLite database.** The `mobiletimerd` daemon manages all alarms in-memory and exposes them via XPC at `com.apple.MobileTimer.alarmserver`. Clock.app only talks to this daemon — never touches the files directly.

## What doesn't work (all tested)

1. **Plist write** (`~/Library/Preferences/com.apple.mobiletimerd.plist`) — daemon ignores it. Clock.app shows "No Alarms".

2. **SQLite write** (`group.com.apple.mobiletimerd/local.sqlite`) — daemon ignores it. Same result.

3. **pyobjc MTAlarmManager.addAlarm_()** — XPC connection rejected: `"not entitled"`. Only Apple-signed apps with the `com.apple.private.mobiletimerd.alarmserver` entitlement can talk to the daemon.

4. **Compiled Swift binary** — same `"not entitled"` error. Code signing doesn't help without Apple's private entitlement.

## What DOES work

**Shortcuts.app** has the correct entitlements. The user already has a `中国法定节假日闹钟` shortcut that creates alarms. `shortcuts run` works.

## The fix

The `_set_alarm` function needs to use **Shortcuts.app** as the bridge. The approach:

1. Create a reusable shortcut (e.g. "ww-create-alarm") in Shortcuts.app that takes `hour`, `minute`, and `label` as input and creates a Clock.app alarm using the `MTCreateAlarm` intent action.

2. In `_set_alarm`, call `shortcuts run "ww-create-alarm" --input-path <args>`.

The shortcut needs to be created once via the Shortcuts.app GUI (we can guide the user), or we can create a `.shortcut` file programmatically and import it. The `shortcuts` CLI supports `sign` but not `import`, so the first shortcut creation is a one-time manual step.

**Want me to proceed with creating the shortcut and updating `alarm.py`?**
