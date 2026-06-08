---
audio: false
generated: true
image: false
lang: en
layout: post
title: Unplugging iShare won't damage Mac
translated: false
type: note
---

**Question:** Can unplugging an iShare (wireless HDMI transmitter) suddenly from a Mac cause damage? A friend's Mac went black screen after doing this and won't boot.

**Answer:**

Direct answer: **No, unplugging the device won't physically damage the Mac hardware.** The black screen is almost certainly unrelated or coincidental—sudden USB device disconnections don't cause electrical damage to modern Macs (they have robust power delivery and isolation).

What likely happened:

1. **Coincidental timing** — The Mac had an existing issue (failing drive, RAM, GPU) that surfaced just then
2. **Kernel panic** — The device driver crash triggered a panic that corrupted the boot partition or left the system in an unrecoverable state
3. **Display output stuck** — The external display connection got wedged and the Mac is actually running but output is routed nowhere

**Troubleshooting steps for your friend:**

```bash
# Force restart (hold power for 10+ seconds until shutdown)
# Try twice

# Then try these in order:

# 1. Reset SMC (Intel Macs)
# Power off → Cmd + Shift + Ctrl + Power (hold 10s) → release all → wait → power on

# 2. Reset SMC (Apple Silicon)
# Power off → hold power button for 10s → release → wait 10s → power on

# 3. Try booting into Recovery Mode
# Power on → Cmd + R (hold immediately) → wait for recovery screen

# 4. If Recovery loads, run Disk Utility to check for corruption
# Disk Utility → select drive → First Aid → Repair Disk
```

If Recovery Mode won't load, the issue is likely **pre-boot** (firmware, SSD, or logic board), not caused by the USB device.

**The actual risk:** Unplugging during active file writes *could* theoretically corrupt an open file, but this would be a filesystem issue, not hardware damage. Boot corruption from a USB device crash is extremely rare on modern macOS.

**Bottom line:** The iShare didn't break the Mac. Your friend either had a hardware failure that coincidentally happened to occur then, or needs to recover the OS via DFU restore using another Mac + USB-C cable. The disconnect itself is harmless.