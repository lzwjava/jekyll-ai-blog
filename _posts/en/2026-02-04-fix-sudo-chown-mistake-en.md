---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Fix Broken Sudo After Chown Mistake
translated: false
type: note
---

The error you're seeing:

```
sudo: /usr/bin/sudo must be owned by uid 0 and have the setuid bit set
```

happened precisely because you ran something like:

```bash
sudo chown -R $USER /usr
```

(or similar — probably `$USER:$USER` or `$USER` alone). This changed ownership of **/usr/bin/sudo** (and thousands of other critical files) away from root, and removed the special **setuid bit** that lets sudo run as root even when you execute it as a normal user.

Fixing **just sudo** is quick and usually works right away. Fixing the rest of /usr (so the system becomes stable again) is much harder — /usr contains libraries, binaries, headers, etc., and many expect to be owned by root:root (or sometimes root:staff, root:other groups). A recursive chown like that breaks a huge number of things.

### Step 1: Fix sudo itself (so you can use it again)

You can't use sudo right now, so get root access without it:

**Option A – Recovery mode (easiest on a desktop/laptop)**

1. Reboot the computer.
2. Hold **Shift** during boot (or **Esc** on some machines) until the GRUB menu appears.
3. Select **Advanced options for Ubuntu** → choose any line that ends with **(recovery mode)** → press Enter.
4. In the recovery menu, select **root** → **Drop to root shell prompt** → press Enter.  
   → You now have a `#` prompt (full root access, no password needed here).
5. Remount the filesystem read-write:

   ```
   mount -o remount,rw /
   ```

6. Fix sudo:

   ```
   chown root:root /usr/bin/sudo
   chmod 4755 /usr/bin/sudo
   ```

   After this, run:

   ```
   ls -l /usr/bin/sudo
   ```

   → You should see something like:

   ```
   -rwsr-xr-x 1 root root ... /usr/bin/sudo
   ```

   (the `s` instead of `x` in the owner's execute position = setuid bit is set)

7. Exit and resume:

   ```
   exit
   ```

   Then select **resume** → normal boot.

8. After reboot, test:

   ```
   sudo -k    # clear any old cache
   sudo ls
   ```

   It should now ask for your password and work.

**Option B – If recovery mode doesn't appear or you prefer a live USB**

- Boot from an Ubuntu live USB (same version if possible — 24.04 or whatever you're on).
- Open Terminal → mount your real system (replace `/dev/nvme0n1p2` or `/dev/sda1` with your actual root partition — use `lsblk` to find it):

  ```
  sudo mkdir /mnt/root
  sudo mount /dev/nvme0n1p2 /mnt/root           # adjust device name
  sudo mount --bind /dev   /mnt/root/dev
  sudo mount --bind /proc  /mnt/root/proc
  sudo mount --bind /sys   /mnt/root/sys
  sudo mount --bind /run   /mnt/root/run
  sudo chroot /mnt/root
  ```

- Now you're inside your broken system as root → run:

  ```
  mount -o remount,rw /
  chown root:root /usr/bin/sudo
  chmod 4755 /usr/bin/sudo
  exit
  ```

- Reboot (remove USB).

### Step 2: After sudo works again — assess and repair the rest of /usr

Now that sudo is back, many things might still be broken (e.g. apt, graphical apps, libraries won't load correctly because wrong owner).

Run these to see obvious damage:

```bash
sudo dpkg --configure -a
sudo apt update
sudo apt install --reinstall sudo   # just in case
ls -l /usr/bin/ls /usr/bin/bash /usr/lib/x86_64-linux-gnu/libc.so*   # should be root:root
```

Common quick fixes for many files:

```bash
# Fix common system binaries & libs (takes time, but helps a lot)
sudo chown -R root:root /usr/bin /usr/sbin /usr/lib /usr/share

# Some directories use other groups (safe to run anyway)
sudo chown root:staff   -R /usr/local   # if you use /usr/local a lot
```

But this **won't fix everything** — some packages expect very specific owners/groups/permissions.

### Realistic options at this point

1. **Best & fastest long-term fix**  
   → **Reinstall Ubuntu** (keep /home if you want).  
   Boot live USB → "Try Ubuntu" → use the installer → choose "Something else" → reuse your existing / partition but **format it** (or just overwrite /usr,/etc,/var if you're advanced).  
   → Takes 20–40 minutes and gives you a clean system.

2. **Try to repair in place (advanced, time-consuming, may not fully succeed)**

   - Reinstall core packages:

     ```bash
     sudo apt install --reinstall ubuntu-desktop ubuntu-minimal linux-generic
     sudo apt install --reinstall $(dpkg -S /usr/bin/* | cut -d: -f1 | sort -u)
     ```

   - But expect many dependency errors — it can snowball.

3. **Backup important data** (from live USB if needed) and reinstall.

Doing a recursive chown on /usr almost always ends with reinstall being the sanest path — especially since many setuid/setgid binaries, shared libraries, etc., are now wrong.

If you want to try more targeted fixes first, tell me:
- Your Ubuntu version (`cat /etc/os-release` if you can run it now)
- What breaks when you try to use apt or open a GUI app
- Whether you have important unsaved data in /home

Good luck — and never run recursive chown/chmod on system directories again! 😅