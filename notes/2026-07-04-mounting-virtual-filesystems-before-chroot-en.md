---
audio: false
generated: true
image: false
lang: en
layout: post
title: Mounting Virtual Filesystems Before Chroot
translated: false
type: note
---

**Question:** In the recovery flow from my post [Recover from a Failed Linux Kernel Boot](https://lzwjava.github.io/recover-from-a-failed-linux-kernel-boot-en), why do we run these five mount commands before `chroot /mnt`? What does each one actually do?

**Answer:**

The five lines are building a *functional* copy of your installed system inside `/mnt` so that `chroot /mnt` behaves like you actually booted that system. One line mounts your real disk; the other four graft the **live USB's kernel-provided virtual filesystems** into it.

## The core insight: chroot changes the filesystem view, not the kernel

`chroot` is a trivially simple syscall — it just changes what a process sees as `/`. After `chroot /mnt`, when a program opens `/proc/mounts`, the kernel resolves that to `/mnt/proc/mounts` on the real filesystem. But you're still running the **live USB's kernel**. The broken kernel on disk is just files; it's not executing.

So the problem is: your on-disk root filesystem contains *empty directories* at `/dev`, `/proc`, `/sys`, `/run` — those are always populated at runtime by the kernel, never stored on disk. A chroot into a bare disk mount gives you a system that looks right but is deaf and blind: no devices, no process info, no kernel interfaces.

## Line by line

```bash
sudo mount /dev/nvme0n1pX /mnt
```

Normal block-device mount. The kernel reads the filesystem (ext4/btrfs) on that NVMe partition and attaches it at `/mnt`. Now `/mnt/boot`, `/mnt/etc`, `/mnt/usr` are your real installed system. (On Fedora with btrfs defaults you may need `-o subvol=root`, and a separate `mount /dev/nvme0n1pY /mnt/boot` plus `/mnt/boot/efi` — more on that below.)

```bash
sudo mount --bind /dev /mnt/dev
```

A **bind mount** makes an existing directory tree visible at a second location — same inodes, no copy, like a hardlink for directory trees at the VFS layer. `/dev` on the live system is a `devtmpfs` populated by the kernel + udev with device nodes: `/dev/nvme0n1`, `/dev/null`, `/dev/urandom`, `/dev/tty`.

Why the chrooted tools need it:

- `grub2-install` must open `/dev/nvme0n1` to write to the EFI partition and probe disk layout
- `dracut` reads `/dev/urandom`, probes block devices to decide which storage drivers go in the initramfs
- Anything that spawns a shell wants `/dev/tty`, `/dev/pts`

Without it: `grub2-install: error: cannot find a device for /boot/efi`.

```bash
sudo mount --bind /proc /mnt/proc
```

`procfs` is the kernel's process/state interface rendered as files. The critical consumer here is **`/proc/mounts`** — `grub2-mkconfig` and `dracut` read it to figure out what's mounted where and what the root device is. `/proc/cmdline`, `/proc/filesystems`, `/proc/cpuinfo` also get consulted. Without it, `grub2-mkconfig` typically dies with `/usr/sbin/grub2-probe: error: failed to get canonical path`.

```bash
sudo mount --bind /sys /mnt/sys
```

`sysfs` is the kernel's device-model tree — every device, driver, and bus as a directory hierarchy. Two critical users:

- **EFI variables** live at `/sys/firmware/efi/efivars`. `grub2-install` on UEFI calls `efibootmgr`, which writes the boot entry into NVRAM through this interface. No `/sys` → GRUB gets installed to disk but the Mac's firmware never learns about it — exactly the "boot entry may be broken" failure mode in the post.
- `dracut` walks `/sys/block/` and `/sys/devices/` to detect which drivers your hardware needs (this is how it knows to include the NVMe driver — the very module whose absence probably broke your custom kernel boot).

```bash
sudo mount --bind /run /mnt/run
```

A `tmpfs` for runtime state. The main reason on Fedora: udev's device database lives in `/run/udev`, and `dracut`/`lvm`/`cryptsetup` query it to resolve device properties and UUIDs. Also, Fedora symlinks `/etc/resolv.conf → /run/systemd/resolve/...`, so binding `/run` is what gives your chroot **working DNS** — which you need for `dnf reinstall kernel-core`.

## Mental model

```
Live USB kernel (running)          Disk (just files)
        │                                │
        ├── /dev  ─── bind ──►  /mnt/dev │
        ├── /proc ─── bind ──►  /mnt/proc├── your broken Fedora
        ├── /sys  ─── bind ──►  /mnt/sys │
        └── /run  ─── bind ──►  /mnt/run │
                                         ▼
                              chroot /mnt = "boot" the disk's
                              userspace on the USB's kernel
```

You're doing a Frankenstein boot: the live kernel provides hardware access, the disk provides the userspace (`dnf`, `dracut`, `grub2-install`, your configs). That's the entire trick.

## Two practical upgrades

**1. Use `--rbind` + `--make-rslave` for `/dev` and `/sys`** (what Arch's `arch-chroot` does):

```bash
sudo mount --rbind /dev  /mnt/dev  && sudo mount --make-rslave /mnt/dev
sudo mount --rbind /sys  /mnt/sys  && sudo mount --make-rslave /mnt/sys
sudo mount -t proc /proc /mnt/proc
sudo mount --bind /run   /mnt/run
```

Plain `--bind` only grafts the top-level mount, missing submounts like `/dev/pts` (pseudo-terminals — some scripts hang without it) and `/sys/firmware/efi/efivars`. `--rbind` recursively binds the whole subtree; `--make-rslave` prevents unmounts inside the chroot from propagating back and killing your live session.

**2. Don't forget the boot partitions before chrooting.** Fedora splits them, and both matter for kernel + GRUB repair:

```bash
# check layout first
lsblk -f
sudo mount /dev/nvme0n1pY /mnt/boot        # ext4 /boot, holds vmlinuz + initramfs
sudo mount /dev/nvme0n1p1 /mnt/boot/efi    # FAT32 ESP, holds grubx64.efi
```

If `/boot` isn't mounted, `dnf reinstall kernel` and `dracut --regenerate-all` write kernels into a directory on the root partition that the firmware will never see — the repair "succeeds" and the machine still won't boot. This is one of the most common silent failures in this exact recovery flow.

Or skip the ceremony entirely: `systemd-nspawn -D /mnt` (from the live USB) sets up all of this for you and gives a cleaner container-style chroot.

**References:**

- [Recover from a Failed Linux Kernel Boot — lzwjava](https://lzwjava.github.io/recover-from-a-failed-linux-kernel-boot-en)
- [`mount(8)` — bind mount semantics](https://man7.org/linux/man-pages/man8/mount.8.html)
- [arch-chroot source — the canonical rbind/rslave setup](https://gitlab.archlinux.org/archlinux/arch-install-scripts/-/blob/master/arch-chroot.in)
