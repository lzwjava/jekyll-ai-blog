---
audio: false
generated: true
image: false
lang: en
layout: post
title: Windows 11 FAT32 USB Setup
translated: false
type: note
---

## ✅ Complete! Here's the Summary

### What Was Done

| Step | Status |
|---|---|
| **1. Formatted USB** (`MS-DOS FAT32` + `GPT`) | ✅ Done |
| **2. Copied all ISO files** (except `install.wim`) | ✅ Done |
| **3. Split `install.wim`** (7.1 GB → 3 FAT32-friendly chunks) | ✅ Done |

### Final USB Structure

```
/Volumes/WIN11/
 ├── autorun.inf
 ├── boot/              ← Windows boot manager
 ├── bootmgfw.efi       ← UEFI bootloader
 ├── bootmgr / bootmgr.efi
 ├── efi/               ← EFI boot files
 ├── setup.exe
 ├── sources/
 │    ├── install.swm   ← 3.2 GB (part 1)
 │    ├── install2.swm  ← 3.7 GB (part 2)
 │    ├── install3.swm  ← 79 MB (part 3)
 │    └── ... (all other source files)
 └── support/
```

**7.9 GB used / 14 GB total** — room to spare.

### How to Use

1. **Eject the USB** safely from Finder (or `diskutil eject /dev/disk13`)
2. **Plug it into your Lenovo Xiaoxin**
3. **Boot** → press `F2` / `F12` (or `Fn+F2`) → select USB as boot device
4. Windows 11 25H2 Setup will load automatically — it recognizes `.swm` files natively

No Etcher needed. No "missing partition table" errors. This is the official Microsoft-compatible UEFI boot method.
