---
audio: false
generated: true
image: false
lang: en
layout: post
title: Quadro 2000 Freezes at Ubuntu Splash
translated: false
type: note
---

**Question:** Why does an NVIDIA Quadro 2000 GPU light up and show BIOS, but then Ubuntu freezes at the red splash screen for about 10 seconds without ever reaching the login screen?

---

**Answer:**

This is a very classic NVIDIA + Ubuntu boot conflict. The card works fine in BIOS (which uses VESA/firmware framebuffer), but Ubuntu's boot process hands off display control to the GPU driver — and that's where things break. Here's why and how to fix it:

---

### Root Cause

When Ubuntu boots, video/graphics mode settings are handled by the kernel. If there's a conflict during graphics initialization — which is especially common with NVIDIA hardware — the system locks up at the splash screen.

The Quadro 2000 (GF106GL chip) is old enough that it has a tension between:

1. **The `nouveau` open-source driver** (loaded by default) — Ubuntu uses the `nouveau` kernel driver for the Quadro 2000 by default, with modesetting. This driver can be unstable during early boot KMS (Kernel Mode Setting) handoff.

2. **Missing or broken proprietary NVIDIA driver** — The Quadro 2000 requires legacy NVIDIA driver 470.xx (the last version supporting Fermi-era cards). If it's not installed, nouveau takes over — and sometimes fails mid-boot.

The boot splash screen (Plymouth) hides the actual output, so you just see the frozen red/orange Ubuntu screen, with no clue what's failing underneath.

---

### Fix — Step by Step

**Step 1: Add `nomodeset` temporarily (to get into the system)**

Add `nomodeset` to the GRUB kernel parameters. This tells the kernel to load the video/graphics drivers *after* the display server starts, avoiding the early-boot conflict. Once logged in, you can then install the proper driver.

At the GRUB menu (hold **Shift** at boot), press **E**, find the line starting with `linux`, and add `nomodeset` at the end before `quiet splash`. Press **Ctrl+X** to boot.

**Step 2: Once inside, install the correct proprietary driver**

```bash
sudo apt update
sudo ubuntu-drivers autoinstall
# or manually:
sudo apt install nvidia-driver-470
sudo reboot
```

**Step 3: Permanently fix GRUB (if nomodeset is still needed)**

```bash
sudo nano /etc/default/grub
# Change this line:
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash nomodeset"
sudo update-grub
```

**Step 4: Check for Plymouth issues**

Plymouth (the splash screen manager) occasionally crashes and causes a visual hang even though the system is working underneath. You can remove `splash` from the GRUB line to see actual boot output — the last line before the freeze is your clue.

**Step 5: If you suspect nouveau conflict with proprietary driver**

Blacklist nouveau after installing the NVIDIA driver:
```bash
echo "blacklist nouveau" | sudo tee /etc/modprobe.d/blacklist-nouveau.conf
sudo update-initramfs -u
sudo reboot
```

---

### Summary Table

| Symptom | Likely Cause |
|---|---|
| Shows BIOS fine | VESA/firmware framebuffer — no driver involved |
| Freezes at Ubuntu red screen ~10s | KMS handoff to nouveau fails |
| Never reaches login | Display manager (GDM) can't start |
| Works with `nomodeset` | Confirms it's a driver/KMS conflict |

---

**References:**
- [How to Fix Ubuntu Stuck at Boot Screen](https://oneuptime.com/blog/post/2026-03-02-how-to-fix-ubuntu-stuck-at-boot-screen/view)
- [Ubuntu Freezing at Boot – itsfoss.com](https://itsfoss.com/fix-ubuntu-freezing/)
- [Quadro 2000 with nouveau on Linux Mint Forums](https://forums.linuxmint.com/viewtopic.php?t=412775)
- [Nouveau KMS Documentation](https://nouveau.freedesktop.org/KernelModeSetting.html)