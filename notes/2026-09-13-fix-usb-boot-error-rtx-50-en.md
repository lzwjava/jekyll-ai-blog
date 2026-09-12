---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix USB Boot Error RTX 50
translated: false
type: note
---

**Question:** How do I fix the boot error when trying to run a GPU test program for the 50-series on a USB disk?

**Answer:**

The error `Partition with root filesystem not found` on a TinyLinux USB boot is very common with **newer hardware (RTX 50-series)** because the USB was likely created for older systems. Here's how to fix it:

---

**Root Cause**
RTX 50-series systems often use:
- **NVMe-only** storage (no SATA), causing device name mismatches
- **USB 3.x controllers** that the old TinyLinux kernel doesn't recognize fast enough
- **Secure Boot** blocking unsigned kernels

---

**Fix Options (try in order):**

**① Add boot delay (easiest)**
At the GRUB/boot menu, press `e` to edit boot parameters and add:
```
rootdelay=10
```
This gives the kernel more time to detect the USB drive.

**② Fix the `root=` parameter**
At GRUB menu, press `e` and change the root line to use your USB device. In the emergency shell, first find it:
```sh
lsblk
# Look for your USB, e.g. /dev/sdb1 or /dev/sda1
```
Then reboot and at GRUB press `e`, find the line with `root=` and change it to:
```
root=/dev/sdb1   # or whatever lsblk showed
```

**③ Disable Secure Boot in BIOS**
- Reboot → Enter BIOS (usually `Del` or `F2`)
- Find **Secure Boot** → Set to **Disabled**
- Save and retry booting from USB

**④ Re-flash the USB with correct settings**
The ISO image may need to be re-written properly:
```sh
# On Linux/Mac — replace /dev/sdX with your USB drive
sudo dd if=tinylinux.iso of=/dev/sdX bs=4M status=progress oflag=sync

# Or use Rufus on Windows:
# - Partition scheme: MBR (for BIOS) or GPT (for UEFI)
# - File system: FAT32
```

**⑤ Enable CSM/Legacy Boot in BIOS**
- Enter BIOS → find **CSM** or **Legacy Boot**
- Enable it, then try booting USB again

---

**Which GPU test program are you using?**
If it's a specific tool like **OCCT**, **FurMark**, or a vendor-specific RTX 50-series diagnostic, let me know — some have updated ISOs specifically for new hardware.

---

**References:**
- [TinyLinux Boot Issues – kernel.org](https://www.kernel.org/doc/html/latest/admin-guide/kernel-parameters.html)
- [Rufus USB creation guide](https://rufus.ie/en/)
- [NVIDIA RTX 50-series Linux support](https://www.nvidia.com/en-us/drivers/unix/)
