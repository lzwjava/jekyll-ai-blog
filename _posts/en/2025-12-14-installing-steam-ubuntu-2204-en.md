---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Installing Steam on Ubuntu 22.04
translated: false
type: note
---

Question: How to install Steam on Ubuntu 22.04?

Answer: 

There are several ways to install Steam on Ubuntu 22.04 LTS. The most recommended methods are using the official `.deb` package from Valve (for the latest version) or via the Snap package (easy and contained). The APT method from Ubuntu's multiverse repository works but may provide an older installer.

### Method 1: Official Debian Package (Recommended for Latest Version)
This installs the full Steam client directly from Valve.

1. Open a terminal.
2. Download the latest `.deb` package:
   ```
   wget https://steamcdn-a.akamaihd.net/client/installer/steam.deb
   ```
3. Install it:
   ```
   sudo dpkg -i steam.deb
   ```
4. Fix any dependency issues (common):
   ```
   sudo apt update
   sudo apt install -f
   ```
5. Launch Steam:
   ```
   steam
   ```
   Or search for "Steam" in the applications menu.

Steam will update itself on first launch.

### Method 2: Via Snap (Easiest, Pre-installed on Ubuntu)
Ubuntu promotes the Snap version for gaming.

1. Open a terminal.
2. Install Steam:
   ```
   sudo snap install steam
   ```
3. Launch it:
   ```
   steam
   ```

### Method 3: Via APT (From Ubuntu Repositories)
This installs an older Steam launcher from the multiverse repo.

1. Enable multiverse (if not already):
   ```
   sudo add-apt-repository multiverse
   sudo apt update
   ```
2. Install:
   ```
   sudo apt install steam
   ```
3. Launch:
   ```
   steam
   ```

**Notes:**
- For best performance, ensure your graphics drivers are up to date (e.g., NVIDIA proprietary drivers if applicable).
- On first run, Steam downloads additional runtime files.
- If issues arise with dependencies, run `sudo apt install -f`.

References:  

- [Official Steam Download Page](https://store.steampowered.com/about/) (source of steam.deb)
- [Ubuntu Packages: steam](https://packages.ubuntu.com/jammy/steam)
- [Ubuntu Blog: Steam Snap](https://ubuntu.com/blog/level-up-linux-gaming-new-steam-snap)
- [LinuxConfig: Install Steam on Ubuntu 22.04](https://linuxconfig.org/how-to-install-steam-on-ubuntu-22-04-jammy-jellyfish-linux)
- [LinuxHint: Install Steam on Ubuntu 22.04](https://linuxhint.com/install-steam-on-ubuntu-22-04/)