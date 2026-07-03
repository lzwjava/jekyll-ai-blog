---
audio: false
generated: true
image: false
lang: en
layout: post
title: Recover from a Failed Linux Kernel Boot
translated: false
type: note
---

Question: I built a custom Linux kernel, rebooted Fedora on a MacBook Pro, and now it won’t start—what should I do?

Answer:

This usually means the system can’t boot the new kernel (missing boot entry, broken initramfs, or EFI/GRUB issue). Don’t worry—your data is likely still fine. The goal is to boot a rescue environment and fix the bootloader/kernel.

---

## 1. First check: is it completely dead or just not booting Linux?

Try these:

* Hold the **power button for ~10 seconds** to fully shut down
* Turn it on again
* Immediately hold **Option (⌥)** key (Intel Mac) or press power + hold startup options (Apple Silicon differs)

If you see:

* **“EFI Boot” / “Fedora”** → select it
* Nothing Linux-related → boot entry may be broken

---

## 2. Boot from a Fedora Live USB (most reliable fix)

You will likely need another computer to create a USB:

* Download Fedora Workstation ISO
* Flash it using:

  * Rufus (Windows)
  * balenaEtcher (Mac/Linux)

Boot MacBook:

* Hold **Option (⌥)** at startup
* Select **EFI USB / Fedora Live**

---

## 3. Once inside Live environment: repair system

Open terminal and do:

### Find your Linux root partition

```bash
lsblk
```

Look for something like:

* `/dev/nvme0n1pX` (root partition)

---

### Mount system

```bash
sudo mount /dev/nvme0n1pX /mnt
sudo mount --bind /dev /mnt/dev
sudo mount --bind /proc /mnt/proc
sudo mount --bind /sys /mnt/sys
sudo mount --bind /run /mnt/run
```

---

### Enter system (chroot)

```bash
sudo chroot /mnt
```

---

## 4. Fix kernel / boot issue

### Option A: reinstall kernel (safe)

```bash
dnf reinstall kernel-core kernel-modules kernel
```

### Option B: rebuild initramfs

```bash
dracut --regenerate-all --force
```

---

## 5. Reinstall GRUB (important on Mac EFI)

For UEFI systems:

```bash
grub2-install --target=x86_64-efi --efi-directory=/boot/efi --bootloader-id=fedora
grub2-mkconfig -o /boot/grub2/grub.cfg
```

---

## 6. Exit and reboot

```bash
exit
reboot
```

Remove USB when rebooting.

---

## 7. If you compiled your own kernel (likely cause)

Your build shows:

> custom kernel + “built successfully”

But common problems:

### Possible failure causes:

* Kernel not copied to `/boot`
* Missing `initramfs`
* GRUB not updated
* Kernel missing modules (especially storage driver!)
* EFI entry not pointing to new kernel

---

## 8. Quick recovery trick (if GRUB still works)

At GRUB menu:

* Press `e`
* Boot old kernel manually

If old kernel works → your custom kernel is broken, not system.

---

## 9. Worst case (still fixable)

If nothing works:

* Boot Live USB
* Backup `/home`
* Reinstall Fedora without touching home partition

---

## If you want next step help

Tell me:

* Intel Mac or Apple Silicon?
* Do you still see GRUB menu?
* What exactly happens on boot (black screen / Apple logo / EFI shell)?

I can give a precise recovery path based on that.