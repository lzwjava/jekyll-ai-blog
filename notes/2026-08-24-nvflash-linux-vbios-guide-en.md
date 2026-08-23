---
audio: false
generated: true
image: false
lang: en
layout: post
title: NVFlash Linux VBIOS Guide
translated: false
type: note
---

**Question:** How do I install and use NVFlash on Linux to back up and flash an RTX GPU VBIOS?

**Answer:**

---

## ⚠️ WARNING

Must run as **root**. The NVIDIA kernel module **must be fully unloaded** before NVFlash can access the GPU. Flashing the wrong VBIOS can permanently brick your card — always back up first.

---

## Step 1 — Download NVFlash

Go to **TechPowerUp** and download the latest version (v5.867):
```
https://www.techpowerup.com/download/nvidia-nvflash/
```

Extract the zip — it includes both a Linux binary and the Windows `.exe`.

```bash
unzip nvflash_5.867.zip -d ~/nvflash
cd ~/nvflash
```

---

## Step 2 — Make the Binary Executable

After extraction, the Linux binary requires `chmod +x` before it can run.

```bash
chmod +x nvflash
```

---

## Step 3 — Stop X11 / Wayland (Desktop GUI)

NVFlash is best run from a text console (TTY) with X11/Wayland stopped. Switch to multi-user (non-graphical) mode before flashing:

```bash
sudo systemctl isolate multi-user.target
```

Or if you're on a desktop, just switch to a TTY with `Ctrl+Alt+F2`, log in as root there, and proceed.

---

## Step 4 — Unload NVIDIA Kernel Modules

Unload all NVIDIA processes in this order — the nvidia module must be fully unloaded for nvflash to function:

```bash
sudo rmmod nvidia_drm nvidia_modeset nvidia_uvm nvidia
```

Verify they're all gone:
```bash
lsmod | grep nvidia
# should return nothing
```

> **Tip:** If modules refuse to unload, stop your display manager first:
> ```bash
> sudo systemctl stop gdm   # or sddm / lightdm
> ```

---

## Step 5 — Verify NVFlash Detects Your GPU

```bash
sudo ./nvflash --list
```

This confirms nvflash is working and detects your GPU. Note the index number (e.g., `0`) shown — you'll need it for multi-GPU systems.

---

## Step 6 — Back Up Current VBIOS (Mandatory!)


```bash
sudo ./nvflash --save vbios_backup.rom
```


For a specific GPU index:
```bash
sudo ./nvflash -i0 --save vbios_backup_gpu0.rom
```

Store the backup on a **USB drive or second machine** — not just the local disk.

---

## Step 7 — Disable Write Protection


```bash
sudo ./nvflash --protectoff
```


---

## Step 8 — Flash the New VBIOS

Standard flash:
```bash
sudo ./nvflash vbios_new.rom
```

If there is a subsystem ID mismatch, use `-6` to override (use with caution):
```bash
sudo ./nvflash -6 vbios_new.rom
```


Press `Y` to confirm when prompted.

---

## Step 9 — Verify the New VBIOS

After flashing, confirm the new VBIOS is active:
```bash
sudo ./nvflash --version
```


Then reboot:
```bash
sudo reboot
```

After boot, reload your desktop and check with `nvidia-smi` or GPU-Z (if on Windows dual-boot) to confirm the BIOS version string changed.

---

## Troubleshooting — Modules Won't Unload

Some distributions have security modules like AppArmor or SELinux that may block nvflash's direct device access. If encountering unexplained permission errors, boot with the security module in permissive mode.

Also try killing any lingering processes:
```bash
sudo fuser -k /dev/nvidia*
sudo rmmod nvidia_uvm nvidia_drm nvidia_modeset nvidia
```

---

## Full Linux Workflow Summary

```bash
# 1. Extract & make executable
chmod +x nvflash

# 2. Stop GUI
sudo systemctl isolate multi-user.target

# 3. Unload NVIDIA modules
sudo rmmod nvidia_drm nvidia_modeset nvidia_uvm nvidia

# 4. List GPUs
sudo ./nvflash --list

# 5. Backup
sudo ./nvflash --save vbios_backup.rom

# 6. Disable protection
sudo ./nvflash --protectoff

# 7. Flash
sudo ./nvflash -6 vbios_new.rom

# 8. Verify
sudo ./nvflash --version

# 9. Reboot
sudo reboot
```

---

**References:**
- [cyclone-github: nvflash how-to Linux (Debian tested, updated 2025)](https://github.com/cyclone-github/nvidia_vbios/blob/main/nvflash_how_to_linux.txt)
- [nvflash Reference 2026 — Linux differences](https://www.mvktech.net/nvflash-guide/)
- [HiveOS VBIOS Flashing Guide (Linux, multi-GPU)](https://hiveon.com/forum/t/guide-nvidia-gpu-vbios-flashing-with-hiveos/4091.rss)
- [TechPowerUp NVFlash Download](https://www.techpowerup.com/download/nvidia-nvflash/)