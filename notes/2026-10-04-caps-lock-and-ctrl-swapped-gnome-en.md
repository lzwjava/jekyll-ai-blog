---
audio: false
generated: true
image: false
lang: en
layout: post
title: Caps Lock and Ctrl swapped GNOME
translated: false
type: note
---

Done ✅ — **Caps Lock ↔ Ctrl swapped** on `192.168.1.45`.

**What I did:**
- Detected the desktop: GNOME 46 on **Wayland** (not X11), so `setxkbmap`/`xmodmap` session hacks wouldn't persist properly — used the supported GNOME approach instead:
- Set the XKB option `ctrl:swapcaps` via dconf (through the active GNOME session bus at `/run/user/1000/bus`):
  - Key: `/org/gnome/desktop/input-sources/xkb-options` → `['ctrl:swapcaps']` ✓ (verified)
  - Session 3 (the live GNOME session on tty2) is **Active**, so it applied immediately

**Effect:** On that machine's physical keyboard, **Caps Lock now acts as Ctrl**, and the **right-hand Ctrl key acts as Caps Lock**. (`ctrl:swapcaps` is a symmetrical swap.)

This is persistent — it's stored in the user's dconf, so it survives reboots and login. No restart needed. If you ever want to revert: `gsettings reset org.gnome.desktop.input-sources xkb-options`.
