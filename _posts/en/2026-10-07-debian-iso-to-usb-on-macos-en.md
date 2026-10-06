---
audio: false
generated: true
image: false
lang: en
layout: post
title: Debian ISO to USB on macOS
translated: false
type: note
---

Your ISO is confirmed: `debian-13.7.0-amd64-netinst.iso` (756 MB), and I found your USB stick: **/dev/disk12** (4 GB, USB, labeled EAGET).

**⚠️ Double-check this is the right USB — dd will erase everything on it with no warning.**

On macOS, run:

```bash
# 1. Unmount the USB (ignore errors if already unmounted)
sudo diskutil unmountDisk /dev/disk12

# 2. Write the ISO to the RAW device (note the "r" in rdisk12)
sudo dd if=/Users/lzwjava/Downloads/debian-13.7.0-amd64-netinst.iso of=/dev/rdisk12 bs=4m status=progress conv=fsync

# 3. Eject when done
sudo diskutil eject /dev/disk12
```

Key points:
- `of=/dev/rdisk12` (raw device) — **never** write to `/dev/disk12` (the logical device), or macOS may not flush the data properly.
- `conv=fsync` ensures all data is flushed to the stick before dd exits.
- `bs=4m` speeds things up; the whole write should take under a minute.
- The `status=progress` flag shows live progress (GNU dd / newer macOS dd). If it errors with "invalid status", drop it and just watch `pkill -USR1 -n -x dd` from another terminal.

If you want to be extra safe before step 2, verify you're targeting the stick: `diskutil info /dev/disk12` should show the same size as your stick (4 GB).
