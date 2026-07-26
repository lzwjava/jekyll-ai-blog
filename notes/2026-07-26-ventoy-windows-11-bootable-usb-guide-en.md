---
audio: false
generated: true
image: false
lang: en
layout: post
title: Ventoy Windows 11 Bootable USB Guide
translated: false
type: note
---

## Comprehensive Summary: Windows 11 Bootable USB — Ventoy Method

### 1. Environment Analysis

First, I scanned the system to understand what we were working with:

| Check | Result |
| --- | --- |
| **USB device** | `/dev/sdb` — 14.6G USB disk detected |
| **Existing partitions** | `/dev/sdb1` (200M, VFAT, EFI) + `/dev/sdb2` (14.5G, VFAT, WIN11) |
| **Existing content** | A Windows 11 installer was **already present** — made via manual FAT32 + `wimsplit` (Method 3) |
| **ISO file** | `~/Downloads/Win11_25H2_English_x64_v2.iso` (7.9G) |
| **Ventoy installed?** | **No** — not on the system |

### 2. Decision: Why We Used Ventoy Anyway

The existing USB was already bootable (EFI partition + split `install.swm` files). However, the user explicitly requested Ventoy. Key advantages of re-doing it with Ventoy:

- **No 4GB FAT32 limit** — Ventoy uses exFAT, so `install.wim` stays intact (no splitting needed)
- **Multi-ISO support** — can drop Linux ISOs alongside Windows later
- **Easier updates** — just replace the ISO file, no repartitioning
- **Better compatibility** — Ventoy handles both Legacy BIOS and UEFI

### 3. Steps Executed

| Step | What I Did | Command |
| --- | --- | --- |
| **A** | Downloaded Ventoy v1.1.17 | `wget https://github.com/ventoy/Ventoy/releases/download/v1.1.17/ventoy-1.1.17-linux.tar.gz` |
| **B** | Extracted the tarball | `tar xzf ventoy-1.1.17-linux.tar.gz` |
| **C** | Unmounted old USB partitions | `sudo umount /dev/sdb1 /dev/sdb2` |
| **D** | Installed Ventoy to `/dev/sdb` | `printf 'y\ny\n' \| sudo ./Ventoy2Disk.sh -i /dev/sdb` |
| **E** | Mounted new Ventoy partition | System auto-mounted `/dev/sdb1` at `/mnt` |
| **F** | Copied Windows 11 ISO | `sudo cp ~/Downloads/Win11_25H2_English_x64_v2.iso /mnt/` |
| **G** | Synced and unmounted | `sync && sudo umount /mnt` |
| **H** | Powered off the USB | `udisksctl power-off -b /dev/sdb` |

### 4. What Ventoy Did Internally

During step D, Ventoy:

1. **Wiped** the entire disk (`dd if=/dev/zero ...`)
2. **Created 2 partitions**:
   - `/dev/sdb1` (14.6G, exFAT, label `Ventoy`) — for storing ISO files
   - `/dev/sdb2` (32M, vfat, label `VTOYEFI`) — EFI bootloader partition
3. **Installed its custom bootloader** — written to the MBR and the EFI partition
4. **Wrote Ventoy's core disk image** — containing the boot menu engine

### 5. Final USB Layout

| Partition | Size | Filesystem | Label | Role |
| --- | --- | --- | --- | --- |
| `/dev/sdb1` | 14.6G | **exFAT** | `Ventoy` | ISO storage (holds `Win11_25H2_English_x64_v2.iso` at 7.9G) |
| `/dev/sdb2` | 32M | **vfat** | `VTOYEFI` | EFI bootloader |

**Total used**: 7.9G / 15G (53%) — plenty of room for more ISOs.

### 6. How Booting Works

When you boot from this USB:

1. **UEFI firmware** loads `VTOYEFI` partition → Ventoy's EFI bootloader starts
2. Ventoy scans `/dev/sdb1` for `.iso` files
3. **Boot menu** displays `Win11_25H2_English_x64_v2.iso`
4. You select it → Ventoy **creates a virtual BIOS/UEFI environment** and boots the Windows installer directly from the ISO
5. Windows installer sees a normal boot environment and proceeds with installation

### 7. Critical Note for Lenovo Xiaoxin

If Windows installer **doesn't detect the NVMe SSD**, it's an Intel VMD/RST driver issue — not a USB problem. Solution:

- Download Intel RST F6 driver on another machine
- Put it on a separate USB
- At disk selection → **Load Driver** → browse to driver folder → SSD appears
