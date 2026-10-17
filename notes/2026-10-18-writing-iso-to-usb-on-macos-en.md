---
audio: false
generated: true
image: false
lang: en
layout: post
title: Writing ISO to USB on macOS
translated: false
type: note
---

The ISO (756M) fits fine on the 4 GB stick. Here's the command:

```bash
# 1. Unmount the disk (don't eject — dd needs raw access)
diskutil unmountDisk /dev/disk14

# 2. Write the ISO to the raw device node (rdisk = much faster than disk)
sudo dd if=/Users/lzwjava/Downloads/debian-13.7.0-amd64-netinst.iso of=/dev/rdisk14 bs=4m status=progress

# 3. Flush buffers, then eject
sync
diskutil eject /dev/disk14
```

Key points:

- **`/dev/rdisk14`** (raw device) — using `/dev/disk14` would be painfully slow; `rdisk` bypasses the block cache.
- **`bs=4m`** — 4 MB block size for speed; `status=progress` shows live progress.
- **`sudo`** — required for writing to the raw device; you'll be prompted for your password.
- This **overwrites the entire stick** — the FAT32 "USB" volume from before will be gone, replaced by the Debian installer image. That's expected and correct for a bootable USB.

After it finishes, the stick will boot the Debian 13.7 netinst installer on any x86-64 machine (UEFI or legacy BIOS).

Want me to run it for you? I can execute the unmount + dd + sync steps — just note it'll prompt for your sudo password in the terminal.
