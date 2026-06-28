---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix Corrupted NVMe Partition Table
translated: false
type: note
---

Don't worry — the SSD is still there, the partition table is just corrupted from the interrupted install. Let's fix it.

**In the Fedora live environment, open a terminal and run:**

```bash
# Check if the disk is visible
lsblk
```

Tell me what you see — specifically look for the ~251 GB NVMe drive (probably `nvme0n1`).

If you see it, we'll wipe the corrupted partition table and start fresh:

```bash
# Wipe the partition table completely
sudo wipefs --all /dev/nvme0n1

# Create a fresh GPT partition table
sudo parted /dev/nvme0n1 mklabel gpt
```

Then go back to the installer — it should see the disk again.

**Also: plug in the power adapter now!** Don't run the install on battery.

What does `lsblk` show?
