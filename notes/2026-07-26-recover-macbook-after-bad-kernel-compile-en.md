---
audio: false
generated: true
image: false
lang: en
layout: post
title: Recover MacBook after bad kernel compile
translated: false
type: note
---

Question: MacBook Pro 2017 running Ubuntu cannot boot after compiling a Linux kernel. How to recover?

Answer:

Yes, this is a common situation. A **MacBook Pro 2017 (Intel)** can run Ubuntu, but after manually compiling a kernel, a bad kernel configuration or missing Apple-specific drivers can make it fail to boot.

The good news: your data is probably still there. You mainly need to boot an older kernel or repair GRUB.

## 1. First try GRUB recovery

Power on the MacBook and immediately hold:

```
Option (⌥) key
```

You should see Apple's boot picker.

Choose:

```
EFI Boot
```

Then in GRUB:

Press:

```
Esc
```

or hold:

```
Shift
```

You should see:

```
Ubuntu
Advanced options for Ubuntu
```

Select:

```
Advanced options for Ubuntu
```

Then choose the previous kernel:

Example:

```
Ubuntu, with Linux 6.8.0-xx-generic
Ubuntu, with Linux 6.8.0-xx-generic (recovery mode)
Ubuntu, with Linux 6.6.x
```

Boot the older one.

---

## 2. If you can boot the old kernel

Check installed kernels:

```bash
dpkg --list | grep linux-image
```

Example:

```
linux-image-6.8.0-40-generic
linux-image-6.8.0-custom
```

Remove the broken kernel:

```bash
sudo apt remove linux-image-6.8.0-custom
sudo update-grub
```

---

## 3. If no kernel boots: use Ubuntu live USB

Boot from USB:

```
Power on
hold Option (⌥)
select EFI Boot
```

Mount your Ubuntu partition:

```bash
sudo fdisk -l
```

Example:

```
/dev/nvme0n1p2   Linux filesystem
```

Mount:

```bash
sudo mount /dev/nvme0n1p2 /mnt
```

Mount EFI:

```bash
sudo mount /dev/nvme0n1p1 /mnt/boot/efi
```

Enter your system:

```bash
sudo chroot /mnt
```

Then:

```bash
update-grub
```

or reinstall kernel:

```bash
apt install --reinstall linux-image-generic linux-headers-generic
```

Exit:

```bash
exit
sudo reboot
```

---

## 4. Why compiling kernel breaks MacBook Pro boot

MacBook Pro 2017 hardware needs several kernel options:

Important:

```
CONFIG_EFI=y
CONFIG_EFI_STUB=y

CONFIG_NVME_CORE=y
CONFIG_NVME=y

CONFIG_HID_APPLE=y
CONFIG_BCM5974=y

CONFIG_DRM_AMDGPU=y   (if Radeon Pro model)
CONFIG_DRM_I915=y     (Intel graphics)
```

Common mistakes:

### Missing EFI support

The Mac boots through EFI:

```
Mac EFI firmware
        |
        v
Linux EFI stub
        |
        v
Kernel
```

If:

```
CONFIG_EFI_STUB=n
```

the Mac cannot start the kernel.

---

### Missing NVMe driver

The SSD needs:

```
CONFIG_NVME_CORE
CONFIG_BLK_DEV_NVME
```

Otherwise:

```
Kernel starts
        |
        X
cannot find root filesystem
```

---

### Wrong initramfs

After installing your custom kernel:

```bash
sudo update-initramfs -c -k <kernel-version>
sudo update-grub
```

Without initramfs, drivers needed before mounting `/` may be missing.

---

## 5. For future kernel compilation

On Ubuntu, start from the current config:

```bash
cp /boot/config-$(uname -r) .config
```

Then:

```bash
make olddefconfig
make -j$(nproc)
sudo make modules_install
sudo make install
sudo update-grub
```

This keeps Apple-required options.

---

The key question is: **what exactly happens when you boot now?**

Examples:

1. Black screen immediately?
2. GRUB appears but kernel says `unable to mount root fs`?
3. Kernel panic?
4. Stuck at Apple logo?
5. Drops into `initramfs` shell?

Also tell me the exact MacBook Pro 2017 model:

* 13-inch Intel only?
* 15-inch with Radeon Pro GPU?
* Ubuntu version?
* Kernel version you compiled?
