---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Fix Broken Sudo After Chown Disaster
translated: false
type: note
---

**Question:** I ran `sudo chown -R $USER:$(id -gn) $(npm -g config get prefix)` and the prefix was `/usr/`, which changed ownership of many system files (including `/usr/bin/sudo`), and now sudo says "sudo must be owned by uid 0" and doesn't work. How can I fix this?

**Answer:**

Your system is in a **very dangerous state** right now — many critical system files in `/usr/` are probably owned by your normal user instead of root.
The most important file right now is `/usr/bin/sudo` (or sometimes `/bin/sudo` or `/usr/local/bin/sudo` depending on distribution).

Here are the realistic recovery options, ordered from safest → most desperate:

### Option 1 – Best chance (if you still have any working root access)

Any method that still gives root (even temporarily):

- **Recovery / single-user / rescue mode** (most distributions)
  Reboot → hold Shift (GRUB) or Esc (some systemd) → choose Advanced options → Recovery mode → root shell
  or at boot menu select "(recovery mode)" or "Rescue"

  Once you have a root shell:

  ```bash
  # Most important fix first
  chown root:root /usr/bin/sudo
  chmod 4755 /usr/bin/sudo

  # Then try to fix the bigger damage (this takes time)
  chown -R root:root /usr/bin /usr/sbin /usr/lib /bin /sbin
  chmod -R u+s /usr/bin/sudo          # just in case
  ```

- **Live USB** (very reliable)
  Boot from Ubuntu / Fedora / Mint live USB
  Open terminal → mount your root filesystem:

  ```bash
  sudo mkdir /mnt/root
  sudo mount /dev/sdaX /mnt/root           # replace sdaX with your root partition
  sudo mount --bind /dev   /mnt/root/dev
  sudo mount --bind /proc  /mnt/root/proc
  sudo mount --bind /sys   /mnt/root/sys
  sudo mount --bind /run   /mnt/root/run

  sudo chroot /mnt/root
  ```

  Then inside chroot run:

  ```bash
  chown root:root /usr/bin/sudo
  chmod 4755      /usr/bin/sudo
  exit
  ```

  After exit → `sudo reboot`

### Option 2 – Quick & dirty (if you only need sudo back and accept risk)

If you have **pkexec** (PolicyKit) still working (common on Ubuntu/Debian):

```bash
pkexec chown root:root /usr/bin/sudo
pkexec chmod 4755 /usr/bin/sudo
```

or if you have another sudo-like tool still working:

- `doas` (if installed)
- `su -` (if you know root password)
- `sudoedit` / `sudo -e` sometimes still works even when sudo is broken

### Option 3 – Nuclear option (last resort)

If **nothing** gives root anymore:

1. Boot live USB
2. Mount root partition
3. Copy a known-good sudo binary from the live system:

```bash
sudo cp /usr/bin/sudo /mnt/root/usr/bin/sudo
sudo chown root:root /mnt/root/usr/bin/sudo
sudo chmod 4755      /mnt/root/usr/bin/sudo
```

This often works because live USB sudo is usually the same version.

### Summary – fastest realistic recovery path most people use

1. Boot Ubuntu live USB (same version as your system if possible)
2. Mount your broken system
3. `chroot` into it
4. Fix sudo permissions
5. Reboot and pray the rest of the system still boots

Many people in this situation end up **reinstalling the OS** because the damage from `chown -R` on `/usr/` is usually too widespread (broken packages, missing libraries, etc.).

**Never** run chown/chmod -R on any path you get from `npm config get prefix` unless you are 100% sure what folder it points to.

**References:**

- None (this is standard Linux permission recovery knowledge)
