---
audio: false
generated: true
image: false
lang: en
layout: post
title: Ventoy Windows 11 USB Plan
translated: false
type: note
---

Everything is ready. Here's the full step-by-step plan:

---

## Full Plan: Ventoy v1.1.17 → Windows 11 USB

### Current State

| Item | Detail |
|---|---|
| **USB device** | `/dev/sdb` (14.6G) |
| **ISO** | `~/Downloads/Win11_25H2_English_x64_v2.iso` (7.9G) |
| **Ventoy** | `/tmp/ventoy-1.1.17/` (extracted) |
| **USB partitions** | Unmounted ✅ |

### ⚠️ This will erase everything on `/dev/sdb`
The current EFI/WIN11 partitions will be destroyed.

### Steps (in order)

| Step | Command |
|---|---|
| **1. Install Ventoy** | `sudo /tmp/ventoy-1.1.17/Ventoy2Disk.sh -i /dev/sdb` |
| **2. Confirm** | Type `y` when prompted |
| **3. Wait for completion** | ~10 seconds |
| **4. Copy ISO** | `cp ~/Downloads/Win11_25H2_English_x64_v2.iso /media/$USER/Ventoy/` |
| **5. Verify** | `ls /media/$USER/Ventoy/` → should show the `.iso` file |
| **6. Sync & eject** | `sync && sudo umount /media/$USER/Ventoy` |

### After Step 4 — Ventoy Features Unlocked

- ✅ **No 4GB FAT32 limit** — Ventoy uses `exFAT` so `install.wim` fits natively
- ✅ **Multi-ISO** — can drop more ISOs (Linux, rescue disks, etc.)
- ✅ **Persistence** — supports persistent storage for Linux ISOs
- ✅ **Legacy + UEFI** — works with both BIOS modes

### For Lenovo Xiaoxin specifically:
After booting from USB → Ventoy menu → select the ISO → if installer doesn't see the SSD, **load Intel RST/VMD driver** during disk selection screen.

---

**Shall I proceed with Step 1 (install Ventoy to `/dev/sdb`)?** This will **wipe the current USB data**.