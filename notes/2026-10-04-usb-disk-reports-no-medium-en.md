---
audio: false
generated: true
image: false
lang: en
layout: post
title: USB Disk Reports No Medium
translated: false
type: note
---

I checked the connected storage devices. Here's what I found:

## USB disk status

There **is** a USB device connected, but it appears **empty/unreadable**:

| Property | Value |
|---|---|
| Device | `/dev/sdb` |
| Vendor / Model | NAND / USB2DISK |
| Interface | USB |
| Removable | Yes |
| Size | **0 bytes** |
| Partition table | None |
| Filesystem | None |

The kernel reports **"No medium found"** for `/dev/sdb`:

```
fdisk: cannot open /dev/sdb: No medium found
Error: Error opening /dev/sdb: No medium found
```

This typically means one of:
1. The USB drive is a **card reader with no memory card inserted** (the "NAND" vendor and "USB2DISK" model are common for SD/microSD adapters).
2. The drive is **blank/never formatted** — though in that case it would still report a size.
3. The drive's flash controller is **not responding** to the OS.

## Other disks (for reference)

These are the system's regular disks, not USB:

- **`/dev/sda1`** — 1.8 TB ext4, mounted at `/mnt/data` (label `data`) — this is the disk your current project lives on.
- **`/dev/nvme0n1`** — 931 GB NVMe SSD (system root + `/boot/efi`).

## What I can check next

Since `/dev/sdb` reports no medium, there's no filesystem to read. If you'd like, I can:

1. **Rescan the device** to see if it becomes readable:
   ```bash
   echo 1 | sudo tee /sys/block/sdb/device/rescan
   ```
2. **Check for a card** — if this is a card reader, insert the SD/microSD card and I'll re-detect it.
3. **Inspect the raw device** with `dmesg`/`udevadm` for more diagnostic detail on why the medium isn't detected.

Want me to try the rescan or gather more diagnostics?