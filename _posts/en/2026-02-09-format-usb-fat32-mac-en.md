---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Format USB as FAT32 on Mac
translated: false
type: note
---

**Question:** How to format a USB drive (U-disk) as FAT32 on macOS when only APFS and exFAT are shown in Disk Utility?

**Answer:**

macOS **Disk Utility** no longer shows FAT32 (MS-DOS FAT) as a direct option in the modern macOS versions (especially Ventura and later), but you can still easily format a USB drive as **FAT32** using one of these reliable methods:

### Method 1 – Recommended (Easiest & Safest) – Use Disk Utility with MS-DOS (FAT)

1. Plug in your USB drive
2. Open **Disk Utility** (Applications → Utilities → Disk Utility)
3. In the left sidebar, **select your USB drive** (click the top-level device, not the indented volume)
4. Click **Erase** at the top
5. Set the following options:
   - **Name**: whatever you want
   - **Format**: Choose **MS-DOS (FAT)**
     → This is the real name for FAT32 on macOS
   - **Scheme**: **Master Boot Record** (MBR) ← very important for maximum compatibility!
6. Click **Erase**

→ Done! Your USB is now formatted **FAT32** with excellent cross-platform compatibility (Windows, macOS, Linux, TVs, cameras, car stereos, etc.).

### Method 2 – Terminal (when MS-DOS (FAT) is still not showing or you want more control)

```bash
# 1. Find your USB drive identifier
diskutil list

# Look for your USB drive (example: /dev/disk3 or /dev/disk4)
# Be VERY careful — wrong disk = data loss on your main drive!

# 2. Unmount the disk (replace disk3 with your actual identifier)
diskutil unmountDisk /dev/disk3

# 3. Format as FAT32 (4096 byte cluster size is default and fine)
sudo diskutil eraseDisk FAT32 MYUSB MBRFormat /dev/disk3
```

Replace:

- `MYUSB` → your desired volume name (no spaces, max 11 characters)
- `/dev/disk3` → your actual USB disk identifier

### Quick Comparison Table – What to choose in 2025/2026

| Format       | Max File Size | Max Volume Size | macOS Write | Windows Write | Best For                              |
|--------------|---------------|------------------|-------------|---------------|---------------------------------------|
| **FAT32**    | 4 GB          | 2 TB (practical) | Yes         | Yes           | USB sticks for TVs/cameras/cars       |
| **exFAT**    | Very large    | Very large       | Yes         | Yes           | Large files (>4GB) cross-platform     |
| **APFS**     | Very large    | Very large       | Yes         | No*           | Mac-only modern drives                |

*Windows can read APFS with third-party software (Paragon, etc.)

**Bottom line (2026 recommendation):**

- Need max compatibility with old devices → **FAT32** (use Method 1)
- Need files > 4 GB → **exFAT** (native & easiest)
- Only use on Mac → **APFS**

Most people still choose **exFAT** today unless they specifically need compatibility with very old devices that refuse exFAT.

Good luck!
