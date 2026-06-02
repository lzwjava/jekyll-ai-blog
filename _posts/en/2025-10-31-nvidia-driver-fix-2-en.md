---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Fixing NVIDIA Driver Package Conflict
translated: false
type: note
---

This looks like a classic package conflict during an NVIDIA driver update on Ubuntu (likely 22.04 based on the package versions). The `nvidia-kernel-common-535` package is trying to overwrite a firmware file (`gsp_ga10x.bin`) that's already owned by `nvidia-firmware-535`, causing dpkg to bail out. This is a known issue with NVIDIA 535-series drivers from Ubuntu repos.

Don't panic—your system should still boot (though graphics might be in software rendering mode if the driver is partially broken). Here's a step-by-step fix to resolve it safely. Run these in a terminal (use TTY if GUI is unstable: Ctrl+Alt+F3 to switch).

### Quick Fix Attempt (Safest First)

1. Try auto-fixing the broken packages:

   ```
   sudo apt --fix-broken install
   ```

   This often resolves dependency/unpack issues without manual intervention.

2. If that fails (or partially succeeds but leaves errors), clean up the interrupted install:

   ```
   sudo dpkg --configure -a
   sudo apt update
   sudo apt upgrade
   ```

### If Still Stuck: Force Overwrite the Conflicting File

The error is specifically on the `nvidia-kernel-common-535` deb file. Force dpkg to overwrite the duplicate file:

```
sudo dpkg -i --force-overwrite /var/cache/apt/archives/nvidia-kernel-common-535_535.274.02-0ubuntu1_amd64.deb
```

- This installs just that package, ignoring the file conflict.
- Then run:

  ```
  sudo apt --fix-broken install
  sudo apt autoremove
  sudo apt upgrade
  ```

- Reboot after: `sudo reboot`.

### Nuclear Option: Purge and Reinstall NVIDIA Packages

If the above doesn't work (e.g., deeper version mismatch), remove the conflicting NVIDIA bits and reinstall:

1. Purge the problem packages (adapt versions if needed—check with `dpkg -l | grep nvidia`):

   ```
   sudo dpkg --force-all -P nvidia-firmware-535-535.274.02 nvidia-kernel-common-535
   ```

2. Clean up:

   ```
   sudo apt autoremove --purge
   sudo apt autoclean
   ```

3. Reinstall the driver:

   ```
   sudo apt update
   sudo apt install nvidia-driver-535
   ```

4. Reboot.

### Prevention/Tips

- Add the graphics-drivers PPA for more stable NVIDIA updates: `sudo add-apt-repository ppa:graphics-drivers/ppa && sudo apt update`.
- If you're on a laptop, ensure Secure Boot is disabled in BIOS before driver installs.
- Test after reboot with `nvidia-smi` (should show your GPU) or `prime-select query` (if NVIDIA Optimus).
- If this breaks your display entirely, boot to recovery mode and run the fixes from there.

If none of this works or you get a new error, paste the full output here for more tweaks.

### References

- [Unmet dependencies nvidia-dkms-535 - package conflict breaks Ubuntu 22.04 install](https://forums.developer.nvidia.com/t/unmet-dependencies-nvidia-dkms-535-package-conflict-breaks-ubuntu-22-04-install/265788)
- [Ubuntu and NVIDIA-provided packages conflict, breaking installation](https://forums.developer.nvidia.com/t/ubuntu-and-nvidia-provided-packages-conflict-breaking-installation/259150)
- [Problem with nvidia package dependencies](https://askubuntu.com/questions/1491916/problem-with-nvidia-package-dependencies)
- [nvidia-kernel-common-535 conflicts with nvidia-firmware-535](https://superuser.com/questions/1833427/nvidia-kernel-common-535-conflicts-with-nvidia-firmware-535-535-161-07-535-161-0)
