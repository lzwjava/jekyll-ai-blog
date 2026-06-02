---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Fix GDM Service Start Failure
translated: false
type: note
---

Question: After booting into recovery mode or chroot from the Ubuntu live USB, when trying to start the graphical interface or after reboot, the system still complains "Failed to start gdm.service" (GNOME Display Manager failed to start). How to fix this?

Answer:

The "Failed to start gdm.service" error usually means GDM cannot start because of permission problems, missing/corrupted files, or broken dependencies — all very likely after you ran `sudo chown -R $(whoami) /usr/`. Here are the most effective repair steps in order of recommendation.

### Step 1: Boot into recovery / root shell again (safest starting point)
Use one of these methods:
- GRUB → edit boot entry → add `rw init=/bin/bash` at end of linux line → Ctrl+X
- Or boot from live USB → chroot into your installed system (as described previously)

Once you have a root shell:

### Step 2: Core ownership and permission repair (run these exactly)
```bash
# Remount root read-write if needed
mount -o remount,rw /

# Fix main directories that must be root-owned
chown -R root:root /usr
chown -R root:root /etc
chown -R root:root /var
chown root:root / 2>/dev/null

# Restore standard directory permissions (very important for executables)
chmod -R 755 /usr/bin /usr/sbin /usr/lib /usr/libexec /usr/share
chmod -R 755 /bin /sbin /lib /lib64 /lib32 2>/dev/null
chmod -R u+rX,go+rX,go-w /usr/bin /usr/sbin /usr/lib /usr/libexec

# Fix common service & config locations
chmod 755 /usr/lib/systemd /usr/lib/systemd/system
chmod 644 /usr/share/gdm /etc/gdm /etc/gdm3 2>/dev/null
chown -R root:root /usr/share/gdm /etc/gdm /etc/gdm3 2>/dev/null

# Make sure /tmp has correct sticky bit
chmod 1777 /tmp
```

### Step 3: Reinstall GDM and GNOME core packages (this usually fixes it)
```bash
# Make sure networking works in chroot (if not already)
mount --bind /dev   /dev
mount --bind /proc  /proc
mount --bind /sys   /sys
mount --bind /run   /run

# Update package lists
apt update

# Reinstall GDM + desktop metapackage (this restores missing/corrupted files)
apt install --reinstall gdm3 ubuntu-gnome-desktop gnome-session gdm3 \
  gnome-shell ubuntu-session xserver-xorg-core xserver-xorg-video-all \
  --no-install-recommends

# Optional: also reinstall if you suspect deeper damage
apt install --reinstall systemd udev libpam-systemd dbus policykit-1 \
  accountsservice libpam-gnome-keyring
```

### Step 4: Clean GDM cache & logs, regenerate configs
```bash
rm -rf /var/lib/gdm3/.cache/* 2>/dev/null
rm -f /var/log/gdm3/* 2>/dev/null

# Regenerate GDM configs if needed
dpkg-reconfigure gdm3

# Make sure GDM is the default display manager
echo "/usr/sbin/gdm3" > /etc/X11/default-display-manager
```

### Step 5: Final checks & reboot
```bash
# Check for obvious errors
journalctl -u gdm --since "1 hour ago"   # if journald is working

# Sync changes to disk
sync

# Exit chroot if you are in one (type exit twice if needed)
exit
umount /mnt/dev /mnt/proc /mnt/sys /mnt/run /mnt 2>/dev/null

reboot
```

### If it still fails after reboot
- You may see a black screen or blinking cursor → press **Ctrl+Alt+F3** (or F2–F6) to get a text console → login as your user → run:
  ```bash
  sudo systemctl restart gdm
  # or
  sudo systemctl status gdm -l
  ```
  Look at the last 10–20 lines of output — copy any specific errors (like "permission denied", "cannot execute", "missing file", etc.) and share them.

- Switch to another display manager temporarily (lightdm is lighter and easier to recover with):
  ```bash
  apt install lightdm
  dpkg-reconfigure lightdm   # choose lightdm
  reboot
  ```
  If lightdm works, you can later switch back to gdm3 once everything is fixed.

### Quick alternative: reinstall desktop from live USB (faster if above is too painful)
From live USB "Try Ubuntu":
1. Mount your root partition (`/dev/nvme0n1pX` or similar) to `/mnt`
2. Run:
   ```bash
   sudo apt update
   sudo apt install --reinstall ubuntu-desktop^ gdm3
   ```
   (The `^` reinstalls the whole tasksel group)

This usually resolves 90% of chown-destroyed GNOME setups without full reinstall.

Do **not** run any more recursive chown/chmod on system directories — that was the root cause.

References:

- [https://askubuntu.com/questions/26496/how-to-recover-from-accidentally-changing-ownership-of-usr](https://askubuntu.com/questions/26496/how-to-recover-from-accidentally-changing-ownership-of-usr)
- [https://askubuntu.com/questions/1029472/gdm-failed-to-start-after-changing-permissions](https://askubuntu.com/questions/1029472/gdm-failed-to-start-after-changing-permissions)
- [https://wiki.ubuntu.com/RecoveryMode](https://wiki.ubuntu.com/RecoveryMode)
