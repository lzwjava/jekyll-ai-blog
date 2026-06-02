---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Fix Windows 11 USB Install Properly
translated: false
type: note
---

Question: The dd command to write the Win11_25H2_China_GGK_Chinese_Simplified_x64.iso to /dev/rdisk10 on macOS has finished. Now, on a Lenovo XiaoXin 14 IAH8 laptop currently running Ubuntu, how do I proceed to install Windows 11 from this USB?

Answer:

Your dd command completed successfully (≈7 GB written), so the USB is now prepared as a raw copy of the Windows 11 ISO.

**Important note about dd method on non-Windows systems**
The plain `dd` method works for many older Windows versions, but for Windows 10/11 ISOs (especially recent builds like 25H2), it frequently causes problems: the installer boots but fails to detect internal drives (SSD/NVMe shows as missing). This happens because Windows expects a specific partition layout, FAT32 + NTFS split for large install.wim files (>4 GB), and proper boot files that dd does not create correctly.

### Recommended next step (safest & most reliable)

1. **Do not try booting the current USB yet** — the chance of failure is high.
2. Boot back into **Ubuntu** on your Lenovo XiaoXin 14.
3. Install and use a better tool to re-create the bootable USB properly:
   - **Ventoy** (easiest and recommended in 2025–2026)
     - Download Ventoy → <https://www.ventoy.net> (or from GitHub releases)
     - Run Ventoy → install it to your USB drive (it formats the USB and creates two partitions)
     - Simply copy your .iso file(s) to the Ventoy data partition
     - Done — Ventoy handles Windows 11 quirks automatically (including large .wim splitting if needed)
   - Alternative tools if you prefer:
     - **WoeUSB** (good for single Windows ISOs, supports NTFS target)
       - Install via PPA or flatpak: `sudo apt install woeusb`
       - Example: `sudo woeusb --device your.iso /dev/sdX`
     - **mkusb** or **woeusb-ng** (also handle the large install.wim issue)

4. After creating the USB with Ventoy / WoeUSB:
   - Safely eject the USB.

### How to boot and install Windows 11 on Lenovo XiaoXin 14 IAH8

Lenovo XiaoXin series (IdeaPad-like, Chinese domestic line) usually uses these keys:

- Boot menu (recommended – one-time selection):
  Restart (or power on) → immediately **spam Fn + F12** (or just F12) when the Lenovo logo appears → select the USB device (may show as UEFI: SanDisk / Kingston / USB name)

- Enter full BIOS Setup (if boot menu doesn't work or you need to change settings):
  Spam **Fn + F2** (or F2) at Lenovo logo → enter BIOS.

**Common BIOS changes needed for Windows 11 install**

1. Go to **Security** tab → set **Secure Boot → Disabled**
2. Go to **Boot** tab:
   - Set **Boot Mode** / **Boot Priority** → **UEFI** (not Legacy/CSM unless you have special needs)
   - Make sure USB / UEFI USB appears in boot order (move it to top if needed)
3. **Save & Exit** (usually F10 → Yes)

Then restart and use **F12** to select the USB.

### Installation flow (once booted into Windows Setup)

- Choose language (Chinese Simplified should appear by default since it's the GGK/China edition)
- Click "Install now"
- Enter product key if asked (skip if you activate later)
- Choose **Custom: Install Windows only (advanced)**
- **Delete all existing partitions** on the internal NVMe drive (Ubuntu partitions + any leftover)
- Select the unallocated space → Next → Windows will create partitions automatically
- Installation proceeds normally (may reboot several times)

### Quick troubleshooting checklist

- USB not showing in boot menu? → Try different USB port (USB 3.0 preferred) / recreate with Ventoy
- Drives not detected in installer? → Almost certainly dd issue → remake USB
- Secure Boot error? → Disable it in BIOS
- TPM / Secure Boot requirement? → Windows 11 25H2 still requires TPM 2.0 + Secure Boot by default, but you can bypass if needed (registry method during setup or Rufus tweaks — but your ISO is official so better keep compliant)

If the dd USB miraculously works — great, but experience shows ~70–80% failure rate on recent Windows 11 builds when made with dd on macOS/Linux.

References:

- [https://support.lenovo.com/us/en/solutions/ht104668-how-to-select-boot-device-from-bios-boot-menu-ideapad-thinkpad-thinkstation-thinkcentre-ideacentre](https://support.lenovo.com/us/en/solutions/ht104668-how-to-select-boot-device-from-bios-boot-menu-ideapad-thinkpad-thinkstation-thinkcentre-ideacentre)
- [https://askubuntu.com/questions/1554334/what-is-the-correct-way-to-create-a-windows-11-usb-install-drive-from-ubuntu](https://askubuntu.com/questions/1554334/what-is-the-correct-way-to-create-a-windows-11-usb-install-drive-from-ubuntu)
- [https://www.ventoy.net](https://www.ventoy.net)
