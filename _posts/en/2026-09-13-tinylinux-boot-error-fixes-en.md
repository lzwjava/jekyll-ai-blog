---
audio: false
generated: true
image: false
lang: en
layout: post
title: TinyLinux Boot Error Fixes
translated: false
type: note
---

**Question:** What do these Linux boot errors mean, and how can I fix them?

**Answer:**

The screen shows a TinyLinux 20.10 boot failure with two distinct issues:

**1. ACPI BIOS Errors (non-critical)**

```
ACPI BIOS Error: Could not resolve symbol [\_SB.PCI0.SAT0.SPT0._GTF.DSSP], AE_NOT_FOUND
ACPI Error: Aborting method \_SB.PCI0.SAT0.SPT0._GTF due to previous error
```

These are ACPI table bugs in the firmware related to SATA/storage device initialization. They're warnings, not the root cause of the boot failure — the system can usually still boot despite them.

**2. Root Filesystem Not Found (critical — this is why it dropped to a shell)**

```
Partition with root filesystem not found. Waiting...
Giving up...
/bin/sh: can't access tty: job control turned off
```

The kernel cannot find the partition it's supposed to boot from. This is the actual failure.

---

**Common Causes & Fixes:**

| Cause | Fix |
| --- | --- |
| Wrong `root=` parameter in bootloader | Edit GRUB: change `root=UUID=...` or `root=/dev/sdXY` to the correct partition |
| Drive detected as different device name (e.g., `sda` → `nvme0n1`) | Check with `lsblk` in the emergency shell, then update GRUB |
| Corrupted or missing initramfs | Rebuild: `update-initramfs -u` from a live USB chroot |
| Bootloader installed on wrong disk | Reinstall GRUB to the correct disk |
| UUID mismatch after disk replacement | Update `/etc/fstab` and GRUB config with the correct UUID |

**Immediate Steps:**

Since you're in the emergency shell (`/ #`), run:

```sh
lsblk        # See all detected partitions
blkid        # See UUIDs of all partitions
cat /proc/cmdline   # See what root= the kernel was given
```

This will tell you whether the partition exists but was named differently, or is genuinely missing.

---

**References:**

- [Linux Kernel Boot Parameters](https://www.kernel.org/doc/html/latest/admin-guide/kernel-parameters.html)
- [GRUB2 Recovery – Arch Wiki](https://wiki.archlinux.org/title/GRUB/Restore_GRUB_Legacy)
- [initramfs troubleshooting – Ubuntu Docs](https://wiki.ubuntu.com/Initramfs)
