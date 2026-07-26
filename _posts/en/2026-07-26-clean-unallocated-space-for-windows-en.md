---
audio: false
generated: true
image: false
lang: en
layout: post
title: Clean Unallocated Space for Windows
translated: false
type: note
---

Question: Used Setup's own "Delete Partition" to remove the 476GB partition on Disk 0, now it shows as unallocated space — what next?

Answer: Good, that's the simplest path and it worked. From here:

1. **Select the unallocated space** on Disk 0.
2. Click **Next** directly — do NOT manually create a partition first. Windows Setup will auto-create the 4 partitions it needs (Recovery, EFI System, MSR, and the actual Windows partition) when you let it work with raw unallocated space on a GPT disk.
3. If you manually hit **Create Partition** yourself instead, Setup will only make one partition and you'll have to deal with the EFI/MSR partitions separately — just let it auto-split.

If Next now proceeds without the "unrecognized type / offline" error, you're clear — that error was tied to the old Linux Mint partition signature (LVM/RAID metadata) on that specific partition, and deleting it wiped the metadata that was confusing Windows's disk driver.

One thing to check: your photo showed **two disks**, each with two partitions (Disk 0 and Disk 1). If Disk 1 also has leftover Mint partitions (e.g. a separate `/home` partition or swap), and you plan to install Windows fresh with no dual-boot, you may want to delete those too now to avoid leftover Linux partitions cluttering Disk Management later. If you want to keep Mint on Disk 1 for dual-boot, leave it alone — Windows Setup won't touch other disks unless you select them.

References:
- [Windows Setup - create and format hard disk partitions](https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/configure-uefigpt-based-hard-drive-partitions)
