---
audio: false
generated: true
image: false
lang: en
layout: post
title: MODS Supported Operating Systems
translated: false
type: note
---

Here's the complete picture of what environment MODS runs in:

## MODS Supported Operating Systems

According to the document (section 1.0):

| OS | Status |
|---|---|
| **Linux** (kernel ≥ 2.6.18) | ✅ Primary platform |
| **Microsoft Windows 7** | ✅ Supported |
| **Mac OS X** (x86 only, not PowerPC) | ✅ Supported |
| **DOS** | ❌ Discontinued since R290 |

## For Linux — Two Approaches

### Option 1: NVIDIA's Turnkey Tiny Linux Image (Recommended)

NVIDIA distributes a **custom Linux disk image** (fits on a **64 MB USB drive**). This is the intended production method:
- Boots from USB stick into a minimal Linux environment
- Automatically runs MODS on startup
- No need to compile kernel modules or configure drivers
- Uses a **squashfs compressed filesystem** with everything pre-packaged
- Configured via `/mods/args` and `/syslinux/commands` files

This is the **"tinylinux"** approach you mentioned — it's what NVIDIA provides as the official way to run MODS in manufacturing.

### Option 2: Run on an Existing Linux Distro (e.g., Ubuntu)

Yes, **Ubuntu works**, but with important caveats:

**Requirements:**
- 64-bit (x86_64) Intel or AMD CPU
- **4 GB+ system memory**
- Kernel ≥ **2.6.18** (2.6.29+ recommended)
- **glibc 2.5+**
- Kernel sources + development tools (`make`, `gcc`) to compile the kernel module

**Critical prerequisites before running:**
1. **NVIDIA GPU must be in its original VBIOS-initialized state**
2. **X server MUST NOT be running** — you need to kill it first
3. **nvidia kernel module MUST be unloaded** — same for the `nouveau` driver (blacklist it)
4. **Framebuffer console should be disabled** (set `vga=normal` in kernel args)

**Steps on Ubuntu/Debian:**
```bash
# Stop X server
sudo service gdm stop   # or lightdm/kdm depending on your DM

# Unload nvidia driver
sudo rmmod nvidia

# Blacklist nouveau (if present)
echo "blacklist nouveau" | sudo tee /etc/modprobe.d/blacklist-nouveau.conf

# Install MODS kernel module
sudo ./install_module.sh --install

# Run MODS
sudo ./mods gputest.js -mfg
```

**⚠️ Warning from the document:**
> *"If you run MODS on a GPU that has been initialized by the nvidia driver, the system may become unstable"*

## Bottom Line

- **For production/testing**: Use NVIDIA's **custom Linux disk image** (tinylinux) — it's a clean, minimal boot environment with no driver conflicts.
- **For development/debug**: Ubuntu works fine, but you must ensure **no display driver touches the GPU first** — this means no X, no nvidia.ko, no nouveau. MODS contains its own embedded OpenGL/CUDA drivers and resource manager, so it doesn't need the NVIDIA display driver.

The environment is basically a **"bare metal" Linux setup** where MODS has exclusive access to the GPU hardware.
