---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Enable Ubuntu Touchpad via Terminal
translated: false
type: note
---

Here are the most common and up-to-date ways (as of 2025–2026) to **enable** the touchpad from the terminal in Ubuntu. The method depends on whether you're using **Wayland** (default since ~Ubuntu 21.10/22.04) or **X11**, and on your GNOME version.

### Method 1: GNOME settings via terminal (recommended – works on both Wayland and X11)

This is the cleanest method for modern Ubuntu versions (22.04, 24.04, 24.10, 25.04, etc.) using GNOME.

```bash
# Enable touchpad (normal mode)
gsettings set org.gnome.desktop.peripherals.touchpad send-events enabled
```

Extra useful variants:

```bash
# Disable touchpad
gsettings set org.gnome.desktop.peripherals.touchpad send-events disabled

# Smart mode: disable when external mouse is connected
gsettings set org.gnome.desktop.peripherals.touchpad send-events disabled-on-external-mouse

# Show current setting
gsettings get org.gnome.desktop.peripherals.touchpad send-events
```

This change is **immediate** and survives reboot.

### Method 2: Using `xinput` (only works on X11 sessions – very common in older guides)

1. List all input devices:

```bash
xinput list
```

Look for something like:

- SynPS/2 Synaptics TouchPad
- ETPS/2 Elantech Touchpad
- DLL07E4:01 06CB:7E92 Touchpad
- etc.

Example output snippet:

```
⎜   ↳ DLL07E4:01 06CB:7E92 Touchpad          id=12   [slave  pointer  (2)]
```

2. Enable it (replace `12` with your real ID):

```bash
xinput enable 12
```

   or (more explicit)

```bash
xinput set-prop 12 "Device Enabled" 1
```

To disable again: `xinput disable 12` or `... "Device Enabled" 0`

**Note**: This only works in an **X11** session. If you're on Wayland (default), `xinput` won't see or control the touchpad properly.

### Quick way to check if you're on Wayland or X11

```bash
echo $XDG_SESSION_TYPE
```

- `wayland` → use Method 1 (`gsettings`)
- `x11`     → you can use either method

### If nothing above works

Very rare cases (driver bug, kernel issue, etc.):

```bash
# Reload the touchpad kernel module (most common ones)
sudo modprobe -r psmouse
sudo modprobe psmouse proto=imps   # or auto, synaptics, etc.
```

But try the first two methods first — they solve 95%+ of cases.

Let me know what Ubuntu version you're using and whether you're on Wayland/X11 if it still doesn't work!
