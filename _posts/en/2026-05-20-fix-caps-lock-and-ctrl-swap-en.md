---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix Caps Lock and Ctrl Swap
translated: false
type: note
---

Problem

    Caps Lock and Left Control were both mapped to Ctrl (key 37 = Control_L, key 66 = Control_L). Your existing ~/.Xmodmap used a keysym-based swap (keysym Caps_Lock = Control_L), which got confused by multiple keys sharing the same keysym and didn't actually swap anything — it effectively did nothing.

    Fix Applied — three methods, all agreeing

    1. Immediate: setxkbmap -option ctrl:swapcaps

    This is the modern, X-server-native way. It tells the X keyboard extension (XKB) to swap the two keys at the hardware-mapping level. It's clean, composable, and won't collide with other keyboard options.

    Keycodes after the fix:

    | Keycode | Physical Key | Keysym             | Acts as          |
    |---------|--------------|--------------------|------------------|
    | 37      | Left Ctrl    | Caps_Lock (0xffe5) | Caps Lock toggle |
    | 66      | Caps Lock    | Control_L (0xffe3) | Ctrl (modifier)  |
    | 105     | Right Ctrl   | Control_R (0xffe4) | Ctrl (unchanged) |

    The clear Lock / clear Control / add Lock / add Control steps ensure the modifier maps are consistent — a common pitfall where xmodmap changes the keysym but the modifier mask doesn't follow.

    2. Persistence via ~/.Xmodmap (rewritten)

    Old file used keysym commands — unreliable when multiple keys share a keysym. Rewritten to keycode-based commands:


    keycode 66 = Control_L
    keycode 37 = Caps_Lock
    clear Lock
    clear Control
    add Lock = Caps_Lock
    add Control = Control_L


    Loaded at login by ~/.config/autostart/xmodmap.desktop (XDG Autostart spec — supported by GNOME, KDE, XFCE, i3, Sway, etc.)

    3. Fallback via ~/.xprofile

    Created ~/.xprofile with setxkbmap -option ctrl:swapcaps. This runs on X11 login via the display manager, before the desktop environment's autostart. Not all DEs read .xprofile (LightDM does, GDM sometimes does), so this is best-effort redundancy.

    Persistence chain


    X11 login (DM)
      → ~/.xprofile (setxkbmap)           ← catches early DE init
      → DE starts
      → ~/.config/autostart/*.desktop      ← catches XDG-compliant DEs
        → xmodmap ~/.Xmodmap               ← final override, keycode-based


    If the DE's own keyboard settings panel overrides XKB options (GNOME Settings does this sometimes), you may need to lock the option there too — but setxkbmap -option ctrl:swapcaps is usually sticky once set.

    To undo

    If you ever want to revert:

    sh
    setxkbmap -option            # clears all custom options → back to defaults
    or for just ctrl swap:
    setxkbmap -option ctrl:nocaps    # Caps Lock does nothing
    setxkbmap -option                   # vanilla


    Then delete or comment out ~/.xprofile and ~/.Xmodmap to prevent it coming back on reboot.
