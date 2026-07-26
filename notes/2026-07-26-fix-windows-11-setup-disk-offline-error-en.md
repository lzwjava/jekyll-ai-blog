---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix Windows 11 setup disk offline error
translated: false
type: note
---

Question: Windows 11 setup shows "partition is of an unrecognized type" / "selected volume is offline" — how to fix?

Answer: This happens when the disk is in a RAID/dynamic-disk state, or has a foreign disk signature (common after pulling a drive from another RAID-configured machine, or a disk that was part of Intel RST/VROC). Setup's GUI "Bring Disk Online" button is greyed out because it can't handle it — drop to diskpart.

1. Press `Shift + F10` on the setup screen to open a command prompt.
2. Run:

```
diskpart
list disk
select disk 1          # match the disk index from the photo
detail disk             # check if it says "Status: Offline" and why
attributes disk clear readonly
online disk
```

3. If it still won't come online (foreign/dynamic disk):

```
list volume
select volume 1
attributes volume clear readonly
```

4. If the disk shows as **Dynamic** instead of **Basic**, Setup can't install to it at all — you must convert it. This is destructive:

```
clean
convert basic
create partition primary
format fs=ntfs quick
```

`clean` wipes the partition table on that disk — make sure you selected the *right* disk number, not your source/data drive. Run `list disk` again after `select disk` to confirm before `clean`.

5. Exit diskpart (`exit`), close cmd, click **Refresh** in Setup, then try Next again.

Root cause is almost always: disk was previously used in a RAID array (Intel RST), was a dynamic disk from Storage Spaces, or has GPT protective MBR confusion from a different OS. If this is a fresh NVMe that was never touched, check BIOS SATA mode (RAID vs AHCI) — switching modes mid-install causes exactly this.

References:
- [Diskpart command reference - Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/diskpart)
- [Fix: Windows Setup could not configure Windows on this computer's hardware](https://learn.microsoft.com/en-us/troubleshoot/windows-client/installing-updates-features-roles/windows-setup-installation-issues)
