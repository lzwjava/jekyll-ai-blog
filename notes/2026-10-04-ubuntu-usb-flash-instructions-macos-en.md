---
audio: false
generated: true
image: false
lang: en
layout: post
title: Ubuntu USB Flash Instructions macOS
translated: false
type: note
---

### Status: ⚠️ No USB drive is currently connected

- ✅ ISO found: `ubuntu-26.04-desktop-amd64.iso` (6.1 GB)
- ❌ The only physical disk is **disk0 (internal 500 GB SSD)**. All the "external" entries are virtual disk images (iOS simulators), **not real USB drives**.

**Plug in your USB stick, then run `diskutil list`** and look for a new entry like `/dev/disk2 (external, physical)`.

---

### The `dd` commands (macOS)

Assuming your USB shows up as `/dev/disk2` **≥ 8 GB**:

```bash
# 1. Confirm the disk (make sure it's the USB, NOT disk0!)
diskutil list

# 2. Unmount it (do NOT eject)
diskutil unmountDisk /dev/disk2

# 3. Flash the ISO (raw device /dev/rdiskX)
sudo dd if=~/Downloads/ubuntu-26.04-desktop-amd64.iso of=/dev/rdisk2 bs=4m status=progress conv=fsync
```

---

### ⚠️ Critical warnings

1. **Double-check the disk number** — `of=/dev/rdisk0` will overwrite your system SSD and brick the machine.
2. It must have **≥ 8 GB** (the ISO is 6.1 GB).
3. If you get `Resource busy`, make sure step 2 succeeded: `diskutil unmountDisk /dev/disk2`.
4. `conv=fsync` ensures data is fully flushed before you pull the stick.

Once it finishes, you can verify with:

```bash
diskutil eject /dev/disk2
```

Plug in your USB and tell me the disk number it gets — I'll run it for you.
