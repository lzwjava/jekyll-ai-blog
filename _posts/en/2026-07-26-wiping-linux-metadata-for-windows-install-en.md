---
audio: false
generated: true
image: false
lang: en
layout: post
title: Wiping Linux Metadata for Windows Install
translated: false
type: note
---

Question: Previous OS was Linux Mint on a Lenovo Xiaoxin, now installing Windows 11 and getting "partition is of an unrecognized type" / "volume is offline" — how to fix?

Answer: This is almost always leftover Linux disk metadata that Windows's partition driver can't parse — either an **mdadm RAID superblock** (Linux Mint installers sometimes create software RAID metadata even for single-disk setups, or leftover from `install_from_iso` GPT+LVM layouts), or **LVM/LUKS signatures** on the partition table that Windows misreads as a foreign/dynamic disk, making it show offline.

Since you're doing a fresh Windows install (no data to keep), the fastest fix is to nuke the whole disk table rather than fight the GUI tools:

1. `Shift + F10` to open cmd on the Setup screen.
2. Run:

```
diskpart
list disk
select disk 0          # pick the disk that showed the error, check size to confirm
detail disk             # confirms Offline / foreign / dynamic status
clean
convert gpt
create partition primary
format fs=ntfs quick
exit
```

3. Close cmd, click **Refresh** on the Setup screen, select the newly created partition, hit **Next**.

Why `clean` is necessary here specifically: Windows's `Bring Disk Online` in the GUI only handles simple offline states (like a disk signature collision), not Linux RAID/LVM signatures sitting in the partition table or at the end of the disk. `diskpart clean` wipes MBR/GPT + any RAID metadata blocks, so Windows sees a truly blank disk and stops complaining.

If this Lenovo Xiaoxin has **dual storage** (NVMe + eMMC, common on the Xiaoxin Air/Pro models) or was set up with **Mint's LVM full-disk encryption**, double check `list disk` sizes carefully before `select disk` — you don't want to clean the wrong one if you're dual-booting and want to keep Mint on a second drive.

If you *do* want to keep Mint on this disk (dual boot) instead of wiping, tell me and I'll give you the LVM-preserving version — that's a different, non-destructive path (delete/recreate only the Windows target partition, leave Mint's LVM PVs untouched).

References:

- [Diskpart command reference - Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/diskpart)
- [Windows Setup "unrecognized partition" troubleshooting](https://learn.microsoft.com/en-us/troubleshoot/windows-client/installing-updates-features-roles/windows-setup-installation-issues)
