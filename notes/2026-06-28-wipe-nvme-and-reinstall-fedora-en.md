---
audio: false
generated: true
image: false
lang: en
layout: post
title: Wipe NVMe and Reinstall Fedora
translated: false
type: note
---

Looking at your `lsblk` output from the photo, the NVMe is already visible:

```
nvme0n1      259:0    0    0B   0 disk          ← shows 0B = corrupted partition table
├─nvme0n1p1  259:1    0  600M   0 part
├─nvme0n1p2  259:2    0    2G   0 part
└─nvme0n1p3  259:4    0  231.2G 0 part  /mnt/sysroot
```

Actually it's showing partitions AND `/mnt/sysroot` is mounted — the partition table isn't fully corrupted, the previous install partially wrote to it. The `0B` on the disk itself is just a display artifact from the blurry photo.

**Here's what to do step by step:**

**Step 1 — Unmount sysroot first (important)**

```bash
sudo umount /mnt/sysroot
```

**Step 2 — Wipe everything**

```bash
sudo wipefs --all /dev/nvme0n1
sudo wipefs --all /dev/nvme0n1p1
sudo wipefs --all /dev/nvme0n1p2
sudo wipefs --all /dev/nvme0n1p3
```

**Step 3 — Fresh GPT label**

```bash
sudo parted /dev/nvme0n1 mklabel gpt
```

**Step 4 — Verify**

```bash
lsblk
```

Should now show `nvme0n1` with no children partitions.

**Step 5 — Relaunch Fedora installer**

```bash
sudo anaconda
```

Or click the installer icon on the desktop. It will see a clean disk and let you do automatic partitioning.

What does `lsblk` show after the wipe?
