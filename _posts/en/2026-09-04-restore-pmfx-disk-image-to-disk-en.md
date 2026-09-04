---
audio: false
generated: true
image: false
lang: en
layout: post
title: Restore .pmfx Disk Image to Disk
translated: false
type: note
---

**Question:** How do I restore a `.pmfx` (DiskGenius disk image) file to a disk?

**Answer:**

A `.pmfx` file is DiskGenius's own disk image format — it's a compressed backup of an entire disk, containing all partitions and files. There are two things you can do with it: **restore it to a disk**, or **browse/extract files from it without restoring**.

---

### ✅ Option 1 — Restore the .pmfx Image to a Disk (Full Restore)


1. **Right-click** the destination disk in DiskGenius → select **"Restore Image File To Disk"**, or go to menu **Disk → Restore Image File To Disk**.
2. In the file dialog, locate and select your `.pmfx` file → click **Open**.
3. Confirm the target disk is correct → click **Start**.
4. A warning will appear that all partitions and data on the destination disk will be overwritten. Make sure any important data is backed up first → click **OK**.
5. Wait for the restore to complete.


> ⚠️ Important: When restoring, the target disk should not be smaller than the source disk.

---

### ✅ Option 2 — Restore Only a Single Partition from the .pmfx File

Newer versions of DiskGenius support restoring an individual partition from a `.pmfx` disk image file, so you don't have to restore the whole disk if you only need one partition.

---

### ✅ Option 3 — Browse & Extract Files Without Restoring

If you just want to pull specific files out of the `.pmfx` image without writing it to a disk:


1. Click **Tools** menu → select **"Load Disk/Partition Image"**.
2. Browse and locate the `.pmfx` image file → click **Open**.
3. Select a time point you want to check → click **Start**. DiskGenius will load the files in the backup image.
4. Select the files you want to retrieve and copy them to a desired location.


---

### 💡 Tips

- The `.pmfx` extension is specific to DiskGenius (also known as Eassos DiskGenius). You can only open/restore `.pmfx` files using DiskGenius on Windows.
- Sector editing is also supported for `.pmfx` disk image files in newer versions, for advanced users.

---

**References:**
- [Restore Disk From Image File – DiskGenius Manual](https://www.diskgenius.com/manual/restore-disk-from-image-file.php)
- [Load and Browse Partition Image File – DiskGenius Manual](https://www.diskgenius.com/manual/explorer-partition-img.php)
- [.PMFX File Extension Info – FileInfo.com](https://fileinfo.com/extension/pmfx)
- [DiskGenius Version History](https://www.diskgenius.com/version-history.php)
