---
audio: false
generated: true
image: false
lang: en
layout: post
title: Chinese PE Boot Disk Tools
translated: false
type: note
---

Question: **What are “SGI / 分区工具 / USB3 / SRS / CEO / MSX” tools seen on Chinese Windows installation USB disks? What kind of bootable disk contains them?**

Answer:

Those names are usually from **Chinese PE (Preinstallation Environment) boot disks**, not from Microsoft's official Windows installer.

A typical Chinese “装机盘” (system installation USB) is actually a **WinPE rescue environment + Windows ISO/image deployment toolkit**. When you boot it, you enter a mini Windows system with tools like:

```
WinPE
 ├── Disk partition tools
 │    ├── DiskGenius (DG)
 │    ├── 傲梅分区助手
 │    └── 分区工具
 │
 ├── System deployment
 │    ├── SGI
 │    ├── GImageX / DISM
 │    └── Ghost
 │
 ├── Driver tools
 │    ├── USB3 driver
 │    ├── SRS driver
 │    └── Intel RST/VMD driver
 │
 └── Hardware tools
      ├── CPU-Z
      ├── memory test
      └── disk health check
```

### SGI

Most likely:

**SGI = 系统安装工具 / 系统备份还原工具**

In Chinese PE communities, SGI usually refers to a **Ghost-like image backup/restore tool**.

Typical workflow:

```
Windows.wim / .gho image
        |
        v
SGI restore
        |
        v
write system partition
        |
        v
install bootloader
```

It is common in OEM repair shops.

---

### 分区工具

Just means:

```
Partition tool
```

Used to:

* delete old partitions
* convert MBR ↔ GPT
* create EFI partition
* create MSR partition
* format NTFS

Example:

```
Disk 0

GPT:

EFI       100MB   FAT32
MSR       16MB
Windows   500GB   NTFS
Recovery 1GB
```

---

### USB3

Usually a **USB 3.0 driver package**.

Old Windows PE images sometimes cannot see:

* USB 3 controllers
* NVMe SSD
* newer Intel platforms

So PE includes:

```
USB3_x64.sys
iusb3hub.sys
iusb3xhc.sys
```

---

### SRS

Usually:

```
SRS = Storage Rapid Storage
```

Meaning:

**Intel Rapid Storage Technology driver**

Modern Lenovo laptops often need this.

Example:

Lenovo Xiaoxin:

```
BIOS:
Intel VMD = ON

Windows Setup:
No disk detected

Solution:
Load SRS driver
   ↓
iaStorVD.inf
   ↓
SSD appears
```

This is the same family as Intel RST/VMD.

---

### CEO / MSX

These are probably PE vendor-specific names.

Common Chinese PE distributions include:

* 微PE (WePE)
* 优启通 (EasyU)
* 老毛桃
* 大白菜
* IT天空 U盘维护系统

They bundle their own:

```
CEO
MSX
SGI
onekey
```

tools.

They are not Windows components.

---

## What bootable USB contains these?

Usually:

### 1. Chinese WinPE USB

Examples:

* 微PE工具箱
* 优启通
* 老毛桃
* 大白菜

Boot menu:

```
UEFI USB
 |
 v
WinPE
 |
 +-- SGI备份还原
 +-- 分区工具
 +-- 驱动安装
 +-- 一键装机
```

---

### 2. OEM factory recovery USB

Lenovo/Dell repair disks may also contain:

```
PE
+
drivers
+
factory image
+
deployment scripts
```

---

### 3. Your normal Microsoft Windows 11 USB does NOT contain these

Official ISO:

```
boot.wim
install.wim
setup.exe
efi/
sources/
```

No:

```
SGI
SRS
CEO
MSX
```

---

For your Lenovo Xiaoxin 14 case, the useful part is likely **SRS/Intel VMD driver**, not SGI. If Windows 11 setup sees:

```
Disk 0 512GB SSD
```

then storage detection is already working. The failure at 75% is more likely:

* corrupted install media
* wrong edition/image
* driver mismatch
* partition/boot mode issue

not missing SGI tools.