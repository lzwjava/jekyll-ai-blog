---
audio: false
generated: true
image: false
lang: en
layout: post
title: Ubuntu ISO to USB Flash
translated: false
type: note
---

All confirmed:

- **ISO**: `/Users/lzwjava/Downloads/ubuntu-26.04.1-desktop-amd64.iso` (6.0G) ✓
- **USB**: `/dev/disk12` — "OnlyDisk", 15.7 GB, external, currently **not mounted** ✓

Run these:

```bash
# 1. Unmount in case anything auto-mounts (disk12 is not mounted now, so this is just safety)
diskutil unmountDisk /dev/disk12

# 2. Flash the ISO (uses the raw device /dev/rdisk12; nothing can be mounted on a raw dd write)
sudo dd if=/Users/lzwjava/Downloads/ubuntu-26.04.1-desktop-amd64.iso of=/dev/rdisk12 bs=4m conv=sync

# 3. Flush buffers and eject
sync && diskutil eject /dev/disk12
```

Notes:

- `/dev/rdisk12` (raw) is preferred over `/dev/disk12` on macOS to avoid write-caching surprises; the ISO is 6.0G and the stick is 15.7G, so it fits.
- `dd` prints nothing until it finishes — press **Ctrl+T** in the terminal to see progress, or use `pv /Users/lzwjava/Downloads/ubuntu-26.04.1-desktop-amd64.iso | sudo dd of=/dev/rdisk12 bs=4m` for a progress bar (if `pv` is installed).
- ⚠️ This is destructive — everything on `/dev/disk12` will be overwritten. Verify it's the right stick with `diskutil list external` (only `disk12` shows as external/physical; the other disks are image/VM ones).
