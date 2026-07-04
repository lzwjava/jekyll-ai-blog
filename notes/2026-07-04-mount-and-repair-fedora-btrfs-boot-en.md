---
audio: false
generated: true
image: false
lang: en
layout: post
title: Mount and Repair Fedora Btrfs Boot
translated: false
type: note
---

**Question:** `lsblk -f` confirms `nvme0n1p1` = FAT32 (ESP), `nvme0n1p2` = ext4 (`/boot`), `nvme0n1p3` = btrfs labeled `fedora`. `/mnt/sysroot` doesn't exist this session. What now?

**Answer:**

Good — the filesystem check removed all ambiguity. This boot session never mounted anything (the earlier `/mnt/sysroot` was from a different session, probably a rescue-mode boot), so `/mnt` is free. Straight to the full sequence:

```bash
# 1. Root — btrfs, so mount the 'root' subvolume, not the top level
sudo mount -o subvol=root,compress=zstd:1 /dev/nvme0n1p3 /mnt

# Verify you got the actual OS tree, not "root/ home/" folders:
ls /mnt        # expect: bin boot etc usr var ...

# 2. Boot chain
sudo mount /dev/nvme0n1p2 /mnt/boot
sudo mount /dev/nvme0n1p1 /mnt/boot/efi

# 3. Virtual filesystems
sudo mount --rbind /dev  /mnt/dev  && sudo mount --make-rslave /mnt/dev
sudo mount --rbind /sys  /mnt/sys  && sudo mount --make-rslave /mnt/sys
sudo mount -t proc proc  /mnt/proc
sudo mount --bind  /run  /mnt/run

# 4. Enter
sudo chroot /mnt /bin/bash
```

If step 1 fails with `subvol=root` not found, list what actually exists:

```bash
sudo mount /dev/nvme0n1p3 /mnt          # top-level mount
sudo btrfs subvolume list /mnt          # look for 'root' and 'home' (Fedora defaults)
sudo umount /mnt                        # then remount with the right subvol name
```

Inside the chroot, verify before repairing:

```bash
ls /boot                            # vmlinuz-*, initramfs-* files present?
ls /boot/efi/EFI/fedora             # grubx64.efi present?
cat /etc/fedora-release             # confirms you're in the right root
ping -c1 pypi.org                   # DNS via bound /run
```

Then the repair:

```bash
dnf reinstall -y kernel-core kernel-modules kernel-modules-core
dracut --regenerate-all --force
grub2-mkconfig -o /boot/grub2/grub.cfg
exit
```

And cleanly tear down before reboot:

```bash
sudo umount -R /mnt
sudo reboot
```

One diagnostic worth doing while chrooted, since your original failure was a custom kernel: `ls /boot` and compare the `initramfs-*` file sizes. A custom kernel's initramfs that's dramatically smaller than the stock one usually means dracut omitted storage drivers (NVMe/btrfs modules) — the classic cause of a hang at boot. That tells you whether the fix is `dracut --force --kver <your-kver>` with proper module config rather than a full reinstall.

**References:**

- [Fedora btrfs layout — subvolumes `root` and `home`](https://fedoraproject.org/wiki/Changes/BtrfsByDefault)
- [dracut(8) — regenerating initramfs](https://man7.org/linux/man-pages/man8/dracut.8.html)
