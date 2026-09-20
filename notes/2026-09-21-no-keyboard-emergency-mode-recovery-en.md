---
audio: false
generated: true
image: false
lang: en
layout: post
title: No Keyboard Emergency Mode Recovery
translated: false
type: note
---

**Question:** In emergency mode where the keyboard isn't responding, how do you recover when you can't type?

**Answer:**

If the keyboard truly isn't working at all in the emergency shell, here are your options ranked by ease:

---

### 1. Try a Different Keyboard / Port

- Swap to a **USB keyboard on a different port** (try USB 2.0 ports instead of USB 3.0)
- Try a **PS/2 keyboard** if the motherboard has that port
- USB keyboards sometimes aren't initialized early enough in boot — a different port or hub may help

---

### 2. SSH In From Another Machine

If the machine has network access (even in emergency mode, networking sometimes comes up):

```bash
ssh user@<ip-address>
```

Then run the diagnostic and fix commands from there.

---

### 3. Boot From a Live USB/CD

This is the most reliable recovery path when you can't interact with the broken system at all:

1. Boot a **Ubuntu/Debian/Fedora Live USB**
2. Mount your root partition:

   ```bash
   sudo mount /dev/sdXN /mnt        # replace sdXN with your root partition
   ```

3. Edit fstab directly:

   ```bash
   sudo nano /mnt/etc/fstab
   ```

4. Comment out the two bad UUID lines, save, reboot

---

### 4. Edit Kernel Boot Parameters (No Keyboard Needed at First)

At the **GRUB menu** (before Linux loads), you can sometimes use arrow keys only:

- Highlight your boot entry → press **`e`** to edit
- Find the `linux` line, add `single` or `init=/bin/bash` at the end
- Press **Ctrl+X** to boot

This drops you into a minimal shell where the keyboard *might* work even if it didn't in emergency mode.

---

### 5. VM-Specific (if this is a virtual machine)

- Use the **hypervisor console** (vSphere, Proxmox, VirtualBox, etc.) — these have their own keyboard input that bypasses the OS entirely
- Attach the disk to another VM and edit `/etc/fstab` from there

---

**The Live USB route (#3) is the safest** — it lets you fix `/etc/fstab` without needing the broken system's keyboard to work at all.

---

**References:**

- [Recovering from emergency mode – Ubuntu Forums](https://ubuntuforums.org/showthread.php?t=2282512)
- [How to boot into rescue/emergency mode – Red Hat Docs](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/managing_systems_using_the_rhel_system_roles/assembly_recovering-and-restoring-a-system_managing-systems-using-the-rhel-system-roles)
- [fstab – Arch Linux Wiki](https://wiki.archlinux.org/title/Fstab)
