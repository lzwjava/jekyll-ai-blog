---
audio: false
generated: true
image: false
lang: en
layout: post
title: No USB drive attached
translated: false
type: note
---

**No — that's not your USB drive.** ❌

`/dev/disk10` is a **virtual disk image** named "iOS 26.3.1 Simulator" (17.8 GB). It's a simulator file, not hardware. Same for disk4, disk6, disk8.

Current physical disks on this machine:

| Device | Type |
|---|---|
| `/dev/disk0` | internal, physical (500 GB SSD) ⛔ never touch |
| disk4/6/8/10 | disk images (iOS simulators) 🎭 not real |

**You still have no USB drive attached.** Since the last check, nothing new appeared.

To confirm yourself, run:

```bash
diskutil list
```

A real USB stick shows up like this:

```
/dev/diskX (external, physical):
   #:                       TYPE NAME                    SIZE       IDENTIFIER
   0:     GUID_partition_scheme                        *7.9 GB     diskX
   1:       Microsoft Basic Data Untitled                7.9 GB     diskXs1
```

📌 Note: `diskutil list | grep -i external` shows nothing because the only physical disk is the internal one — `diskutil list external` didn't print a hardware line either.

**Steps:**
1. Physically plug the USB stick into the Mac
2. Run `diskutil list` again and paste the output here
3. Then we flash it with `dd`

If it's already plugged in, try another port, or check with `ioreg`/System Information → USB to see if macOS detects it at all.
