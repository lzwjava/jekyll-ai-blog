---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fedora Linux Installation Guide 2026
translated: false
type: note
---

**Question:** How to install Fedora Linux?

**Answer:**

Here is a clear, step-by-step guide to install **Fedora Linux** (as of 2026, the process is still very similar to recent versions — Fedora 41 / 42 era).

### Two Main Ways to Install Fedora

1. **Workstation** (recommended for most desktop/laptop users — GNOME desktop)
2. **Spins** / **Kinoite** / **Silverblue** / **Server** / etc. (choose if you want KDE, XFCE, immutable system, server, etc.)

### Recommended Method in 2025/2026: Fedora Workstation (GNOME)

#### Step 1 – Download Fedora

- Go to the official website:  
  https://getfedora.org/

- Choose **Fedora Workstation** (most popular choice)

- Download the ISO file (~2.0–2.5 GB)

#### Step 2 – Create bootable USB

Use one of these tools (all free):

| Your current OS     | Recommended tool                  | Notes                                 |
|---------------------|------------------------------------|---------------------------------------|
| Windows             | Rufus (best) or Fedora Media Writer | Use “DD mode” in Rufus if needed     |
| macOS               | Fedora Media Writer or balenaEtcher | Fedora Media Writer is official      |
| Linux               | Fedora Media Writer, `dd`, Ventoy, balenaEtcher | `dd` command is very reliable        |

**Quick dd command example (Linux):**

```bash
sudo dd if=Fedora-Workstation-Live-x86_64-42-1.2.iso of=/dev/sdX bs=4M status=progress oflag=sync
```

Replace `/dev/sdX` with your USB device (use `lsblk` to check — **be careful!**)

#### Step 3 – Boot from USB

- Insert USB
- Restart computer
- Enter **boot menu** (usually F12, F11, Esc, F2, Del — depends on manufacturer)
  - Common keys:
    - Dell      → F12
    - Lenovo   → F12 or Fn+F12
    - HP       → F9 or Esc → F9
    - ASUS     → F8 or Esc
- Select the USB drive

If it doesn't appear → enter BIOS/UEFI (usually Del, F2, F10) and:
- Disable **Secure Boot** (recommended for first install)
- Set USB as first boot device or enable “UEFI USB boot”

#### Step 4 – Start Fedora Live system

- Choose **Try Fedora** (recommended) or **Install to Hard Drive**

- Test everything works (Wi-Fi, sound, touchpad, screen brightness)

#### Step 5 – Launch the installer (Anaconda)

Click the **“Install to Hard Drive”** icon on the desktop.

The graphical installer has these main steps:

1. **Language** → choose your language
2. **Keyboard** → add layouts if needed
3. **Time & Date** → usually auto-detected
4. **Installation Destination**
   - Select your disk
   - Two easy choices:
     - **Automatic** partitioning (recommended for beginners)
     - **Custom** (if you want separate /home, encryption, etc.)
5. **Network & Hostname** (optional)
6. **Root Password** & **User Creation**
   - Create at least one user (you can make it administrator)
   - Set root password (or enable root login — not recommended)
7. Begin Installation → wait 3–15 minutes

#### Step 6 – Finish & Reboot

- Remove USB when asked
- Click **Reboot**

First boot:
- GNOME welcome / tour appears
- Connect to Wi-Fi if needed
- Log in with the user you created

### Quick Tips & Common Choices (2026)

| Question                        | Recommended for most people          | Alternative                     |
|---------------------------------|--------------------------------------|---------------------------------|
| Desktop environment             | GNOME (Workstation)                  | KDE (Fedora KDE Spin)           |
| Immutable / atomic system       | Fedora Silverblue or Kinoite         | Traditional (Workstation)       |
| Full disk encryption            | Yes (LUKS)                           | No (faster, but less secure)    |
| Partitioning                    | Automatic                            | Custom (if dual-boot)           |
| Secure Boot                     | Disabled during install              | Can re-enable later             |
| Third-party codecs/drivers      | Install after first boot via command | —                               |

**Post-install useful commands:**

```bash
# Update system
sudo dnf update --refresh

# Install common useful packages (multimedia, etc.)
sudo dnf install ffmpeg gstreamer1-plugins-{bad-\*,good-\*,ugly-\*,base} gstreamer1-plugin-openh264

# Enable RPM Fusion (for more software)
sudo dnf install https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm
sudo dnf install https://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm
```

Enjoy Fedora!  
It is one of the most modern, up-to-date, and clean Linux distributions available.

**References:**

- [https://getfedora.org/](https://getfedora.org/)
- [https://docs.fedoraproject.org/en-US/fedora/latest/install-guide/](https://docs.fedoraproject.org/en-US/fedora/latest/install-guide/)