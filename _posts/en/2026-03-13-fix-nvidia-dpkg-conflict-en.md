---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix NVIDIA Dpkg File Conflict Quickly
translated: false
type: note
---

**Question:** How do I fix the dpkg error "trying to overwrite `/lib/firmware/nvidia/535.288.01/gsp_ga10x.bin`" caused by a conflict between `nvidia-kernel-common-535` and `nvidia-firmware-535-535.288.01` packages on Ubuntu?

**Answer:**

## Root Cause

This is a known conflict: when the `nvidia-kernel-common-535` and `nvidia-firmware-535-535.288.01` packages happen to be at an identical upstream version, they both ship identical firmware files at the same path on disk. When a user attempts to install both, this results in a dpkg file conflict.

The two packages from different sources (Ubuntu repo vs. NVIDIA's own repo) both try to own the same file: `/lib/firmware/nvidia/535.288.01/gsp_ga10x.bin`.

---

## Fix Options (in order of preference)

### Option 1: Remove the conflicting `nvidia-firmware` package first (Recommended)

The cleanest approach is to remove the standalone firmware package that conflicts, then let `nvidia-kernel-common-535` own those firmware files:

```bash
sudo apt remove nvidia-firmware-535-535.288.01
sudo apt --fix-broken install
sudo apt upgrade
```

### Option 2: Force overwrite with `dpkg --force-overwrite`

This tells dpkg to proceed and overwrite the conflicting file. Note that the `--force-overwrite` command is only recommended for experienced Linux users and may further break your system if done incorrectly.

```bash
# Force-overwrite the two conflicting packages
sudo dpkg -i --force-overwrite /tmp/apt-dpkg-install-wlv4CV/07-nvidia-kernel-common-535_535.288.01-0ubuntu1_amd64.deb
sudo dpkg -i --force-overwrite /tmp/apt-dpkg-install-wlv4CV/01-libnvidia-extra-535_535.288.01-0ubuntu1_amd64.deb

# Then fix broken dependencies
sudo apt --fix-broken install
```

Or using the apt cache path if the files are there:
```bash
sudo dpkg -i --force-overwrite /var/cache/apt/archives/nvidia-kernel-common-535_535.288.01-0ubuntu1_amd64.deb
sudo apt --fix-broken install
```

### Option 3: Full clean reinstall of NVIDIA drivers

If the above don't work, do a full purge and reinstall:

```bash
# Remove all NVIDIA packages
sudo apt purge nvidia-* libnvidia-* cuda-drivers* --autoremove
sudo apt autoremove
sudo apt autoclean

# Update and reinstall
sudo apt update
sudo apt install nvidia-driver-535
```

---

## After Any Fix

Always run these cleanup commands at the end:

```bash
sudo apt --fix-broken install
sudo apt upgrade
sudo reboot
```

After reboot, verify the driver is loaded:
```bash
nvidia-smi
```

---

## Why This Happens

You likely have packages from **two different sources** installed simultaneously:
- Ubuntu's official repo packages: `...-0ubuntu1`
- NVIDIA's own repo packages: `...-0ubuntu0.22.04.1`

The version suffix difference (`0ubuntu1` vs `0ubuntu0.22.04.1`) indicates different package origins. The safest long-term fix is to **pin to one source only** — either Ubuntu's `ubuntu` repo or NVIDIA's official repo, but not both mixed together.

References:

- [Ubuntu Bug #2025565 - nvidia-firmware conflict](https://bugs.launchpad.net/bugs/2025565)
- [Ubuntu Bug #2026622 - nvidia-firmware-535-server conflict](https://bugs.launchpad.net/ubuntu/+source/nvidia-graphics-drivers-535-server/+bug/2026622)
- [NVML Driver/Library Version Mismatch Fix Guide](https://hychiang.info/blog/2024/nvml_mismatch/)