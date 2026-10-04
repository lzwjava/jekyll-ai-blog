---
audio: false
generated: true
image: false
lang: en
layout: post
title: Create Bootable Ubuntu USB
translated: false
type: note
---

Disk is unmounted ✅. But `sudo` needs your password, which I can't type for you — **run this yourself in a terminal**:

```bash
sudo dd if=/Users/lzwjava/Downloads/ubuntu-26.04-desktop-amd64.iso of=/dev/rdisk12 bs=4m status=progress conv=fsync
```

Then, once it finishes (progress shows `6139+0 records in/out`), eject:

```bash
diskutil eject /dev/disk12
```

⚠️ **Confirm the device before pressing Enter**: it's `/dev/rdisk12` — the 15.7 GB external USB. Double check with `diskutil list` if unsure. Writing to `rdisk0` would destroy your internal SSD.

After `dd` completes, your USB will be a bootable Ubuntu 26.04 installer; the "FD13-LITE" partition will be gone (expected). Tell me the result or if it errors.
