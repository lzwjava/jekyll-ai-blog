---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Fix Broken Sudo Permissions Quickly
translated: false
type: note
---

The error message:

```
sudo: /usr/bin/sudo must be owned by uid 0 and have the setuid bit set
```

means the **sudo** binary has incorrect ownership or permissions. Normally, it must be:

- Owned by **root** (UID 0)
- Have the **setuid bit** set (so it runs as root even when called by a normal user)

This often happens from accidental commands like `chown`, `chmod -R`, or messing with `/usr/bin`.

You can't fix this with `sudo` (it's broken), so you need root access another way. Here are the main fixes for Ubuntu (works on 20.04–26.04+ versions).

### Method 1: Boot into Recovery Mode (Recommended & Safest)

1. **Reboot** your computer.
2. Hold **Shift** (or **Esc** on some systems) during boot to show the **GRUB menu**.
3. Select **Advanced options for Ubuntu**.
4. Choose a line ending in **(recovery mode)** → press Enter.
5. In the recovery menu, select **root** → **Drop to root shell prompt** → press Enter.
   - You'll get a `#` prompt as root (no password needed here).
6. Remount the filesystem read-write (important!):

   ```
   mount -o remount,rw /
   ```

7. Fix the sudo binary:

   ```
   chown root:root /usr/bin/sudo
   chmod 4755 /usr/bin/sudo
   ```

   - `4755` = owner read/write/execute + setuid bit + group/other read/execute.
   - After this, `ls -l /usr/bin/sudo` should show something like:
     ```
     -rwsr-xr-x 1 root root ... /usr/bin/sudo
     ```
     (the `s` in place of `x` = setuid bit)

8. Optional but good: also fix `su` if broken:

   ```
   chown root:root /usr/bin/su
   chmod 4755 /usr/bin/su
   ```

9. Exit the shell:

   ```
   exit
   ```

10. From recovery menu: choose **resume** → normal boot.
11. After reboot, test with:

    ```
    sudo ls
    ```

It should ask for your password and work.

### Method 2: If You Have Root Password Set (or Can Log In as Root on TTY)

- Switch to a text console: press **Ctrl + Alt + F3** (or F2–F6).
- Log in as **root** (if you have a root password) or your user if root login is allowed.
- Then run the same fix commands as above:

  ```
  mount -o remount,rw /
  chown root:root /usr/bin/sudo
  chmod 4755 /usr/bin/sudo
  exit
  ```

- Go back to GUI: **Ctrl + Alt + F1** or **F2**.

### Method 3: If Recovery Mode Fails or You Prefer Live USB

1. Boot from an **Ubuntu Live USB** (same version if possible).
2. Open terminal → mount your installed system (replace `/dev/sda1` with your root partition – check with `lsblk`):

   ```
   sudo mkdir /mnt/root
   sudo mount /dev/sda1 /mnt/root
   sudo mount --bind /dev /mnt/root/dev
   sudo mount --bind /proc /mnt/root/proc
   sudo mount --bind /sys /mnt/root/sys
   sudo mount --bind /run /mnt/root/run
   sudo chroot /mnt/root
   ```

3. Now you're "inside" your broken system as root → run:

   ```
   chown root:root /usr/bin/sudo
   chmod 4755 /usr/bin/sudo
   exit
   ```

4. Reboot without the USB.

### Extra Checks After Fix

- Run `ls -l /usr/bin/sudo` → should show `-rwsr-xr-x root root`
- If error mentions `/usr/local/bin/sudo` instead: remove it (it's overriding the real one):

  ```
  sudo rm /usr/local/bin/sudo
  hash -r   # refresh shell cache
  ```

- Reinstall sudo package if still weird:

  ```
  sudo apt update
  sudo apt install --reinstall sudo
  ```

This almost always fixes it. If you get a different error or it still fails, tell me what exactly happens (and your Ubuntu version if you know it).