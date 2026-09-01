---
audio: false
generated: true
image: false
lang: en
layout: post
title: Write Debian ISO to USB Disk
translated: false
type: note
---

Here's the command to write the Debian ISO to the USB disk. **⚠️ This will completely erase `/dev/disk12` — make sure no other important data is on it.**

### Step 1 — Unmount the disk (don't eject)
```bash
diskutil unmountDisk /dev/disk12
```

### Step 2 — Write the ISO with `dd`
```bash
sudo dd if=/Users/lzwjava/Downloads/debian-live-13.6.0-amd64-xfce.iso \
     of=/dev/rdisk12 \
     bs=4m \
     status=progress
```

Notes:
- Use **`/dev/rdisk12`** (raw device) instead of `/dev/disk12` — it's much faster on macOS.
- `bs=4m` gives good throughput; `status=progress` shows transfer progress (GNU dd style; macOS's BSD `dd` ignores it but it won't error).

### Step 3 — Flush and eject safely
```bash
sync
diskutil eject /dev/disk12
```

### Quick safety check before running
You can confirm the target is really your USB stick (15.7 GB, external):
```bash
diskutil info /dev/disk12 | grep -E "Device/ Media Name|Disk Size|Solid State|Removable"
```

### One-liner (unmount → dd → sync → eject)
```bash
diskutil unmountDisk /dev/disk12 && \
sudo dd if=/Users/lzwjava/Downloads/debian-live-13.6.0-amd64-xfce.iso of=/dev/rdisk12 bs=4m && \
sync && diskutil eject /dev/disk12
```

If `status=progress` isn't supported and you want to see progress, in another terminal you can run:
```bash
sudo kill -INFO $(pgrep -n dd)     # macOS: sends SIGINFO, prints current progress
```

**Double-check `/dev/disk12` is still your USB drive before running `dd`** — disk identifiers can change after reinsertion. Verify with `diskutil list external` right before.
