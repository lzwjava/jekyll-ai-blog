---
audio: false
generated: true
image: false
lang: en
layout: post
title: Creating Windows USB with Etcher
translated: false
type: note
---

Question: How does the balenaEtcher GUI method create a Windows installation USB from a Mac?

Answer:

[balenaEtcher official website](https://etcher.balena.io?utm_source=chatgpt.com) is a simple graphical tool that writes an ISO image directly to a USB drive.

The idea is:

```
Windows ISO file
        |
        v
   balenaEtcher
        |
        v
 USB flash drive (bootable)
        |
        v
 Lenovo Xiaoxin boots Windows installer
```

Instead of manually formatting the USB, copying files, splitting `install.wim`, etc., Etcher does a raw image write.

---

## 1. Install balenaEtcher on macOS

Download:

[balenaEtcher downloads](https://etcher.balena.io/?utm_source=chatgpt.com)

Choose:

```
macOS Intel
```

for MacBook Pro 2017.

Install:

```
balenaEtcher.app
```

Move it to:

```
Applications
```

---

## 2. Download Windows ISO

Example:

Windows 11 ISO:

[Download Windows 11 Disk Image (ISO)](https://www.microsoft.com/software-download/windows11?utm_source=chatgpt.com)

You get:

```
Win11_24H2_English_x64.iso
```

Size:

```
~6GB
```

---

## 3. Plug USB drive

Use:

```
USB >= 8GB
16GB recommended
```

Check the disk:

```bash
diskutil list
```

Example:

```
/dev/disk2
   external physical
   16GB USB
```

---

## 4. Open Etcher

You see three steps:

```
+-----------------------+
| Flash from file       |
|                       |
|  Win11.iso            |
+-----------------------+

          ↓

+-----------------------+
| Select target         |
|                       |
| USB 16GB              |
+-----------------------+

          ↓

+-----------------------+
| Flash                 |
+-----------------------+
```

Click:

```
Flash from file
```

Select:

```
Win11_24H2_English_x64.iso
```

---

Select USB:

```
SanDisk 16GB USB
```

Then:

```
Flash!
```

---

## 5. What Etcher actually does

Behind the GUI:

```
open ISO
       |
       |
       v
write ISO blocks
       |
       |
       v
USB sectors
```

Equivalent roughly to:

```bash
dd if=windows.iso of=/dev/disk2 bs=4m
```

It creates a bootable USB layout.

---

## 6. Boot Lenovo Xiaoxin

Insert USB.

Power on:

```
Fn + F12
```

or:

```
F12
```

Boot menu:

```
UEFI:
   USB Storage Device
```

Select it.

Windows installer starts.

---

## Important caveat: Windows ISO + Etcher

For Linux ISOs, Etcher is almost perfect.

For Windows ISOs, there is a historical issue:

```
Windows ISO
    |
    +-- install.wim
          |
          +-- sometimes >4GB
```

UEFI firmware usually expects:

```
FAT32
```

but FAT32 cannot store:

```
single file >4GB
```

So some Windows ISOs written by Etcher may not boot on some machines.

For Lenovo Xiaoxin (modern UEFI), success rate is usually good, but if it fails:

* black screen
* "no boot device"
* USB appears but installer does not start

then use the `wimlib` FAT32 method.

---

For your case:

```
MacBook Pro 2017
        |
        | create USB
        v
Lenovo Xiaoxin
        |
        v
Windows 11
```

I would try **Etcher first** because it takes ~10 minutes. If Lenovo cannot boot it, switch to the `wimlib` method.
