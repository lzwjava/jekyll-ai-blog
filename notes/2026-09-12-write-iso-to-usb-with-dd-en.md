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

Your USB stick shows up as **`/dev/disk12`** (external, physical, 15.7 GB). Here's the process on macOS:

**1. Unmount the disk first** (do not eject it, just unmount):

```bash
diskutil unmountDisk /dev/disk12
```

**2. Write the ISO with `dd`** (use `rdisk` for much faster raw writes):

```bash
sudo dd if=/Users/lzwjava/Downloads/ubuntu-26.04-desktop-amd64.iso of=/dev/rdisk12 bs=4M status=progress
```

If your `dd` doesn't support `status=progress`, use:

```bash
sudo dd if=/Users/lzwjava/Downloads/ubuntu-26.04-desktop-amd64.iso of=/dev/rdisk12 bs=4m
```

During the write there's no visible output — it can look frozen for several minutes. You can press `Ctrl+T` in the terminal to show progress.

**3. Eject when done:**

```bash
diskutil eject /dev/disk12
```

⚠️ **Warning:** this completely erases everything on `/dev/disk12`. Double-check the target — if you plug/unplug other drives, run `diskutil list` again to confirm the USB stick's identifier before running `dd`.
