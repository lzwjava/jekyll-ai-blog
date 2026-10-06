---
audio: false
generated: true
image: false
lang: en
layout: post
title: Stalled USB drive recovery
translated: false
type: note
---

Done — `dd` is killed and the drive is idle again (0 IOPS). The drive still enumerates as `/dev/disk12` with its old partition table intact.

Since the drive's USB pipe was stalled, it's in a half-reset hardware state. Before trying anything else:

1. **Unplug the USB stick and plug it back in** (this resets the stalled flash controller).
2. Test the drive health: `diskutil eraseDisk FAT32 TEST /dev/disk12`
3. If that succeeds, try flashing again — ideally a different USB port, and with `bs=1m` instead of `bs=4m`.

If it stalls at the same LBA again, the stick is genuinely bad and not worth another try.
