---
audio: false
generated: true
image: false
lang: en
layout: post
title: Flash Debian ISO to USB
translated: false
type: note
---

Found the USB drive. Here's the situation:

**USB drive: `/dev/disk12`** (external, physical, 15.7 GB, currently has Ventoy)
**ISO: `/Users/lzwjava/Downloads/debian-live-13.6.0-amd64-xfce.iso`** (3.6 GB)

> ⚠️ This will **erase everything** on the USB drive (including Ventoy). Make sure disk12 is really your USB stick.

### Steps

**1. Unmount the disk (don't eject):**
```bash
diskutil unmountDisk /dev/disk12
```

**2. Write the ISO with dd (using `rdisk12` for much faster writes):**
```bash
sudo dd if=/Users/lzwjava/Downloads/debian-live-13.6.0-amd64-xfce.iso of=/dev/rdisk12 bs=4m status=progress
```

**3. Eject safely when done:**
```bash
diskutil eject /dev/disk12
```

Notes:
- Use `of=/dev/rdisk12` (not `disk12s1`) — write to the whole disk, raw device for speed.
- `status=progress` shows transfer progress (works on recent macOS).
- You'll be prompted for your password due to `sudo`.

Want me to run the unmount + dd for you?
