---
audio: false
generated: true
image: false
lang: en
layout: post
title: Write ISO to USB with dd
translated: false
type: note
---

Found your USB disk at **`/dev/disk12`** (15.7 GB external, FAT32).

Here's the `dd` command:

```bash
# ⚠️ WARNING: This will DESTROY ALL DATA on /dev/disk12
# First, unmount any mounted volumes
sudo diskutil unmountDisk /dev/disk12

# Write the ISO to the USB disk (using raw disk for speed)
sudo dd if=/Users/lzwjava/Downloads/ubuntu-26.04-desktop-amd64.iso of=/dev/rdisk12 bs=1m
```

**Key notes:**
- Uses `/dev/rdisk12` (raw disk) → much faster than `/dev/disk12`
- `bs=1m` → 1 MB block size for better performance
- No progress indicator by default on macOS `dd`; to see progress, open another terminal and run:
  ```bash
  sudo killall -INFO dd
  ```
  (or use `sudo pv -tpreb /Users/lzwjava/Downloads/ubuntu-26.04-desktop-amd64.iso | sudo dd of=/dev/rdisk12 bs=1m` if you have `pv` installed)

Then wait patiently — ~6.1 GB at ~30-50 MB/s takes **2–3 minutes**. After it finishes, eject safely:

```bash
sudo diskutil eject /dev/disk12
```

**Double-check** `/dev/disk12` is indeed your USB stick before running — make sure no other external disks are connected!
