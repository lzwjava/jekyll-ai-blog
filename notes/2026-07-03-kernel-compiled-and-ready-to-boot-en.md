---
audio: false
generated: true
image: false
lang: en
layout: post
title: Kernel Compiled and Ready to Boot
translated: false
type: note
---

Everything is fully installed. The new kernel is already set as the default boot entry. Let me explain:

---

## What does "compiling the Linux kernel" mean?

The Linux kernel is the **core of the operating system** — it manages hardware (CPU, memory, disks, USB, network), runs programs, and handles security. You just took the **source code** (what you have in `/projects/linux`) and turned it into a **binary** that the computer can actually run.

## What happened step by step

1. **Source code** (C, assembly, headers — 3.0 GB) → **compiler** (GCC) → **binary kernel** (15 MB)
2. The binary was copied to `/boot/vmlinuz-...`
3. An **initramfs** (initial RAM filesystem — drivers needed at boot time) was built → 30 MB
4. **Kernel modules** (drivers compiled as `.ko` files) were installed → `/lib/modules/7.2.0-rc1-...`
5. **GRUB** (the boot menu) was updated — your new kernel is already the **default**

## What can you do with it?

**Reboot into your custom kernel.** On next restart, GRUB will automatically boot **your** compiled kernel instead of the stock Fedora one. You'll see it in the GRUB menu as:
```
Fedora Linux (7.2.0-rc1-00044-g87320be9f0d2) 44 (Workstation Edition)
```

To reboot now:
```bash
sudo reboot
```

## Why would you do this?

| Purpose | What you'd do next |
|---------|-------------------|
| **Learn** how kernel works | Read the source, add printk() debug messages, recompile |
| **Customize** | Edit `.config` — enable/disable drivers, tune performance |
| **Add a feature** | Write a kernel module, patch a subsystem |
| **Test a fix** | Apply a patch, rebuild, reboot and verify |
| **Remove bloat** | Disable drivers you don't need, shrink the kernel |
| **Security hardening** | Enable CONFIG_DEBUG_*, SELinux features, lockdown |

The default `x86_64_defconfig` you built is a **generic** config — it works on almost any x86_64 machine but includes many drivers you may not need. You could trim it down for a faster boot and smaller size.

Want to reboot and try it, or dive deeper into something specific?