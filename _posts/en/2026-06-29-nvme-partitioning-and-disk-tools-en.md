---
audio: false
generated: true
image: false
lang: en
layout: post
title: NVMe Partitioning and Disk Tools
translated: false
type: note
---

Question: What is `lsblk`, how do I partition a disk when installing Fedora, what disk tools exist, and why does an NVMe drive (e.g. `nvme0n1`) appear split into multiple devices?

Answer:

You probably mean `lsblk` ("list block devices"), not `lbdisk`. It shows the tree of block devices and how they're sliced.

```bash
lsblk
# NAME        MAJ:MIN RM   SIZE RO TYPE MOUNTPOINTS
# nvme0n1     259:0    0 931.5G  0 disk
# ├─nvme0n1p1 259:1    0   600M  0 part /boot/efi
# ├─nvme0n1p2 259:2    0     1G  0 part /boot
# └─nvme0n1p3 259:3    0 929.9G  0 part /
```

### NVMe naming — why it looks "split"

The naming encodes the NVMe topology, not multiple disks:

```
nvme0  n1   p3
 │     │    └─ partition 3
 │     └────── namespace 1
 └──────────── controller 0 (the physical SSD)
```

- `nvme0` = the controller (one physical SSD).
- `n1` = namespace 1. NVMe drives expose storage as *namespaces*; consumer SSDs almost always have exactly one (`n1`). Enterprise drives can carve one SSD into several namespaces, which then look like separate disks (`nvme0n1`, `nvme0n2`).
- `p1/p2/p3` = partitions inside that namespace.

So `nvme0n1p1 … p3` is **one** SSD, one namespace, three partitions. Compare to SATA where it'd be `sda` → `sda1, sda2, sda3`. The "extra" letters (`n1`) are the only difference. You're seeing partitioning, not multiple disks.

### What partitioning actually is

A partition is just a contiguous byte range recorded in a partition table (GPT on modern UEFI systems). The kernel reads the GPT header at the start of the disk and creates the `pN` device nodes. Nothing is physically segmented — it's metadata pointing at offsets.

A typical Fedora UEFI layout:

| Partition | Size | FS | Mount | Purpose |
|-----------|------|-----|-------|---------|
| p1 | ~600M | FAT32 | `/boot/efi` | EFI System Partition (bootloader) |
| p2 | ~1G | ext4 | `/boot` | kernel + initramfs |
| p3 | rest | btrfs | `/` | root (Fedora default is btrfs) |

Fedora's default also puts `/home`, `/`, and others as **btrfs subvolumes** inside p3 rather than separate partitions — flexible, no fixed size split.

### Partitioning during Fedora install (Anaconda)

In the installer: **Installation Destination → Storage Configuration**.

- **Automatic** — Anaconda creates the ESP + `/boot` + btrfs root for you. Pick this unless you have a reason not to.
- **Custom** — you define mount points; it builds partitions/subvolumes.
- **Advanced (Blivet-GUI)** — raw partition editor, full manual control.

### Partitioning from the CLI

If you want to do it by hand (or scripted), the modern tools:

```bash
# Inspect
lsblk -f                      # devices + filesystems + UUIDs
sudo fdisk -l /dev/nvme0n1    # partition table dump

# GPT partitioning, scriptable
sudo sgdisk -n 1:0:+600M -t 1:ef00 /dev/nvme0n1   # ESP
sudo sgdisk -n 2:0:+1G   -t 2:8300 /dev/nvme0n1   # /boot
sudo sgdisk -n 3:0:0     -t 3:8300 /dev/nvme0n1   # root, rest of disk

# Interactive alternatives
sudo gdisk /dev/nvme0n1       # GPT-aware fdisk
sudo cfdisk /dev/nvme0n1      # curses TUI, easiest interactive
sudo parted /dev/nvme0n1      # supports resize, scripting

# Format
sudo mkfs.fat -F32 /dev/nvme0n1p1
sudo mkfs.ext4 /dev/nvme0n1p2
sudo mkfs.btrfs /dev/nvme0n1p3
```

`sgdisk` partition type codes worth knowing: `ef00` = EFI System, `8300` = Linux filesystem, `8200` = swap, `8e00` = LVM.

Key thing for your mental model: the "multiple disks" appearance under one NVMe is just `controller → namespace → partitions`. One SSD, sliced by a GPT table. If you ever see `nvme0n2`, *that's* a genuinely separate namespace, which only enterprise/datacenter drives expose.

References:

- [lsblk(8) man page](https://man7.org/linux/man-pages/man8/lsblk.8.html)
- [NVMe namespace and device naming — Arch Wiki](https://wiki.archlinux.org/title/NVMe)
- [Fedora Installation Guide — Manual Partitioning](https://docs.fedoraproject.org/en-US/fedora/latest/install-guide/install/Installing_Using_Anaconda/)
- [sgdisk / gdisk documentation](https://www.rodsbooks.com/gdisk/)
