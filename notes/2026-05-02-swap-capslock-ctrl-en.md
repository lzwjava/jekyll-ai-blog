---
audio: false
generated: true
image: false
lang: en
layout: post
title: Swapping CapsLock and Ctrl on Mint
translated: false
type: note
---

## Review: CapsLock ↔ Ctrl Swap on Linux Mint

### What We Did

**`~/.Xmodmap`** — tells X11 how to remap the keys:
1. Remove CapsLock from the "Lock" modifier group
2. Remove Ctrl_L from the "Control" modifier group
3. Reassign the physical CapsLock key → `Control_L` keycode
4. Reassign the physical Ctrl_L key → `Caps_Lock` keycode
5. Re-add both to their respective modifier groups

This is a clean full swap — both keys work as the other in every app.

**`~/.config/autostart/xmodmap.desktop`** — a Cinnamon autostart entry that runs `xmodmap ~/.Xmodmap` every time the desktop session starts. No root needed; Cinnamon processes `~/.config/autostart/` automatically on login.

**`DISPLAY=:0 xmodmap ~/.Xmodmap`** — applied it live to the running X session without needing a logout.

---

### What's Good

- No root/sudo required — fully user-space
- Works immediately without restart
- Persists across reboots via the autostart mechanism
- The Xmodmap approach is the most reliable way on X11 across all desktop environments (Cinnamon, XFCE, MATE, etc.)

### What's Slightly Fragile

- **Wayland**: `xmodmap` doesn't work under Wayland. Linux Mint Cinnamon currently uses X11 by default, so this is fine — but worth knowing.
- **Alternative**: The cleaner system-wide approach is `XKBOPTIONS="ctrl:swapcaps"` in `/etc/default/keyboard`, but that needs sudo. What we did is the best no-root option.
