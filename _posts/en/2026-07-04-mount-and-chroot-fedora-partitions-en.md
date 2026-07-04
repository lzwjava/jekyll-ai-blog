---
audio: false
generated: true
image: false
lang: en
layout: post
title: Mount and Chroot Fedora Partitions
translated: false
type: note
---

**Question:** My `lsblk` on the Fedora live USB shows `nvme0n1p1` (600M), `nvme0n1p2` (2G), `nvme0n1p3` (231.2G, already mounted at `/mnt/sysroot`). What are the exact mount + chroot commands for this layout?

**Answer:**

Your layout is the standard Fedora scheme:

| Partition | Size | Role |
| --- | --- | --- |
| `nvme0n1p1` | 600M | EFI System Partition (FAT32) |
| `nvme0n1p2` | 2G | `/boot` (ext4) — kernels + initramfs live here |
| `nvme0n1p3` | 231.2G | root, almost certainly **btrfs** with `root` and `home` subvolumes |

Two things to notice: something already mounted p3 at `/mnt/sysroot`, and if it's btrfs, it may be mounted at the *top level* (showing `root/` and `home/` as directories) rather than the `root` subvolume. Check first:

```bash
lsblk -f /dev/nvme0n1        # confirm fstypes
ls /mnt/sysroot              # if you see just "root home" dirs → top-level btrfs mount
```

Cleanest path — start fresh at `/mnt`:

```bash
sudo umount -R /mnt/sysroot 2>/dev/null

# root subvolume (Fedora btrfs default)
sudo mount -o subvol=root /dev/nvme0n1p3 /mnt
# if lsblk -f said ext4 instead: sudo mount /dev/nvme0n1p3 /mnt

sudo mount /dev/nvme0n1p2 /mnt/boot
sudo mount /dev/nvme0n1p1 /mnt/boot/efi

# virtual filesystems (rbind so /dev/pts and efivars come along)
sudo mount --rbind /dev  /mnt/dev  && sudo mount --make-rslave /mnt/dev
sudo mount --rbind /sys  /mnt/sys  && sudo mount --make-rslave /mnt/sys
sudo mount -t proc proc  /mnt/proc
sudo mount --bind  /run  /mnt/run

sudo chroot /mnt /bin/bash
```

Sanity checks inside the chroot before repairing:

```bash
ls /boot                          # should list vmlinuz-*, initramfs-*
ls /boot/efi/EFI/fedora           # grubx64.efi, grub.cfg stub
ls /sys/firmware/efi/efivars | head   # non-empty → efibootmgr will work
cat /etc/resolv.conf && ping -c1 pypi.org   # DNS for dnf
```

Then the actual repair (from the earlier flow):

```bash
dnf reinstall -y kernel-core kernel-modules
dracut --regenerate-all --force
grub2-mkconfig -o /boot/grub2/grub.cfg
```

Two footnotes on your output: `nvme0n1` and `nvme0n2` showing `0B` at the disk level is a known Apple NVMe quirk (multi-namespace controller reporting) — the partition sizes are what matter, and they're correct. And `zram0 [SWAP]` is just the live session's compressed-RAM swap, ignore it.

**References:**

- [Fedora default partitioning (btrfs subvolumes)](https://docs.fedoraproject.org/en-US/fedora/latest/install-guide/install/Installing_Using_Anaconda/#sect-installation-gui-manual-partitioning-recommended)
- [Recover from a Failed Linux Kernel Boot — lzwjava](https://lzwjava.github.io/recover-from-a-failed-linux-kernel-boot-en)
