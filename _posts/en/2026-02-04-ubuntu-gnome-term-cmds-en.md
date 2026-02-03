---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Ubuntu GNOME Settings Terminal Commands
translated: false
type: note
---

In **Ubuntu with GNOME** (the default desktop environment since Ubuntu 17.10+), the graphical **Settings** app is launched from the terminal using this command:

```bash
gnome-control-center
```

This opens the main Settings window (the same as clicking the gear icon or searching for "Settings").

### Quick tips & useful variants

- **Open a specific panel** directly (very handy!):

```bash
# Wi-Fi & network
gnome-control-center network

# Bluetooth
gnome-control-center bluetooth

# Sound / audio
gnome-control-center sound

# Displays / monitors
gnome-control-center display

# Power / battery
gnome-control-center power

# Privacy / screen lock
gnome-control-center privacy

# Users / accounts
gnome-control-center user-accounts

# Date & Time
gnome-control-center datetime

# Keyboard / shortcuts
gnome-control-center keyboard

# Mouse & Touchpad
gnome-control-center mouse

# Background / wallpaper
gnome-control-center background

# Notifications
gnome-control-center notifications

# Search for a panel by keyword
gnome-control-center search
```

- To see **all available panels** (may vary slightly by Ubuntu version):

```bash
gnome-control-center --list
```

(or just press **Tab** after typing `gnome-control-center` + space to autocomplete panel names)

### If the command is not found

Very rare on a standard Ubuntu desktop install, but you can (re)install it:

```bash
sudo apt update
sudo apt install --reinstall gnome-control-center
```

### Extra notes (2025–2026 Ubuntu versions)

- Still works the same way in Ubuntu 24.04 LTS, 24.10, 25.04, 25.10, etc.
- If you're **not** using GNOME (e.g., KDE, XFCE, Cinnamon flavors of Ubuntu), the command is different:
  - KDE Plasma → `systemsettings`
  - XFCE → `xfce4-settings-manager`
  - Cinnamon → `cinnamon-settings`

Let me know your Ubuntu version / desktop environment if this doesn't work or if you want to open a very specific settings page!