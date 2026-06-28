---
audio: false
generated: true
image: false
lang: en
layout: post
title: Ready to flash Fedora
translated: false
type: note
---

The USB is `/dev/disk13` — same 15.7 GB drive. Here's what's on it:

```
disk13s128  Bios Boot Partition     245 KB    (GRUB bootloader)
disk13s1    Linux Filesystem       16.8 MB   (likely OpenWrt kernel)
disk13s2    Linux Filesystem       109 MB    (likely OpenWrt rootfs)
(free space)                       15.6 GB   (unused)
```

This looks like an **OpenWrt firmware image** flashed via `dd` — tiny kernel + rootfs partitions, rest empty. Not useful for the MacBook.

**Ready to flash Fedora. Commands:**

```bash
# Unmount the USB
diskutil unmountDisk /dev/disk13

# Flash Fedora ISO (this erases everything on the USB)
sudo dd if=/Users/lzwjava/Downloads/Fedora-Workstation-Live-44-1.7.x86_64.iso of=/dev/rdisk13 bs=4m status=progress

# Eject when done
diskutil eject /dev/disk13
```

Want me to run these now?
