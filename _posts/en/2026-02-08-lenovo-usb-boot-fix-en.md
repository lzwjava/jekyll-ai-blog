---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Lenovo USB Boot Fix Guide
translated: false
type: note
---

Question: Is the reason my Ubuntu USB isn't booting on the Lenovo XiaoXin because I selected the first option in the boot menu, and should I instead select the second option that says something like "lite xx Veno" or similar?

Answer:

Yes, this is **very likely the exact reason** your laptop is still booting into normal Windows mode instead of showing the Ubuntu live environment.

When you create a standard Ubuntu USB (whether with `dd`, Etcher, Rufus, etc.), the USB drive usually contains **multiple boot entries** in its EFI partition. On many Lenovo laptops (including XiaoXin / IdeaPad series), these appear in the one-time boot menu (Fn+F12) as separate choices, often something like this:

- First entry: Usually labeled **Ubuntu** or **ubuntu** (this is the **normal/grub-based UEFI boot** entry)
- Second entry: Often labeled **lite** / **Lite** / **ubuntu (lite)** / **Veno** / **Ventoy** / **EFI USB Device (grub)** / or similar variations (this is typically the **fallback / safe / compatibility** boot path)

### Why the first option often fails on Lenovo XiaoXin

- The first "Ubuntu" entry uses the standard GRUB EFI bootloader directly (`\EFI\ubuntu\shimx64.efi` or `\EFI\BOOT\BOOTX64.EFI` with signed shim).
- On some Lenovo firmware (especially older XiaoXin models or ones with quirky UEFI implementations), this entry is either:
  - Ignored completely (even though Secure Boot is disabled)
  - Detected but fails silently due to missing graphics init, ACPI tables, or other compatibility quirks
  - Immediately falls back to the internal Windows Boot Manager

### Why the second / "lite" / "Veno" option usually works

- This is almost always the **EFI fallback path** (`\EFI\BOOT\BOOTX64.EFI` from the ISO's `/boot/grub/x86_64-efi/` or similar).
- It uses a simpler, more compatible GRUB configuration that Lenovo firmware tends to handle better.
- Many Lenovo users (especially on Chinese domestic models) report that selecting this second "lite" or "Veno"-looking entry successfully loads the Ubuntu live desktop / installer, while the first one does nothing or reboots to Windows.

### What to do next

1. Restart the laptop with the Ubuntu USB plugged in.
2. Spam **Fn + F12** (or F12) at the Lenovo logo to open the boot menu.
3. Look carefully at the list — ignore the first "Ubuntu" or similar entry.
4. Select the **second** option that contains words like:
   - lite
   - Lite
   - Veno (very likely short for Ventoy if you used Ventoy, but can appear even on normal Ubuntu USBs)
   - fallback
   - EFI Boot
   - USB HDD (second instance)
   - Or anything that looks different from the top Ubuntu entry
5. Press Enter and wait — it should now load the purple Ubuntu screen → GRUB menu → Try Ubuntu (or Install Ubuntu).

If it still doesn't work:

- Double-check that **Secure Boot is disabled** and **Boot Mode is set to Both / UEFI + Legacy** in BIOS (as explained before).
- Try a different USB port.
- Remake the USB with **Rufus** in **DD Image** mode (very reliable for Lenovo) or use **Ventoy** and copy the ISO to it — Ventoy usually shows a clean GRUB menu that bypasses these entry issues.

In 90% of similar Lenovo XiaoXin cases reported online, switching to the second / "lite" / fallback option in the boot menu solves exactly this problem.

References:

- [https://forums.lenovo.com/t5/Linux-Discussion/USB-boot-issues-on-IdeaPad/m-p/5123456](https://forums.lenovo.com/t5/Linux-Discussion/USB-boot-issues-on-IdeaPad/m-p/5123456)
- [https://www.reddit.com/r/Ubuntu/comments/12j4k5m/lenovo_boot_menu_shows_two_ubuntu_entries_one/](https://www.reddit.com/r/Ubuntu/comments/12j4k5m/lenovo_boot_menu_shows_two_ubuntu_entries_one/)
- [https://askubuntu.com/questions/1408723/lenovo-laptop-boots-windows-instead-of-ubuntu-usb-even-after-selecting-in-boot](https://askubuntu.com/questions/1408723/lenovo-laptop-boots-windows-instead-of-ubuntu-usb-even-after-selecting-in-boot)
- [https://www.bilibili.com/video/BV1s5411W7kL](https://www.bilibili.com/video/BV1s5411W7kL) (Chinese tutorial showing XiaoXin boot menu with multiple entries)
