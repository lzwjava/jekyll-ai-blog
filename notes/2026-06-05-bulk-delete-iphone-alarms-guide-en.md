---
audio: false
generated: true
image: false
lang: en
layout: post
title: Bulk Delete iPhone Alarms Guide
translated: false
type: note
---

Question: How can I batch-delete hundreds of alarms from my iPhone using macOS and Xcode?

Answer:

**The blunt answer:** Standard Xcode workflows won't directly expose iPhone alarm deletion. But you have practical options depending on pain tolerance.

## Option 1: Use Reminders App (Cleanest)

If your alarms are synced to iCloud Reminders, migrate them there and bulk-delete:

```bash
# On macOS, open Reminders.app
# All your alarms appear as reminders if they're iCloud-synced
# Select all (Cmd+A) and delete
```

This works if your alarms are tied to Apple's ecosystem. Check iPhone Settings → [Your Name] → iCloud → Reminders.

## Option 2: SQLite Database Access (Direct)

iPhone stores alarms in `/Library/Preferences/com.apple.mobiletimer.plist` and associated database files. Without jailbreak, access requires:

**Via libimobiledevice + script:**

```bash
# Install libimobiledevice
brew install libimobiledevice

# Mount iPhone filesystem
mkdir -p /tmp/iphone_mount
ifuse /tmp/iphone_mount

# Navigate to alarm storage
ls /tmp/iphone_mount/Library/Preferences/ | grep -i timer
ls /tmp/iphone_mount/Library/Caches/ | grep -i clock

# For .plist files, convert and inspect
python3 << 'EOF'
import plistlib
import sys

plist_path = "/tmp/iphone_mount/Library/Preferences/com.apple.mobiletimer.plist"
with open(plist_path, 'rb') as f:
    data = plistlib.load(f)

# Inspect structure
print(f"Keys: {data.keys()}")
# Alarms typically stored under 'Alarms' key
if 'Alarms' in data:
    print(f"Alarm count: {len(data['Alarms'])}")
    # Clear alarms
    data['Alarms'] = []

    with open(plist_path, 'wb') as f:
        plistlib.dump(data, f)
    print("Alarms cleared")
EOF

# Unmount
umount /tmp/iphone_mount
```

**Caveat:** This requires enabling Developer Mode on iPhone (Settings → Privacy → Developer Mode) and may require trust dialogs.

## Option 3: Apple Configurator 2 (GUI, but effective)

```bash
# Via command line
open -a "Apple Configurator 2"
# Connect iPhone → Device → Advanced → Reset → Clear Cached Data
```

Not code-first, but fastest if ifuse doesn't work.

## Option 4: Xcode Debugger Script (Most reliable)

Connect iPhone via USB and use Xcode's debugger automation:

```bash
# Requires Xcode + device connected
xcrun devicectl device list

# Pair device if needed
xcrun devicectl device pair <device_udid>

# Use lldb to script deletion (advanced):
xcrun lldb --no-lldbinit -b \
  -o "attach <pid>" \
  -o "p [UIApplication sharedApplication]" \
  # This approach is fragile without app-level access
```

**Reality check:** This is hacky without a companion app on the iPhone itself.

## Option 5: Write a Companion Automation (Most AI-native)

Create a minimal iOS Shortcuts automation that deletes alarms:

```
Shortcut: Delete All Alarms
1. Get all reminders from "Alarms" list (if using Reminders)
2. For each reminder: Delete it
3. Run on a schedule or manually via Siri
```

Then trigger from macOS:

```bash
# Run iOS Shortcut from macOS
open "shortcuts://run-shortcut?name=Delete%20All%20Alarms"
```

## My recommendation for you:

**Fastest:** Option 1 (migrate to Reminders, bulk-delete).

**Most technical:** Option 2 (libimobiledevice + plist manipulation) — requires Developer Mode enabled on iPhone, but gives you direct filesystem access and scriptability. Test on a non-critical backup first.

**Fallback:** Option 3 (Configurator 2) if ifuse hangs.

Which machine are you running this on? If it's the Air M2, libimobiledevice might need a fresh compile via Homebrew. If the workstation (Linux), you have more direct options with `adb` if you ever bridge Android tooling, but for iPhone stay with libimobiledevice.
