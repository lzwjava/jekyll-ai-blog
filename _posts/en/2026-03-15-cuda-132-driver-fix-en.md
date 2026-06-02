---
audio: false
generated: true
image: false
lang: en
layout: post
title: CUDA 13.2 and Driver Fix Guide
translated: false
type: note
---

✅ **Done!** Created backup at `~/.bashrc.backup` and added CUDA 13.2 to PATH and LD_LIBRARY_PATH.

---

## 📋 **Fix Summary: NVIDIA Driver & CUDA 13.2 Installation**

**Problem:** `nvidia-smi` failed with "NVIDIA-SMI has failed because it couldn't communicate with the NVIDIA driver"

**Root Cause:** Broken/mixed NVIDIA driver packages (590 series + 595 series) in half-installed state

**Solution Steps:**

1. **Cleaned up broken packages:**
   - Killed stuck dpkg/apt processes holding locks
   - Removed `/var/lib/dpkg/lock*` files
   - Purged conflicting NVIDIA packages (`nvidia-*`, `libnvidia-*`)
   - Fixed corrupted dpkg updates files

2. **Removed version conflicts:**
   - `libnvidia-cfg1` (595) vs `libnvidia-cfg1-535` conflict
   - `libnvidia-egl-gbm1` vs NVIDIA 535 driver conflict

3. **Installed correct versions:**
   - CUDA Toolkit 13.2 from NVIDIA repo
   - NVIDIA Driver 535.288.01 (Ubuntu repo) - compatible with CUDA 13.2

4. **Verified installation:**
   - `nvidia-smi` shows RTX 4070 active
   - Driver: 535.288.01
   - CUDA path: `/usr/local/cuda-13.2`
   - Compiled and ran test CUDA program successfully

**Key Commands Used:**

```bash
# Fix dpkg locks and kill stuck processes
sudo kill -9 $(ps aux | grep dpkg | grep -v grep | awk '{print $2}')
sudo rm -f /var/lib/dpkg/lock*

# Remove broken packages
sudo dpkg --remove --force-remove-reinstreq cuda-drivers libnvidia-compute libnvidia-decode libnvidia-encode libnvidia-gl nvidia-driver xserver-xorg-video-nvidia

# Install CUDA 13.2 and driver
sudo apt-get install -y cuda-13-2
sudo apt-get install -y nvidia-driver-535

# Load driver and test
sudo modprobe nvidia
nvidia-smi
```

**Current Status:** ✅ **FIXED** - CUDA 13.2 + NVIDIA Driver 535 working with RTX 4070
