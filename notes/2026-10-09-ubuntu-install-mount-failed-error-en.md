---
audio: false
generated: true
image: false
lang: en
layout: post
title: Ubuntu Install Mount Failed Error
translated: false
type: note
---

**Question:** Why did the Ubuntu installation fail with this error?

**Answer:**

The key error is:

```
RuntimeError: Mount failed: /dev/sda2 @ /target/ with options defaults
```

This means the Ubuntu installer (Subiquity/Curtin) **failed to mount the partition `/dev/sda2` to `/target/`** during the installation's partitioning/formatting step. Common causes:

**1. Disk Already in Use / Busy**

- The partition `/dev/sda2` may be mounted elsewhere or locked by another process.

**2. Filesystem Corruption or Wrong Filesystem Type**

- The partition may have an incompatible or corrupted filesystem that can't be mounted.

**3. Faulty or Incompatible Drive**

- Bad sectors or a failing SSD/HDD can cause mount failures.

**4. RAID / LVM Conflict**

- If the disk was previously part of a RAID array or LVM group, remnants can block mounting.

**5. Secure Boot / Driver Issue**

- Some NVMe or SATA controllers need specific drivers.

---

**How to Fix:**

1. **Try "Erase disk and install Ubuntu"** — let the installer wipe and repartition from scratch.
2. **Open a terminal** (Ctrl+Alt+T during install) and run:

   ```bash
   sudo wipefs -a /dev/sda
   sudo fdisk /dev/sda  # re-create partition table
   ```

3. **Check disk health:**

   ```bash
   sudo smartctl -a /dev/sda
   ```

4. **Deactivate old LVM/RAID:**

   ```bash
   sudo dmsetup remove_all
   sudo vgchange -an
   ```

5. **Try a different USB boot drive** — the ISO may be corrupted.

---

**References:**

- [Ubuntu Installation Errors – Ask Ubuntu](https://askubuntu.com/questions/tagged/installation)
- [Curtin block_meta.py source – GitHub](https://github.com/canonical/curtin)
- [Mount failed during Ubuntu install – Ubuntu Forums](https://ubuntuforums.org/forumdisplay.php?f=335)
