---
audio: false
generated: true
image: false
lang: en
layout: post
title: GNOME Desktop Uninstalled From Your Machine
translated: false
type: note
---

Alright, I've got the full picture. Here's what happened:

**The GNOME desktop has been completely uninstalled from this machine.**

Here's the evidence:

| Package | Status | Notes |
|---------|--------|-------|
| `ubuntu-desktop` | **Not installed** | The meta-package that pulls in the whole desktop |
| `gdm3` | **`rc`** (removed, config left) | Display manager binary is gone |
| `gnome-shell` | **`rc`** (removed, config left) | The actual GNOME shell is gone |
| `gnome-session` | **Not installed** | Gone |
| `gnome-settings-daemon` | **`rc`** | Gone |

What happens at boot: systemd tries to start gdm3 via the old SysV init script (`/etc/init.d/gdm3`), which checks `test -x /usr/sbin/gdm3` — the binary doesn't exist — so it silently exits 0. That's why `systemctl status gdm3` shows `active (exited)` with no errors. It's "started" but immediately quit because there's nothing to run.

Meanwhile `/etc/X11/default-display-manager` still points to `/usr/sbin/gdm3`, and `graphical.target` is the default — but without a display manager or shell, you just land on TTY.

**To fix it, run:**

```bash
sudo apt install ubuntu-desktop
```

This will pull back gdm3, gnome-shell, and everything else. After that, a reboot should bring you to the graphical login.

**Or**, if you intentionally removed the desktop to save resources on this server (it's running Docker/Jellyfin/OpenClaw) and just want to keep it headless — that's fine too, just let me know.
