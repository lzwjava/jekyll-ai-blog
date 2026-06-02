---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Fix Sudo via GRUB Recovery Mode
translated: false
type: note
---

Question: I am now at the GRUB menu showing options like Ubuntu, Advanced options, Memory test, etc. How do I proceed to fix the broken sudo?

Answer:

Since your main goal is to recover the broken sudo (due to wrong ownership after the chown mistake), **do not** select the normal "Ubuntu" entry yet — it will boot into the broken system and you still won't have sudo.

Instead, follow one of these two paths from the current GRUB screen (both can work, pick the easier one for you):

**Path 1: Try Recovery Mode first (fastest if it works — no USB needed)**

1. In GRUB, highlight **Advanced options for Ubuntu** and press Enter.
2. You will see a list of kernel entries, for example:
   - Ubuntu, with Linux 6.8.0-40-generic (or similar)
   - Ubuntu, with Linux 6.8.0-40-generic (recovery mode)   ← **this one**
   - Older kernels (if any)
3. Select the line that says **(recovery mode)** for the newest kernel (usually the second or third line) and press Enter.
4. Wait for the recovery menu to appear. It looks like a purple/blue text screen with options such as:
   - resume             normal boot
   - clean              clean disk space
   - dpkgs              repair broken packages
   - fsck               check all filesystems
   - grub               update GRUB boot loader
   - network            enable networking
   - root               Drop to root shell prompt   ← **choose this**
5. Select **root** → press Enter.
6. You should now have a root shell prompt (# symbol, already root — no password needed in most cases).
7. The filesystem might be read-only at first. Make it writable:
   ```
   mount -o remount,rw /
   sync
   ```
8. Now fix sudo (minimum commands):
   ```
   chown root:root /usr/bin/sudo
   chmod 4755 /usr/bin/sudo
   ```
   Also fix the sudo library directory you mentioned earlier:
   ```
   chown -R root:root /usr/lib/sudo
   chmod -R 755 /usr/lib/sudo
   ```
9. Optional but strongly recommended — fix more common damage from the chown -R:
   ```
   chown root:root /usr/bin/pkexec 2>/dev/null
   chmod 4755 /usr/bin/pkexec 2>/dev/null
   chown -R root:root /usr/libexec /usr/lib/cups 2>/dev/null
   ```
10. Exit the shell and continue booting:
    ```
    exit
    ```
    Then select **resume** (or just type `reboot` if you prefer).
11. The system should now boot normally and sudo should work again (test with `sudo -l` after login).

**Path 2: If recovery mode fails or you get errors → boot from the Ubuntu live USB instead**

- Restart the computer (hold power button if needed).
- Enter the **boot menu** (press F12, F10, F9, Esc, or similar key shown on startup screen — different per laptop/brand).
- Choose your USB stick (it may say "USB: Kingston", "UEFI: Ubuntu", etc.).
- Select **Try Ubuntu** (not Install).
- Once on the desktop → follow the live USB chroot steps I gave you earlier:
  - Identify partition with `lsblk -f`
  - Mount it (`sudo mount /dev/sdaX /mnt/root`)
  - Bind mounts for /dev /proc /sys /run /dev/pts
  - `sudo chroot /mnt/root`
  - Run the same chown/chmod commands as above
  - Exit, unmount, reboot without USB

**Quick tip:** If you succeed with recovery mode (Path 1), it's much faster — no need to touch the USB.
If it doesn't give you a usable root shell (e.g. drops to busybox or filesystem errors), go straight to Path 2.

After fixing sudo, you can also clean up the huge CUPS logs from inside the fixed system:
```
sudo truncate -s 0 /var/log/cups/error_log*
```

Good luck — almost there.

References:

- [Ask Ubuntu: How to boot into recovery mode](https://askubuntu.com/questions/156209/how-do-i-boot-to-recovery-mode)
- [Ubuntu Community Help: RecoveryMode](https://help.ubuntu.com/community/RecoveryMode)
