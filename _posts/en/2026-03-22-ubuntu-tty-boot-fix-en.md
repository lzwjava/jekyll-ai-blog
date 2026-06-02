---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixing Ubuntu Boot to TTY Error
translated: false
type: note
---

Sure, here's how I diagnosed and fixed your "boots to TTY" problem, step by step:

## 🔍 Diagnosis

**Step 1 — Check the display manager status**

```bash
systemctl status gdm3
```

This was the first red flag: it showed `active (exited)` instead of `active (running)`. A display manager should be running continuously — "exited" means it started and immediately died.

**Step 2 — Verify no GNOME processes are actually running**

```bash
ps aux | grep -i gdm
ps aux | grep -i gnome-shell
```

Both returned nothing. No GDM binary, no GNOME Shell — the graphical stack wasn't there at all.

**Step 3 — Check the default boot target**

```bash
systemctl get-default
```

This showed `graphical.target`, meaning systemd *was* configured to boot into GUI mode. So the configuration was correct — the problem was the software was missing.

**Step 4 — Check if the packages are actually installed**

```bash
dpkg -l | grep -i gdm
```

This was the smoking gun: `rc  gdm3`. In dpkg language:
- **`r`** = the package has been **removed** (binary deleted)
- **`c`** = **config files** still exist on disk

Same for `gnome-shell` — also `rc` status.

**Step 5 — Confirm the binary is gone**

```bash
which gdm3
ls /usr/sbin/gdm3
```

No binary exists. The old SysV init script (`/etc/init.d/gdm3`) still existed though, which is why systemd reported "started" — the script ran, checked `test -x /usr/sbin/gdm3`, found nothing, and exited 0 silently.

**Step 6 — Verify the full extent**

```bash
apt list --installed | grep gnome-shell  # nothing
apt-cache policy ubuntu-desktop          # "Installed: (none)"
apt-cache policy gdm3                    # "Installed: (none)"
apt-cache policy gnome-shell             # "Installed: (none)"
```

The entire GNOME desktop stack — `ubuntu-desktop`, `gdm3`, `gnome-shell`, `gnome-session`, `gnome-settings-daemon` — had all been uninstalled at some point.

## 🔧 Fix

One command:

```bash
sudo apt install ubuntu-desktop -y
```

This is the Ubuntu meta-package that pulls in everything: GDM3 (display manager), GNOME Shell (the desktop), gnome-session, mutter (window manager), nautilus (file manager), and ~460 other packages (~266 MB + 1 GB disk space). After it finished, GDM3 came up as `active (running)` immediately.

Then `sudo reboot` to land back on the graphical login screen.

## 🧠 Key Takeaway

When `systemctl status` shows `active (exited)` for a service that should be long-running, it usually means the binary doesn't exist. The `dpkg -l` status codes (`rc`, `ii`, `iU`, etc.) are your best friend for quickly seeing what's installed vs. removed vs. half-configured.
