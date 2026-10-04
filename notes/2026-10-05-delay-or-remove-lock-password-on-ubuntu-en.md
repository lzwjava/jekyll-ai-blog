---
audio: false
generated: true
image: false
lang: en
layout: post
title: Delay or Remove Lock Password on Ubuntu
translated: false
type: note
---

Question: In Ubuntu, how can I delay the password prompt that appears after the screen locks from idling, or turn off the password requirement entirely?

Answer:

**Option 1: Settings app (GNOME desktop)**
1. Open **Settings → Privacy & Security → Screen Lock**. On older versions it's under **Privacy → Screen Lock**.
2. To **delay** the password prompt: keep Screen Lock enabled and set the Automatic Screen Lock Delay to the timing you want. That's useful if you'd rather postpone the lock than remove it.
3. To **disable** it: switch Automatic Screen Lock off.
4. Also check **Blank Screen Delay** (Settings → Power). Blanking the screen is separate from locking, so set it to a long time or "Never" if you don't want the display to turn off.

**Option 2: Terminal (gsettings)**

```bash
# Stop locking after idle
gsettings set org.gnome.desktop.screensaver lock-enabled false

# OR keep locking but delay it (seconds after the screen blanks)
gsettings set org.gnome.desktop.screensaver lock-delay 7200   # 2 hours

# Idle time before the screen blanks (0 = never)
gsettings set org.gnome.desktop.session idle-delay 0
```

Note that lock-delay counts from when the screen blanks. For a lock after about N hours of idle, set idle-delay to a long value (e.g. `10800` for 3 hours) and keep lock-delay at `0`.

**Don't ask for a password after waking from suspend**

```bash
gsettings set org.gnome.desktop.screensaver ubuntu-lock-on-suspend false
```

This is a separate preference from the idle lock, so you may need to change it too if the password appears after sleep.

**Other things to know**
- A password asked after a reboot or logout comes from the login screen, not the lock screen. To remove that, use **Settings → System → Users → Automatic Login**.
- Setting `org.gnome.desktop.lockdown disable-lock-screen` to true disables the lock function entirely, including the Super+L shortcut. This is more drastic than you probably need.
- These steps apply to GNOME, Ubuntu's default desktop. KDE, Xfce and other flavors use different settings.
- Without a lock screen, anyone with physical access can use your session, so consider a longer delay rather than turning it off completely.

References:
- [How to Turn Off the Lock Screen on Ubuntu](https://macmyths.com/how-to-turn-off-the-lock-screen-on-ubuntu/)
- [How to disable the screen lock in Ubuntu](https://linuxhint.com/disable-screen-lock-ubuntu/)
- [Disable Lock Screen on Ubuntu 22.04](https://linuxconfig.org/?p=14528)