---
audio: false
generated: true
image: false
lang: en
layout: post
title: Windows 11 25H2 Bootable USB Created
translated: false
type: note
---

## Summary — Windows 11 25H2 Bootable USB Created ✅

### The Problem
`Win11_25H2_English_x64_v2.iso` is a **DVD image** (ISO9660), not a raw disk image. Etcher expects a partition table inside the image (like Ubuntu ISOs), so it errors with *"missing partition table"*. Even if you bypass it, the 7.1 GB `install.wim` exceeds FAT32's 4 GB file limit — the USB won't boot.

### What We Did

| # | Action | Command / Tool |
|---|---|---|
| 1 | **Analyzed** the ISO and USB | `diskutil list`, `hdiutil imageinfo`, verified `install.wim` is 7.1 GB |
| 2 | **Formatted** the 15.7 GB USB as FAT32 with GPT | `diskutil eraseDisk MS-DOS WIN11 GPT /dev/disk13` |
| 3 | **Copied** all files from ISO to USB (excluding `install.wim`) | `rsync -av --exclude='sources/install.wim'` |
| 4 | **Split** the 7.1 GB `install.wim` into 3 FAT32-safe chunks (`.swm` files) | `wimlib-imagex split ... 3800` |

### Final USB Drive `/Volumes/WIN11`

- **File system:** FAT32 + GPT
- **Size:** 7.9 GB used / 14 GB total
- **Structure:** `boot/`, `efi/`, `sources/`, `setup.exe`, `support/`
- **Install files:** `install.swm` (3.2 GB) + `install2.swm` (3.7 GB) + `install3.swm` (79 MB)

This is the **official Microsoft-compatible method** for UEFI Windows installation media. The USB was safely ejected and is ready to boot the **Lenovo Xiaoxin**.
