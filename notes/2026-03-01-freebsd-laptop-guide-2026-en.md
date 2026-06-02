---
audio: false
generated: true
image: false
lang: en
layout: post
title: FreeBSD Laptop Installation Guide 2026
translated: false
type: note
---

Question: How to install FreeBSD on a laptop?

Answer:

Here is a practical step-by-step guide to install **FreeBSD** on a modern laptop (as of early 2026, covering FreeBSD 14.3 or FreeBSD 15.0).

### Before You Start – Important Laptop Notes
FreeBSD works very well on many ThinkPads, some Dell Latitudes/Precisions, and Framework laptops. On many other modern laptops you will likely face these common challenges:

- Wi-Fi usually needs extra configuration (especially Intel AX2xx / BE2xx series)
- Function keys / brightness / touchpad sometimes need tweaks
- Hybrid GPU laptops (Intel + NVIDIA/AMD) need careful driver choice
- Battery life is usually worse than Linux/Windows

Check compatibility first:

- Look up your exact Wi-Fi chip → search "FreeBSD [your Wi-Fi model] iwlwifi OR iwm OR ath10k"
- See FreeBSD Hardware Notes for 14.2 / 14.3 / 15.0
- Framework laptops and many ThinkPads have the best community support

### Step-by-step Installation

1. **Download the correct image**
   Go to → https://www.freebsd.org/where/
   Recommended choices for laptops in 2026:

   - **memstick.img** (most common) → write to ≥8 GB USB
   - FreeBSD-15.0-RELEASE-amd64-memstick.img     (if 15.0 is out)
   - or FreeBSD-14.3-RELEASE-amd64-memstick.img

   Also download the **CHECKSUM.SHA256** file and verify.

2. **Create bootable USB**
   - **Linux / FreeBSD / macOS**: `dd if=FreeBSD-*.img of=/dev/sdX bs=1M status=progress`
   - **Windows**: Use Rufus (DD Image mode) or balenaEtcher

3. **Prepare the laptop BIOS/UEFI**
   - Enter BIOS (usually F2, Del, F12, Esc)
   - **Disable** Secure Boot
   - Set **UEFI** mode (almost always better in 2025+)
   - Set USB as first boot device or use one-time boot menu (F12 / F11 / Esc)

4. **Boot the installer**
   Insert USB → reboot → select USB from boot menu
   You should see the FreeBSD loader → press Enter (or wait) → choose **Install**

5. **Follow the bsdinstall menus** (text-based installer)

   | Menu                     | Recommended choice for laptop                                 | Notes |
   |--------------------------|-----------------------------------------------------------------------|-------|
   | Keymap                   | Belgian / Spanish / Swedish / ... or default US               |       |
   | Hostname                 | mylaptop / thinkpad / etc.                                    |       |
   | Distribution Set         | **ports** + **src** (very useful later)                       | At least base + kernel + lib32 |
   | Partitioning             | **Auto (ZFS)** or **Auto (UFS)**                              | ZFS is better if ≥16 GB RAM |
   | Pool Type (ZFS)          | stripe (single disk) or mirror (if 2+ disks)                  |       |
   | Encryption               | Usually **Yes** (GELI) – very easy in installer now           | Strongly recommended on laptop |
   | Root password            | Strong password                                               |       |
   | Network (during install) | Try wired Ethernet if possible                                | Wi-Fi usually not yet |
   | Time Zone                | Your region / city                                            |       |
   | System Configuration     | Enable **sshd** if you want remote access                     |       |
   | Final Configuration      | Usually **Yes** to all defaults                               |       |

6. **Finish & Reboot**
   Remove USB when prompted → system should boot into FreeBSD console (black screen with text login)

### After First Boot – Make the Laptop Usable

1. **Update the system immediately**

   ```shell
   freebsd-update fetch install
   shutdown -r now
   ```

   (or if using git src: `pkg install git` → follow handbook for src updating)

2. **Install binary package manager (pkg)**

   ```shell
   pkg update && pkg upgrade
   ```

3. **Install desktop environment** (one of the popular choices)

   ```shell
   # KDE Plasma (most polished in 2025–2026)
   pkg install kde5 sddm
   sysrc sddm_enable="YES"
   sysrc dbus_enable="YES"

   # or GNOME
   pkg install gnome gdm
   sysrc gdm_enable="YES"
   sysrc dbus_enable="YES"

   # or lightweight XFCE
   pkg install xfce xfce4-goodies slim
   sysrc slim_enable="YES"
   ```

4. **Enable graphics** (most common cases)

   - Intel → usually auto-detects (`drm-kmod`)
   - AMD   → `pkg install drm-kmod`
   - NVIDIA → `pkg install nvidia-driver` or `nvidia-driver-libs`

   ```shell
   sysrc kld_list+="i915kms"      # Intel newer chips
   # or
   sysrc kld_list+="amdgpu"       # AMD
   ```

5. **Wi-Fi – the hardest part on many laptops**

   Most common drivers in 2025–2026:

   - `iwlwifi`   Intel AX/BE series (best chance in FreeBSD 15)
   - `iwm`       older Intel AC
   - `ath10k` / `rtw88` / `rge`   various Realtek & Atheros

   Example (Intel AX210/AX211):

   ```shell
   pkg install wpa_supplicant
   sysrc wlans_iwlwifi0="wlan0"
   sysrc ifconfig_wlan0="WPA SYNCDHCP"
   ```

   Then create/edit `/etc/wpa_supplicant.conf`

6. **Power management & laptop-specific tweaks**

   ```shell
   sysrc powerd_enable="YES"
   sysrc powerd_flags="-a adaptive -b adaptive -i 85"
   pkg install acpi-thinkpad   # ThinkPad owners
   ```

### Quick Summary – Recommended Path in 2026

- ThinkPad or Framework → FreeBSD 15 memstick + ZFS + KDE Plasma
- Modern Intel Wi-Fi laptop → hope for good iwlwifi support in 15.0
- No good Wi-Fi support → plan to use USB-C Ethernet / tethering for first days

Good luck!

References:

- [FreeBSD Handbook – Installing FreeBSD](https://docs.freebsd.org/en/books/handbook/bsdinstall)
- [FreeBSD download page](https://www.freebsd.org/where)
- [FreeBSD Foundation – Getting Started](https://freebsdfoundation.org/resource/getting-started-with-freebsd)
- [FreeBSD on Framework guide (community repo)](https://github.com/FrameworkComputer/freebsd-on-framework)
