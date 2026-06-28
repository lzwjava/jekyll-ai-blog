---
audio: false
generated: true
image: false
lang: en
layout: post
title: Decoding Live Environment Block Devices
translated: false
type: note
---

**Question:** What is this `lsblk` output showing?

**Answer:**

You're booted into a **Linux live environment** (`liveuser@localhost-live`). Here's the block device breakdown:

```
loop0        2.3G   loop  /run/rootfsbase     ← live OS squashfs
sda         14.6G   disk                      ← USB boot drive
├─sda1       2.6G   part  /run/initramfs/live ← live boot partition
└─sda2        30M   part                      ← EFI or BIOS boot
zram0          8G   disk  [SWAP]              ← compressed RAM swap
nvme0n1        0B   disk                      ← NVMe SSD (main)
├─nvme0n1p1  600M   part                      ← EFI System Partition
├─nvme0n1p2    2G   part                      ← likely /boot
└─nvme0n1p3 231.2G  part  /mnt/sysroot        ← main OS root, mounted
nvme0n2        GB   disk                      ← second NVMe (size unclear, blurry)
```

Key observations:

- `nvme0n1p3` (231G) is mounted at `/mnt/sysroot` — this is your installed system's root partition, accessible from the live session
- `sda` is your USB live boot drive (14.6G)
- `nvme0n2` exists but has no partitions visible — possibly blank or uninitialized

**What are you trying to do?** Install an OS, recover/chroot into the existing system, repartition, or something else? The setup looks like a Fedora or similar live ISO (the `rootfsbase` + `initramfs/live` pattern is Fedora's).
