---
audio: false
generated: true
image: false
lang: en
layout: post
title: "DiskGenius: Restore, Recover, Create Bootable USB"
translated: false
type: note
---

**Question:** How do I use DiskGenius on Windows — specifically to restore a disk image to a USB drive, recover files, and other common tasks?

**Answer:**

DiskGenius is a powerful all-in-one disk tool for Windows. Here are the most common things you can do with it:

---

### 🔁 Restore a Disk Image to a USB Drive

This writes an image file (backup) back onto a physical disk (like a USB drive):

1. **Right-click** the destination disk (your USB) in the left panel → choose **"Restore Image File To Disk"**, or go to menu **Disk → Restore Image File To Disk**.
2. In the file dialog, **locate and select** your disk image file → click **Open**.
3. **Confirm** the target disk is correct → click **Start**.
4. A warning will appear that all data on the USB will be overwritten — click **OK** to confirm.
5. Wait for the restore to complete.

> ⚠️ Back up any existing data on the USB before doing this — it will be wiped!

---

### 💾 Recover Lost/Deleted Files from USB

When you open DiskGenius, all connected storage devices are shown in the left panel. If a USB drive is connected, it appears there (e.g., as "RD1"). If DiskGenius can't detect the device at all, it may be physically damaged and software recovery won't work.

To recover files:

1. Select the USB drive or partition in the left panel.
2. Click **File → Recover Lost Files** (or right-click the drive).
3. Choose scan mode — you can enable **"Search For Known File Types"** to scan sector-by-sector for specific file types (photos, videos, docs, etc.). Note that this mode recovers files without their original names or folder structure.
4. Preview and save the recovered files to a **different** drive.

---

### 📀 Create a Bootable WinPE USB Drive

1. Insert a USB drive and launch DiskGenius.
2. Click **Tools → Create WinPE Bootable USB Drive of DiskGenius**.
3. Click **OK** and wait a few seconds for the bootable disk to be created.

Requirements: the USB must be formatted as FAT32, exFAT, or NTFS, and have at least **800 MB** of free space. For UEFI computers, format the USB as **FAT32** beforehand.

---

### 🗂️ Other Common Features

DiskGenius also supports: partition recovery, cloning disks, backing up a disk to an image file, rebuilding MBR, quick partitioning, verifying and repairing bad sectors, converting dynamic disks to basic, and system migration.

---

**References:**

- [DiskGenius Official User Guide](https://www.diskgenius.com/manual/)
- [Restore Disk From Image File – DiskGenius Manual](https://www.diskgenius.com/manual/restore-disk-from-image-file.php)
- [How to Recover Lost Data with DiskGenius](https://www.diskgenius.com/how-to/recover-lost-data-with-diskgenius.php)
- [Create WinPE Bootable USB – DiskGenius Manual](https://www.diskgenius.com/manual/create-winpe-bootable-disk-for-diskgenius.php)
