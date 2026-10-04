---
audio: false
generated: true
image: false
lang: en
layout: post
title: Ubuntu ISO Write to USB Now
translated: false
type: note
---

Unmounted ✅. The stick is write-ready **right now**.

### Run this single command (needs your password)

```bash
sudo dd if=/Users/lzwjava/Downloads/ubuntu-26.04-desktop-amd64.iso of=/dev/rdisk12 bs=4m status=progress conv=fsync
```

- **Device:** `/dev/rdisk12` = your 15.7 GB USB (double-checked just now) — **not** disk0 (your SSD)
- ISO: 6.1 GB → will take ~2–5 min
- It prints a progress bar; wait until you see `xxxx+0 records in` / `xxxx+0 records out` and the `$` prompt returns

**Do NOT** until it finishes:

- Eject, unplug, or click anything in Finder
- Run Disk Utility

After it finishes, tell me the last line, or just run:

```bash
diskutil eject /dev/disk12
```

to safely unplug.
