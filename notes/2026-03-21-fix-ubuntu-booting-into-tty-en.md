---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix Ubuntu Booting Into TTY
translated: false
type: note
---

Question: Why does Ubuntu boot into a TTY (terminal) instead of the normal graphical window, and how can I switch back to the GUI?

Answer:

When Ubuntu boots into a TTY (text-only terminal like `tty1`) instead of the graphical desktop, it usually means the graphical system failed to start. This is typically related to the display manager, desktop environment, or graphics drivers.

---

## 🚀 Quick Temporary Fix (Try First)

Press:

```
Ctrl + Alt + F2   (or F1–F7)
```

* One of these may bring you back to the graphical login screen.
* If you see GUI → just log in normally.

---

## 🔧 Step 1: Try Starting GUI Manually

Login in the TTY, then run:

```bash
startx
```

If it works → problem is likely the display manager not starting automatically.

---

## 🔧 Step 2: Restart Display Manager

Ubuntu uses a display manager like:

* `gdm3` (default for GNOME)
* `lightdm` (older systems)

Try:

```bash
sudo systemctl restart gdm3
```

Or:

```bash
sudo systemctl restart lightdm
```

If GUI appears → issue is temporary.

---

## 🔧 Step 3: Enable GUI at Boot

Check default target:

```bash
systemctl get-default
```

If it shows:

```
multi-user.target
```

👉 That means CLI-only mode.

Fix it:

```bash
sudo systemctl set-default graphical.target
sudo reboot
```

---

## 🔧 Step 4: Reinstall Desktop Environment

Sometimes GNOME is broken:

```bash
sudo apt update
sudo apt install ubuntu-desktop
```

For minimal reinstall:

```bash
sudo apt install --reinstall gdm3
```

---

## 🔧 Step 5: Check Disk Space (Very Common!)

```bash
df -h
```

If root (`/`) is full → GUI won't start.

Clean up:

```bash
sudo apt clean
sudo apt autoremove
```

---

## 🔧 Step 6: Check GPU / Driver Issues

If you recently installed NVIDIA drivers, it might break GUI.

Try:

```bash
sudo ubuntu-drivers autoinstall
```

Or remove problematic drivers:

```bash
sudo apt purge nvidia*
```

---

## 🔧 Step 7: Check Logs (Advanced)

```bash
journalctl -xe
```

or:

```bash
cat /var/log/Xorg.0.log | grep EE
```

Look for errors related to:

* display
* GPU
* gdm

---

## 🧠 Common Causes Summary

| Cause                 | Explanation                   |
| --------------------- | ----------------------------- |
| GUI disabled          | system boot target set to CLI |
| Display manager crash | gdm3/lightdm not starting     |
| Full disk             | no space → GUI fails          |
| Broken update         | packages partially installed  |
| GPU driver issue      | especially NVIDIA             |

---

## ✅ Fastest Fix Path (Recommended Order)

1. `Ctrl + Alt + F2~F7`
2. `sudo systemctl restart gdm3`
3. `systemctl get-default` → set to graphical
4. Check disk: `df -h`
5. Reinstall: `sudo apt install ubuntu-desktop`

---

If you want, paste what you see in the TTY (errors, login messages), and I can pinpoint the exact root cause quickly.
