---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Fix Broken GNOME After Chown Mistake
translated: false
type: note
---

Question: After attempting to boot from the USB on the Lenovo XiaoXin 14 IAH8 laptop (currently running Ubuntu), it fails to boot and shows the error "failed to start gdm gnome display manager". This happened because previously, to fix a Claude code CLI upgrade issue, the command `sudo chown -R $(whoami) /usr/` was run, which changed ownership of /usr/ (and subdirectories) from root to the user lzwjava. How to fix this broken GNOME Display Manager (GDM) login screen issue?

Answer:

The command `sudo chown -R lzwjava /usr/` (or whatever your username is) is extremely dangerous. It broke system binaries, libraries, configuration files, and services that must be owned by **root** (or sometimes specific system users like systemd-*, messagebus, etc.). GDM failing to start is just the most visible symptom — many other parts of the system are likely also broken or have permission issues.

### Quick Recovery Options (from easiest to more involved)

#### Option 1: Boot into recovery / single-user mode (recommended first try)

1. Power on the laptop.
2. When the GRUB menu appears:
   - If GRUB is hidden, hold **Shift** (or spam **Esc**) right after powering on.
3. In GRUB, highlight your normal Ubuntu entry → press **e** to edit.
4. Find the line that starts with `linux` (usually contains `quiet splash`).
5. At the end of that line, add a space and then:
   `rw init=/bin/bash`
6. Press **Ctrl + X** or **F10** to boot.
7. You should drop into a root shell (no login required).

Now run these commands one by one:

```bash
mount -o remount,rw /
mount --all

# Restore correct ownership (this is the critical step)
chown -R root:root /usr
chown root:root /usr/bin /usr/sbin /usr/lib /usr/share 2>/dev/null

# Fix any obvious executable bits that might have been lost
chmod -R u+rX,go+rX,go-w /usr/bin /usr/sbin /usr/libexec
chmod -R 755 /usr/bin /usr/sbin

# Reinstall gdm3 (very important – many files were probably damaged)
apt update
apt install --reinstall gdm3 ubuntu-gnome-desktop gnome-session gdm3

# Also reinstall core packages that almost certainly have wrong ownership now
apt install --reinstall bash coreutils systemd udev passwd login sudo

# Optional but helpful: fix common other locations
chown -R root:root /etc /bin /sbin /lib /lib64 /var 2>/dev/null
chmod -R 755 /bin /sbin /lib /lib64 2>/dev/null

sync
reboot
```

- After reboot, GDM should start again (you may need to select GNOME on Wayland or X11 at login).
- If it still fails, proceed to Option 2.

#### Option 2: Use live USB (Ubuntu or any Linux live session) to repair

1. Boot from your Ubuntu live USB (or make a new one).
2. Choose "Try Ubuntu".
3. Open Terminal.
4. Identify your internal drive (usually `/dev/nvme0n1pX` or `/dev/sdaX` — be **very careful**).

```bash
sudo fdisk -l                # find your root partition (look for Linux filesystem ~50–100+ GB)
sudo mount /dev/nvme0n1pX /mnt   # replace X with your root partition number
sudo mount --bind /dev   /mnt/dev
sudo mount --bind /proc  /mnt/proc
sudo mount --bind /sys   /mnt/sys
sudo mount --bind /run   /mnt/run
sudo chroot /mnt
```

Now inside chroot, run the same repair commands as above:

```bash
apt update
apt install --reinstall gdm3 ubuntu-gnome-desktop gnome-session
chown -R root:root /usr /etc /bin /sbin /lib /lib64 /var
chmod -R 755 /usr/bin /usr/sbin /bin /sbin
exit
reboot
```

#### Option 3: Last resort — reinstall Ubuntu (fastest if above fails)

- Boot from Ubuntu live USB.
- Choose "Install Ubuntu".
- Select "Something else" → reuse your existing partitions but **format only / (root)** partition (keep /home if you have separate /home).
- This will reinstall the system files correctly while keeping your personal files (if /home is separate or you skip formatting it).

### Important notes

- Never run `chown -R` on `/`, `/usr`, `/etc`, `/var`, etc. again — it's one of the fastest ways to destroy a Linux system.
- For future "permission fix" attempts, only chown specific directories/files, e.g. `sudo chown -R $USER:$USER ~/project` or `/home/yourname`.
- After recovery, run `sudo apt update && sudo apt upgrade && sudo apt install --reinstall ubuntu-desktop` to make sure everything is consistent.

If you get stuck at any step (e.g. specific error messages), provide them and I can give more targeted commands.

References:

- [https://askubuntu.com/questions/26496/how-to-recover-from-accidentally-changing-ownership-of-usr](https://askubuntu.com/questions/26496/how-to-recover-from-accidentally-changing-ownership-of-usr)
- [https://unix.stackexchange.com/questions/132281/chown-really-recursive-and-dangerous](https://unix.stackexchange.com/questions/132281/chown-really-recursive-and-dangerous)
- [https://help.ubuntu.com/community/Boot-Repair](https://help.ubuntu.com/community/Boot-Repair)
