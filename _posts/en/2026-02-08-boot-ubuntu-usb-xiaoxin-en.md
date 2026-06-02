---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Boot Ubuntu USB on Lenovo XiaoXin
translated: false
type: note
---

Question: How to boot from an Ubuntu live USB on a Lenovo XiaoXin 14 IAH8 laptop? The user has created a bootable USB using dd with ubuntu-24.04.3-desktop-amd64.iso.

Answer:

Your dd command created a standard bootable Ubuntu 24.04.3 live USB (UEFI-compatible by default). Here's how to boot from it on your Lenovo XiaoXin 14 IAH8 (a domestic Chinese IdeaPad-like model).

### Step-by-step to boot the Ubuntu live USB

1. **Insert the USB drive**
   Plug the USB into a USB port (preferably a USB 3.0/3.1 port for faster loading).

2. **Power off the laptop completely**
   Shut down Ubuntu fully (not restart, because fast boot / hybrid shutdown can interfere).
   Hold the power button if needed to force shutdown.

3. **Power on and enter the boot menu**
   - Press the power button.
   - **Immediately and repeatedly tap Fn + F12** (or just F12 if your keyboard doesn't require Fn for function keys) as soon as the Lenovo logo appears.
     - Keep tapping until the **Boot Menu** (Startup Menu) appears.
   - In the boot menu, look for entries like:
     - UEFI: [USB brand name, e.g. SanDisk, Kingston, USB Flash]
     - or just the USB name
   - Use arrow keys to highlight the **UEFI USB entry** (avoid Legacy/CSM if shown) → press **Enter**.

   If Fn + F12 doesn't work after several tries:
   - Try just **F12** alone.
   - Some XiaoXin models use a small **Novo button** (a pinhole near the power button or on the side) — press it with a paperclip while powered off → select **Boot Menu** from the Novo menu → insert USB if not already in.

4. **If the boot menu doesn't appear or USB is missing** → Enter full BIOS Setup first
   - Power on → immediately and repeatedly tap **Fn + F2** (or F2) at the Lenovo logo.
   - In BIOS:
     - Go to **Security** tab → **Secure Boot** → set to **Disabled** (important for most live USBs).
     - Go to **Boot** / **Startup** tab:
       - Ensure **Boot Mode** is **UEFI** (or **UEFI Only**; do NOT set to Legacy unless UEFI fails).
       - If there's **UEFI/Legacy Boot** → set to **Both** or **UEFI First**.
       - In **Boot Priority** or **Boot Order**, move **USB HDD** or **UEFI: USB** to the top (use +/− or F5/F6 keys).
     - Press **F10** → **Yes** to save and exit.
   - The laptop will restart → now repeat step 3 (Fn + F12) to select the USB quickly.

5. **Once booted into Ubuntu**
   - You should see the GRUB menu (Ubuntu options).
   - Choose **Try Ubuntu** (live session) — this runs Ubuntu from USB without touching your disk.
   - Or choose **Install Ubuntu** if you want to reinstall/repair.

### Common fixes if it still won't boot

- **USB not listed** → Recreate the USB with a different tool (Ventoy, balenaEtcher, or Startup Disk Creator in another Ubuntu) — dd sometimes has edge-case issues with certain BIOS.
- **Black screen / stuck** → In boot menu, try the non-UEFI USB entry if available (rare).
- **Secure Boot error** → Must disable in BIOS (step 4).
- **Fast boot interference** → Always fully shut down (not restart) before trying.
- Wrong port → Try a different USB port (some Lenovo models are picky with USB-C vs USB-A).

This should get you into the live environment so you can repair your broken system (chown issue from earlier).

References:

- [https://support.lenovo.com/us/en/solutions/ht104668-how-to-select-boot-device-from-bios-boot-menu-ideapad-thinkpad-thinkstation-thinkcentre-ideacentre](https://support.lenovo.com/us/en/solutions/ht104668-how-to-select-boot-device-from-bios-boot-menu-ideapad-thinkpad-thinkstation-thinkcentre-ideacentre)
- [https://wiki.archlinux.org/title/Lenovo_XiaoXin_15are_2020](https://wiki.archlinux.org/title/Lenovo_XiaoXin_15are_2020) (similar XiaoXin series info on keys)
- [https://support.lenovo.com/us/en/solutions/ht500216-recommended-way-to-enter-bios-ideapad](https://support.lenovo.com/us/en/solutions/ht500216-recommended-way-to-enter-bios-ideapad)
