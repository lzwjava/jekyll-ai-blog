---
audio: false
generated: true
image: false
lang: en
layout: post
title: Syslinux XZ Decompression Failure
translated: false
type: note
---

**Question:** Why does "XZ compressed data is corrupt — System halted" appear in Syslinux when booting from a MOD 50-series (or similar) image, and what does it mean?

---

**Answer:**

## What This Error Means

When Syslinux loads a Linux kernel or initramfs, those files are compressed using XZ (or similar formats). The error "XZ-compressed data is corrupt — System halted" occurs during the kernel decompression stage — Syslinux successfully loads the file, but when the kernel tries to decompress it into memory, the data doesn't pass integrity checks and the system halts completely.

This is **not** usually a software bug — it most commonly signals a **hardware or media problem**.

---

## Root Causes (Most to Least Common)

### 1. Faulty RAM (Most Common)
One confirmed cause is a faulty RAM module — after replacing the bad RAM, the update installs with no issue. The decompression process requires memory to be reliable; even a single bit flip corrupts the output.

### 2. Bad USB Drive or Write Error
A bad USB flash drive can cause this error. Writing the same ISO to a different USB drive resolved the issue in one case. The physical media may have bad sectors even if it appears healthy.

### 3. Old or Incompatible Hardware
On older machines, the error can appear intermittently. ACPI settings can also create the error, which can sometimes be worked around by appending `acpi=off` to the kernel boot parameters.

### 4. Faulty Optical Drive (if booting from CD/DVD)
A faulty DVD drive has been identified as a cause in at least one case.

### 5. Incomplete or Interrupted Write
The error can occur even when an ISO checksum is correct and boots fine on a different machine, suggesting the issue is hardware-specific rather than a corrupt image file.

---

## Troubleshooting Steps

| Step | Action |
|---|---|
| 1 | Run **Memtest86+** to test RAM |
| 2 | Try a **different USB drive** or flash media |
| 3 | Re-flash the image with a verified tool |
| 4 | Try booting on a **different machine** to isolate |
| 5 | Add `acpi=off` to kernel boot parameters |
| 6 | Reseat or swap RAM modules one at a time |

---

## Note on "MOD 50 Series Only Image"

If you're using a specific embedded appliance image (like a NAS, UPS controller, or network device with "MOD 50" branding) and only that particular image triggers this error, the likely culprits are: the image was written incompletely, the device's flash storage has a bad block, or the device's RAM has a fault in the address range used during decompression. Re-flashing via the manufacturer's recovery method is the recommended first step.

---

**References:**
- [LibreELEC Forum — Faulty RAM causing XZ corrupt error](https://forum.libreelec.tv/thread/9589-solved-update-to-8-1-0-on-generic-failed-xz-compressed-data-is-corrupt-system-ha/)
- [Arch Linux Forums — XZ-compressed data is corrupt](https://bbs.archlinux.org/viewtopic.php?id=144116)
- [Arch Linux Forums — ACPI workaround for old hardware](https://bbs.archlinux.org/viewtopic.php?id=144116)
- [Linux Mint Forums — Bad USB drive as root cause](https://forums.linuxmint.com/viewtopic.php?t=204857)
- [Gentoo Forums — Hardware-specific XZ corrupt error](https://forums.gentoo.org/viewtopic.php?t=987516)
