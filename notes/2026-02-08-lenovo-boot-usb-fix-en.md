---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Fix Lenovo Boot Ignores Ubuntu USB
translated: false
type: note
---

Question: My Ubuntu USB was made with the dd command, not Etcher. On my Lenovo XiaoXin laptop, when I select the Ubuntu option in the boot menu, it still boots into normal mode (Windows) instead of Ubuntu. What should I do?

Answer:

The fact that you used `dd` to create the Ubuntu USB is **not** the problem — `dd` is a perfectly valid and commonly used method for making bootable Ubuntu USBs (it creates an exact copy of the ISO). It produces the same result as Etcher or Rufus in most cases, and Ubuntu ISOs boot fine when written with `dd`. The issue is almost certainly with your Lenovo XiaoXin laptop's BIOS/UEFI settings, not the USB creation method.

Lenovo XiaoXin laptops (Chinese domestic IdeaPad series) use UEFI firmware with **Secure Boot** enabled by default. Ubuntu supports Secure Boot, but sometimes compatibility issues occur (especially with certain ISOs, kernels, or if the USB is not detected as a valid signed EFI boot entry). More commonly on Lenovo laptops, when you select the USB in the **one-time boot menu** (Fn+F12), but the system ignores it and boots Windows anyway, the root causes are:

1. **Secure Boot** is still enabled and blocking the boot (even if Ubuntu should work with it).
2. **Boot Mode** is set to "UEFI Only" without proper USB detection, or needs "UEFI/Legacy (CSM)" or "Both" enabled.
3. The USB appears in the boot menu but isn't prioritized correctly, or the firmware skips it.

### Recommended Fix Steps (in order)

1. **Enter BIOS Setup** (not just the boot menu):
   - Power off the laptop completely.
   - Power on and **immediately spam F2** (or Fn+F2) repeatedly when the Lenovo logo appears.
     (Some XiaoXin models use Fn+F2, Novo button if present, or F1/Fn+F1 — try variations.)
   - This should enter the full BIOS/UEFI setup menu.

2. **Disable Secure Boot**:
   - Go to the **Security** tab (or Boot → Secure Boot).
   - Set **Secure Boot** to **Disabled**.
   - If it asks to clear keys or switch to "Setup Mode" → do so.
   - Save and exit (usually F10 → Yes).

3. **Check/Change Boot Mode** (very important for many Lenovo models):
   - Go to **Boot** or **Startup** tab.
   - Look for **Boot Mode**, **UEFI/Legacy Boot**, or **CSM** (Compatibility Support Module).
   - Change it to **Both** (UEFI + Legacy/CSM) or **Legacy First** if "Both" isn't available.
     (Ubuntu works best in UEFI mode, but enabling CSM often helps detection on picky Lenovo firmware.)
   - Ensure **USB Boot** or **External Device Boot** is enabled if such an option exists.

4. **Set Boot Order / USB Priority** (optional but helpful):
   - In the Boot tab, move the USB device (or "USB HDD", "Removable Device") higher in the list if it appears.
   - Some models have a separate "Boot Priority" for UEFI vs Legacy.

5. **Save, Exit, and Test Boot Menu Again**:
   - Save changes (F10 → Yes) and reboot.
   - Plug in your Ubuntu USB.
   - Spam **Fn + F12** (or just F12) at the Lenovo logo to open the one-time boot menu.
   - Select the entry that says something like:
     - UEFI: [USB brand/model] (e.g., UEFI: SanDisk)
     - Or just the USB name if no UEFI prefix.
   - Avoid selecting non-UEFI entries if possible (unless you changed to Legacy mode).

6. **If It Still Fails**:
   - Recreate the USB using **Ventoy** (highly recommended for Lenovo laptops) — copy the Ubuntu ISO to a Ventoy USB and boot from Ventoy's menu. Ventoy handles many UEFI/Secure Boot quirks better.
   - Or remake with **Rufus** (on Windows) using **DD Image** mode (not ISO mode) for maximum compatibility.
   - Try a different USB port (some Lenovo models are picky with USB 3.0 vs 2.0 ports).
   - Update your BIOS from Lenovo's Chinese site (if available for your exact XiaoXin model) — newer firmware sometimes fixes USB boot issues.
   - Test the USB on another computer to confirm it boots to the Ubuntu live environment.

After disabling Secure Boot and enabling CSM/Both mode, most users report the USB boots correctly into the Ubuntu installer/live session. Once Ubuntu is installed, you can re-enable Secure Boot if desired (Ubuntu signs its bootloader).

References:

- [https://support.lenovo.com/us/en/solutions/ht500207-how-to-boot-from-usb-disk-in-the-bios-boot-menu-windows-8-windows-10-ideapadlenovo-laptops](https://support.lenovo.com/us/en/solutions/ht500207-how-to-boot-from-usb-disk-in-the-bios-boot-menu-windows-8-windows-10-ideapadlenovo-laptops)
- [https://askubuntu.com/questions/891248/ubuntu-16-04-how-can-i-disable-secure-boot](https://askubuntu.com/questions/891248/ubuntu-16-04-how-can-i-disable-secure-boot)
- [https://www.reddit.com/r/Lenovo/comments/wwkstm/new_laptop_cannot_boot_to_usb_it_always_jumps](https://www.reddit.com/r/Lenovo/comments/wwkstm/new_laptop_cannot_boot_to_usb_it_always_jumps)
- [https://forums.lenovo.com/t5/Other-Linux-Discussions/BIOS-does-not-recognize-USB-boot-media/m-p/5304674](https://forums.lenovo.com/t5/Other-Linux-Discussions/BIOS-does-not-recognize-USB-boot-media/m-p/5304674)
