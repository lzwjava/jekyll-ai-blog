---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Fix Full Disk and Recover Ubuntu
translated: false
type: note
---

**Question:** My disk is always full. I deleted 3 GB of files and restarted, but now the Ubuntu live USB shows up, and after selecting it, GDM fails to start again. Using Ctrl+Alt+F3 and running `df -h` shows the 468 GB disk is 100% full. How can I find the largest files, stop whatever is filling up the disk, and fix the system?

**Answer:**

Your system is in a critical state — the root filesystem is completely full (100%), which prevents normal boot, prevents login managers (GDM) from starting, and often breaks many services.

### Step 1: Get into a usable root shell right now

You already reached tty3 (Ctrl+Alt+F3) → good.

If you are **not** logged in yet:

- Username: your normal username
- Password: your user password

If login fails because filesystem is read-only or too full:

Try to force remount rw (very often needed):

```bash
mount -o remount,rw /
```

Then try login again.

If still can't log in as user → try root (if you have root password):

```bash
Login: root
Password: ...
```

If no root password or it doesn't work → boot with live USB (safest next step).

### Step 2: Quickly find what is eating the disk (from tty or live USB)

From the broken system tty (if you got shell):

```bash
# Fastest way to see biggest directories
du -shx /* 2>/dev/null | sort -hr | head -15

# Then drill down into the biggest ones, example:
du -shx /var/* 2>/dev/null | sort -hr | head -10
du -shx /var/log/* 2>/dev/null | sort -hr | head -8
du -shx /home/* 2>/dev/null | sort -hr
```

Most common huge offenders when disk fills suddenly:

- `/var/log/journal/` (systemd journal) – very common
- `/var/log/` (nginx/apache/mysql logs, syslog without rotation)
- `/var/cache/apt/archives/` (old .deb packages)
- `/tmp/` or `/var/tmp/` (some programs write huge temp files)
- `/home/youruser/.cache/` (thumbnails, browser cache, flatpak cache…)
- Docker: `/var/lib/docker/`
- Snap: `/var/lib/snapd/snaps/`
- Timeshift snapshots: `/timeshift/`

To see the absolute largest individual files (very useful):

```bash
find / -xdev -type f -size +500M -exec ls -lh {} \; 2>/dev/null | sort -hr
```

or even bigger ones:

```bash
find / -xdev -type f -size +1G -ls 2>/dev/null | sort -k7nr | head -20
```

### Step 3: Immediate emergency space recovery (delete biggest safe things)

From biggest to safest:

```bash
# 1. Clean old apt cache (usually several GB)
apt-get clean
rm -rf /var/cache/apt/archives/*.deb

# 2. Clear systemd journal (often 10–30+ GB when broken)
journalctl --vacuum-size=100M
# or nuclear:
rm -rf /var/log/journal/*   # then reboot → journald recreates

# 3. Remove old snaps (if you use snap)
snap list --all | grep disabled | awk '{print $1, $3}' | while read snap rev; do snap remove "$snap" --revision="$rev"; done

# 4. Clear thumbnail cache
rm -rf /home/*/ .cache/thumbnails/*

# 5. Clear /tmp (usually safe)
rm -rf /tmp/*
```

After each big deletion → check free space:

```bash
df -h /
```

### Step 4: Stop the thing that keeps filling the disk

Most frequent causes in 2024–2026 Ubuntu systems:

- Journald without limit → add to `/etc/systemd/journald.conf`:

```ini
SystemMaxUse=300M
SystemKeepFree=2G
RuntimeMaxUse=100M
```

Then: `systemctl restart systemd-journald`

- rsyslog / syslog-ng writing forever without rotation
- snapd refreshing huge snaps endlessly
- flatpak updating apps with huge caches
- docker container logs without limit (json-file driver)
- some VPN / mining / backup software writing logs or temp files

Quick check what is actively writing right now:

```bash
watch -n 2 "lsof / | grep REG | grep -v deleted | awk '{print \$NF}' | sort | uniq -c | sort -nr | head -8"
```

or simpler:

```bash
iotop   # (install if needed: apt install iotop)
```

### Step 5: Recommended realistic recovery path

1. Boot Ubuntu live USB (same version preferred)
2. Open terminal
3. Mount your root partition:

```bash
sudo mount /dev/nvme0n1pX /mnt          # or sdaX, check with lsblk
sudo mount --bind /dev  /mnt/dev
sudo mount --bind /proc /mnt/proc
sudo mount --bind /sys  /mnt/sys
sudo mount --bind /run  /mnt/run
sudo chroot /mnt
```

4. Inside chroot:

```bash
du -shx /* | sort -hr | head -12
journalctl --vacuum-size=50M
apt-get clean
rm -rf /var/log/journal/*
# ... other cleanups from above
sync
exit
```

5. Reboot and remove USB

If still fails → most people at this point reinstall (especially if /usr got damaged earlier + full disk).

**References:**

- None (standard Linux troubleshooting commands & recovery steps)