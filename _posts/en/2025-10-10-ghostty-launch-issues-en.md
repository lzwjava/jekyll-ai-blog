---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Ghostty Installation and Launch Issues
translated: false
type: note
---

### Issue Diagnosis

Based on the logs you shared, the installation of Ghostty 1.1.3 via the `.deb` package succeeded, but launching it fails for two main reasons:

1. **CLI Argument Error**: The command `ghostty .` treats `.` as an invalid configuration field (likely intended as a directory, but Ghostty doesn't support that syntax). This causes the immediate exit with "invalid field".

2. **OpenGL/GTK Compatibility Issue**: When running `ghostty` without arguments, it initializes but crashes due to "OpenGL version is too old. Ghostty requires OpenGL 3.3" (your system reports 3.2 to Ghostty). This is a known problem on Ubuntu 22.04, especially with NVIDIA drivers under X11. Despite `glxinfo` often showing OpenGL 4.6+, Ghostty's GTK 4.6 runtime can't properly access higher versions with NVIDIA GL. The "GDK_DEBUG=vulkan-disable" warning is a workaround attempt but doesn't resolve the core issue. The final Gtk-CRITICAL error is a symptom of the failed surface realization.

This affects many users on Ubuntu 22.04 (and derivatives like Pop!_OS) due to the older GTK version (4.6 vs. the newer 4.12+ needed for full NVIDIA compatibility).

### Quick Checks
- Verify your actual OpenGL support (install `mesa-utils` if needed: `sudo apt install mesa-utils`):
  ```
  glxinfo | grep "OpenGL version"
  ```
  If it reports 3.3+, the issue is indeed GTK/NVIDIA-specific.
- Check your session type: `echo $XDG_SESSION_TYPE`. If it's `x11`, that's likely contributing.

### Solutions
Here are step-by-step fixes, starting with the simplest:

1. **Switch to Wayland (if you have hybrid graphics, e.g., Intel + NVIDIA)**:
   - Log out and select a Wayland session at login (or add `WaylandEnable=true` to `/etc/gdm3/custom.conf` and restart GDM).
   - Run Ghostty with integrated graphics: `prime-run --gpu intel ghostty` (install `nvidia-prime` if needed).
   - This bypasses NVIDIA X11 issues for some users.

2. **Install via Snap (Easier Alternative Package)**:
   - The unofficial `.deb` you used can inherit system quirks. Try the official Snap, which bundles dependencies:
     ```
     sudo snap install ghostty --classic
     ```
   - Launch with `snap run ghostty`. If OpenGL still fails, proceed to upgrades.

3. **Upgrade Ubuntu to 24.04 (Recommended for Long-Term Fix)**:
   - Ubuntu 24.04 includes GTK 4.14+, resolving NVIDIA compatibility.
   - Follow the official upgrade guide: `sudo do-release-upgrade`.
   - After upgrading, reinstall Ghostty via the same `.deb` or Snap. Users report it works flawlessly post-upgrade.

4. **Build from Source with GLFW Backend (Temporary Workaround)**:
   - This uses a non-GTK runtime to sidestep the OpenGL issue (note: lacks tabs, for testing only).
     ```
     sudo apt install git zig libgtk-4-dev libadwaita-1-dev libharfbuzz-dev libpango1.0-dev libcairo2-dev libgdk-pixbuf-2.0-dev libglib2.0-dev libwayland-dev libxkbcommon-dev libinput-dev libudev-dev libseat-dev libpipewire-0.3-dev libsystemd-dev libx11-dev libxext-dev libxfixes-dev libxi-dev libxrandr-dev libxtst-dev libxdamage-dev libxcomposite-dev libxrender-dev libxcursor-dev libxinerama-dev libxss-dev libxv-dev libxxf86vm-dev libgl1-mesa-dev libegl1-mesa-dev libgles2-mesa-dev libgbm-dev libdrm-dev libvulkan-dev libclang-dev
     git clone https://github.com/ghostty-org/ghostty.git
     cd ghostty
     zig build -Doptimize=ReleaseFast -Dapp-runtime=glfw
     sudo cp zig-out/bin/ghostty /usr/local/bin/
     ```
   - Run `ghostty`. For full features, switch back to GTK once upgraded.

### Additional Tips
- Update your NVIDIA drivers: `sudo ubuntu-drivers autoinstall` (or use 550+ series manually).
- If you're on AMD/Intel-only, ensure Mesa is updated: `sudo apt update && sudo apt upgrade mesa-vulkan-drivers`.
- For the config warning in your template file (`~/.config/ghostty/config`), edit it to remove any invalid lines (e.g., stray `.`).

If none of these work, share your `glxinfo` output or GPU details (`lspci | grep VGA`) for more tailored advice.

[OpenGL Too Old Discussion](https://github.com/ghostty-org/ghostty/discussions/3159)
[Ghostty Ubuntu Builds](https://github.com/mkasberg/ghostty-ubuntu)
[Ghostty Snap](https://snapcraft.io/ghostty)
