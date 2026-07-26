---
audio: false
generated: true
image: false
lang: en
layout: post
title: Clean Disk 0 Convert GPT Install
translated: false
type: note
---

Question: Disk 0 confirmed as the UMIS NVMe 512GB drive, correct target — proceed with clean?

Answer: Yes, this is the right disk. Confirmed: NVMe, Online, 476GB NTFS Volume C, Healthy, not read-only. This is your target SSD, not the small Disk 1.

Proceed:

```cmd
clean
```

Wait for `DiskPart succeeded in cleaning the disk.`

```cmd
convert gpt
```

Wait for `DiskPart successfully converted the selected disk to GPT format.`

```cmd
exit
```

Close the command prompt window entirely, then from the Repair menu **restart into the Windows 11 USB installer** (not Repair again — you need the full Setup GUI to get to partition selection). Go through language/edition screens to "Select location to install Windows 11," click **Refresh**, select the unallocated Disk 0, click **Next**.

**Critical check this time:** after clicking Next, wait a few seconds for Setup to auto-create partitions, then if it errors again immediately go back to the partition list screen and look — you should see 4 entries on Disk 0 (System/EFI, MSR, Primary, Recovery). If EFI System Partition is present this time, the install should proceed past the reboot without the earlier failure.
