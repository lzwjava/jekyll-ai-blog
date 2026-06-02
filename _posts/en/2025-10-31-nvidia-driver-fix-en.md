---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Fixing NVIDIA Driver Version Mismatch
translated: false
type: note
---

### Understanding the Error
The `nvidia-smi` command is failing because of a version mismatch between your NVIDIA kernel driver (loaded in the OS kernel) and the user-space NVML (NVIDIA Management Library) components. This often occurs after a kernel update, partial driver installation, or system upgrade without a full driver reinstall. The reported NVML version (535.274) suggests you're using a relatively recent NVIDIA driver branch (likely from the 535 series), but the kernel module isn't aligned.

Don't worry—this is fixable without losing data. Below are step-by-step troubleshooting and resolution steps, starting with the simplest.

### Quick Fixes (Try These First)
1. **Reboot Your System**
   The most common cause is a stale kernel module. Rebooting reloads everything cleanly.
   ```
   sudo reboot
   ```
   After reboot, run `nvidia-smi` again. If it works, you're done!

2. **Check Current Driver and Kernel Versions**
   Verify what's installed:
   ```
   # Check kernel driver version
   cat /proc/driver/nvidia/version

   # Check loaded kernel modules
   lsmod | grep nvidia

   # Check your current kernel version
   uname -r
   ```
   Compare the driver version here with 535.274. If they don't match (e.g., kernel shows 535.x but x ≠ 274), proceed to reinstall.

### Full Resolution: Reinstall NVIDIA Drivers
If rebooting doesn't help, reinstall the drivers to sync everything. This assumes you're on Ubuntu/Debian (common for nanoGPT setups; adjust for other distros like Fedora).

#### Option 1: Via Package Manager (Recommended for Stability)
1. **Purge Existing Drivers** (removes mismatches):
   ```
   sudo apt update
   sudo apt purge 'nvidia*'
   sudo apt autoremove
   sudo rm -rf /usr/lib/nvidia*  # Optional: Clean leftovers
   ```

2. **Reboot to Clear Modules**:
   ```
   sudo reboot
   ```

3. **Install Matching Drivers**:
   Since your NVML is 535.274, install the 535 series (or newer if available). Check NVIDIA's site for your GPU, but for 535:
   ```
   sudo apt install nvidia-driver-535 nvidia-utils-535
   ```
   (Replace with your distro's package name if needed, e.g., `dnf` on Fedora.)

4. **Reboot and Verify**:
   ```
   sudo reboot
   nvidia-smi  # Should now work
   ```

#### Option 2: Direct from NVIDIA (For Latest/Custom Versions)
1. Download the 535.274 runfile from [NVIDIA's archive](https://www.nvidia.com/Download/driverResults.aspx/227xxx/en-us/) (search for your GPU and 535.274).
   ```
   wget https://us.download.nvidia.com/XFree86/Linux-x86_64/535.274.05/NVIDIA-Linux-x86_64-535.274.05.run
   chmod +x NVIDIA-Linux-x86_64-535.274.05.run
   ```

2. **Stop Display Manager** (switch to console):
   ```
   sudo systemctl stop gdm  # Or lightdm/sddm
   sudo telinit 3  # Or Ctrl+Alt+F3 to switch TTY
   ```

3. **Install**:
   ```
   sudo ./NVIDIA-Linux-x86_64-535.274.05.run --no-questions
   ```
   Follow prompts; it may warn about mismatches—proceed.

4. **Reboot**:
   ```
   sudo reboot
   ```

### If Issues Persist
- **Secure Boot Enabled?** Disable it in BIOS/UEFI, as it blocks unsigned kernel modules.
- **Kernel Mismatch?** If you updated your kernel recently, boot into the old one via GRUB (hold Shift at boot) and reinstall drivers.
- **Logs for Clues**: Check `dmesg | grep nvidia` or `/var/log/Xorg.0.log` for errors.
- **GPU-Specific?** Run `lspci | grep -i nvidia` to confirm your GPU is detected.

After fixing, you should see output like GPU usage, memory, etc., in `nvidia-smi`. If you're training models in nanoGPT, this will unblock CUDA. If you share more details (e.g., distro, GPU model, or output from the version checks), I can refine this!
