---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fcitx5 Input Method Fix Applied
translated: false
type: note
---

Done ✅ fcitx input method is enabled.

## Root Cause

Your system (GNOME on Wayland) has **im-config's Wayland hook disabled by Ubuntu** (`/etc/profile.d/im-config_wayland.sh` is entirely commented out), so at login:
- Nothing started fcitx5
- Environment variables stayed at the ibus defaults (`XMODIFIERS=@im=ibus`)

That's why it disappeared after restarting.

## Fixes Applied

| Item | File | Purpose |
|------|------|---------|
| Autostart | `~/.config/autostart/org.fcitx.Fcitx5.desktop` | Runs `fcitx5 -d` at login |
| Environment | `~/.config/environment.d/input-method.conf` | Sets `GTK_IM_MODULE` / `QT_IM_MODULE` / `XMODIFIERS=@im=fcitx` (read by systemd at login) |
| IM selection | `~/.xinputrc` | `im-config -n fcitx5` wrote `run_im fcitx5` |
| Currently running | PID 9854 | Shuangpin config loaded, pinyin + cloud-pinyin addons active |

## What You Need to Do

**Log out and log back in** (or reboot) so the environment variables and autostart take effect. After login:
- fcitx5 starts automatically, tray icon: 🀄
- **Ctrl + Space** toggles Chinese/English
- Input method status bar appears at top-right

## Verification

```bash
pgrep -a fcitx5          # should show the fcitx5 process
echo $XMODIFIERS         # should be @im=fcitx (after login)
```

If it still doesn't work after logging back in, let me know and we'll check the GNOME input source (`gsettings`) config.