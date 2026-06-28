---
audio: false
generated: true
image: false
lang: en
layout: post
title: Swapping Caps Lock via SSH on GNOME
translated: false
type: note
---

On Fedora 44 (GNOME/Wayland), I ran this over SSH:

```bash
export DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/$(id -u)/bus
gsettings set org.gnome.desktop.input-sources xkb-options "['ctrl:swapcaps']"
```

**How it works:**

1. **`DBUS_SESSION_BUS_ADDRESS`** — SSH sessions don't have access to the GNOME desktop bus. Setting this env var points to the running user's D-Bus socket so gsettings can talk to the GNOME session.

2. **`gsettings set org.gnome.desktop.input-sources xkb-options`** — GNOME's keyboard settings stored in dconf. The `xkb-options` key accepts a list of XKB options.

3. **`ctrl:swapcaps`** — XKB option from `xkeyboard-config` that swaps the Caps Lock and Left Ctrl keycodes at the input layer. Works on both Wayland and X11.

Persists across reboots because it's stored in GNOME's dconf database (`~/.config/dconf/user`).
