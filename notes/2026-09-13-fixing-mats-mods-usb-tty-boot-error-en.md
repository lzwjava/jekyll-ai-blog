---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixing MATS MODS USB TTY Boot Error
translated: false
type: note
---

**Question:** I followed the instructions from post #70 (the GRUB bare-bone setup for MATS/MODS), but the USB won't boot — it seems stuck and can't start a TTY (terminal). What's going wrong and how do I fix it?

---

**Answer:**

The "can't start tty" error is a common Linux boot issue with these bare-bone USB setups. Here are the most likely causes and fixes:

**1. Wrong Boot Mode (UEFI vs Legacy)**

The GTX version boots as **Legacy only** (no UEFI), while the RTX version boots as both Legacy and UEFI. RTX 50 series requires UEFI boot.

Make sure your BIOS boot mode matches your card generation:
- GTX card → Set BIOS to **Legacy/CSM mode**
- RTX card → Legacy or UEFI both work
- RTX 50xx → Must use **UEFI**

**2. GRUB vs Syslinux — Try the Other One**

Post #69 offers a **Syslinux version** and post #70 offers a **GRUB version**. If the GRUB version fails to boot or gets stuck on TTY, try the Syslinux version instead — some systems are more compatible with one bootloader over the other.

The Syslinux setup (`mats_syslinux.zip`) and GRUB setup (`mats_grub.zip`) both use the same steps: format USB as FAT32, extract the executable onto the USB, and run the executable from the USB to create the bootloader.

**3. USB Format Issue**

The USB drive must be formatted with **default FAT32** before running the executable. If you used exFAT or NTFS, reformat to FAT32 and redo the setup.

**4. Screen Resolution Issue**

For the RTX image, screen resolution is forced at **1280x720** and can be changed inside the `syslinux.cfg` file. If your display doesn't support that resolution, the boot may appear to hang (but is actually running without a visible output). Try a different monitor or TV.

**5. GPU Has No Display Output**

If the GPU itself is faulty and produces no display, you need a motherboard and CPU with an iGPU, connect your display to the **motherboard's display output**, then run `modsinit` before running `mods` or `mats -n 1`.

---

**Quick Checklist:**

| Check | Action |
|---|---|
| Boot mode | Match Legacy/UEFI to your GPU generation |
| Bootloader | Try Syslinux if GRUB fails |
| USB format | Must be FAT32 |
| Display output | Use iGPU output if GPU has no signal |
| Resolution | Try different monitor if screen is blank |

---

**References:**
- [Nvidia MATS & MODS USB stick (with NVMT) — Levirepair Forum](https://www.levirepair.eu/infusions/forum/viewthread.php?thread_id=3&pid=70#post_70)
