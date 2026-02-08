---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Fix No Space Left on Device
translated: false
type: note
---

Question: The system complains "no space left on device", which is the root cause of the ongoing issues (including GDM failing to start). After reaching a text console with Ctrl+Alt+F3 (or similar), logging in, and running commands like `sudo systemctl restart gdm` or `sudo systemctl status gdm -l`, the problem persists. How to fix the "no space left on device" error and recover the system?

Answer: 

The **"No space left on device"** error is now the primary blocker — even if ownership/permissions are partially fixed, GDM (and many other services) cannot start because the disk (usually the root `/` partition) is completely full. This often happens after reckless `chown` operations combined with package reinstall attempts, log spam, or temporary files.

### Step-by-step fix from text console (TTY / Ctrl+Alt+F3)

1. **Login** at the text console with your username (`lzwjava`) and password.

2. **Check which partition is full and why**
```bash
df -h
# Look at / (root) — if it shows 100% or very close, that's the issue

# See the biggest space users (run these one by one)
du -sh /* | sort -hr | head -15

# Most common culprits after broken upgrades/chown:
du -sh /var /var/log /var/cache /tmp /home /usr
```

Common offenders on broken Ubuntu systems:
- `/var/log/journal/` — huge logs from repeated failed starts
- `/var/cache/apt/archives/` — old .deb packages
- `/tmp/` — stuck temporary files
- `/var/lib/systemd/coredump/` — crash dumps

3. **Free up space — aggressive but safe cleanup**
Run these commands carefully (they are non-destructive):

```bash
# Clear old package cache (usually frees 1–5 GB)
sudo apt clean
sudo apt autoclean
sudo rm -rf /var/cache/apt/archives/*.deb 2>/dev/null

# Truncate huge logs (safe)
sudo journalctl --vacuum-time=2weeks
sudo journalctl --vacuum-size=100M
sudo truncate -s 0 /var/log/*.log /var/log/*/*.log 2>/dev/null

# Remove old kernels if many are installed (frees ~500 MB each)
sudo apt autoremove --purge

# Clear /tmp completely (only safe if you're not running important temp jobs)
sudo rm -rf /tmp/*
sudo mkdir /tmp
sudo chmod 1777 /tmp

# If /var/log/journal is huge:
sudo rm -rf /var/log/journal/*
sudo systemctl restart systemd-journald
```

4. **Check space again**
```bash
df -h
free -h   # also check RAM/swap — low RAM can cause similar symptoms
```

You need at least 500 MB–1 GB free on `/` for GDM and basic services to start reliably.

5. **Try restarting GDM again**
```bash
sudo systemctl restart gdm

# If it still fails, look at the real error now
sudo systemctl status gdm -l --no-pager | tail -30

# Or full journal since last boot
journalctl -b -u gdm --no-pager | tail -40
```

Copy any new specific errors (permission denied, cannot write file, etc.) if it still doesn't work.

6. **If space is freed but GDM still won't start**
Re-run the earlier reinstall commands (now that there's space):
```bash
sudo apt update
sudo apt install --reinstall gdm3 ubuntu-gnome-desktop gnome-session ubuntu-session
sudo dpkg-reconfigure gdm3
sudo systemctl restart gdm
```

7. **Switch to lightdm as fallback (much lighter, needs less space)**
```bash
sudo apt install lightdm
sudo dpkg-reconfigure lightdm   # choose lightdm
sudo reboot
```

If lightdm starts successfully, you get a graphical login again — then you can fix GDM later or keep lightdm.

### If you cannot free enough space from TTY
Boot back into the **Ubuntu live USB** (as you did before):
- Mount your root partition to `/mnt`
- Then run similar cleanup commands:
```bash
sudo mount /dev/nvme0n1pX /mnt   # replace with your root partition
sudo rm -rf /mnt/var/log/journal/*
sudo rm -rf /mnt/var/cache/apt/archives/*
sudo journalctl --rotate   # if journald is accessible
```
- Or just delete largest files you identify with `du`.

This is almost always recoverable once space is freed.

### Prevention note
Avoid running broad recursive commands on `/usr`, `/var`, `/etc`. Use targeted fixes only (e.g. `chown $USER:$USER ~/somefolder`).

If you share the output of `df -h` and `du -sh /* | sort -hr | head` (or the biggest folders), I can tell you exactly which directories to clean next.

References:  

- [https://askubuntu.com/questions/2663/no-space-left-on-device-but-there-is-tons-of-space-available](https://askubuntu.com/questions/2663/no-space-left-on-device-but-there-is-tons-of-space-available)  
- [https://help.ubuntu.com/community/FullDisk](https://help.ubuntu.com/community/FullDisk)  
- [https://askubuntu.com/questions/104635/how-to-clear-journalctl-logs](https://askubuntu.com/questions/104635/how-to-clear-journalctl-logs)