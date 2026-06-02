---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Check USB Format on macOS
translated: false
type: note
---

Question: In macOS, how to know what format a USB disk is (FAT32 or others)?

Answer:

Here are the easiest ways to check the file system format (such as FAT32, exFAT, APFS, Mac OS Extended, NTFS, etc.) of a USB drive on macOS:

### Method 1: Using Finder (Quickest – Recommended)

1. Plug in your USB drive.
2. Open **Finder**.
3. In the sidebar, locate your USB drive (it usually appears under "Locations").
4. Right-click (or Control-click) the USB drive name.
5. Choose **Get Info**.
6. In the Info window, look for the line labeled **Format** (near the top, under General).
   - You will see something like:
     - **MS-DOS (FAT32)** → This is FAT32
     - **ExFAT** → Modern large-file compatible format
     - **Mac OS Extended (Journaled)** → Also called HFS+
     - **APFS**
     - **Windows (NTFS)**
     - etc.

This method works on any recent macOS version and is the fastest for most users.

### Method 2: Using Disk Utility (More detailed view)

1. Plug in your USB drive.
2. Open **Disk Utility**:
   - Go to Applications → Utilities → Disk Utility
   - Or use Spotlight (Cmd + Space) and type "Disk Utility"
3. In the left sidebar, select your USB drive (click the actual device name, not just the volume — if you don't see the full device list, go to menu **View → Show All Devices**).
4. Look at the information shown in the main area:
   - You will see **Format** or **File System** listed clearly (e.g., "MS-DOS (FAT32)", "ExFAT", "APFS", etc.).
   - You can also click the **Info** button (i icon) at the top for more details.

### Method 3: Using Terminal (For command-line users)

1. Open **Terminal** (Applications → Utilities → Terminal).
2. Run this command to list all disks:

   ```
   diskutil list
   ```

   → Find your USB drive (usually something like `/dev/disk2` or `/dev/disk3` — look at the size and name to identify it).
3. Then run (replace `disk3` with your actual disk number):

   ```
   diskutil info disk3s1
   ```

   (use the partition like `diskXs1` or `diskXs2` that corresponds to the volume)
   → Look for the line **File System Personality** or **Type (Bundle)** — it will show FAT32, ExFAT, Journaled HFS+, APFS, etc.

**Quick tip**: FAT32 usually appears as **MS-DOS (FAT32)** in macOS. If you see just "MS-DOS (FAT)", it's the older 16-bit FAT (rare on modern USB drives).

These methods work on macOS Ventura, Sonoma, Sequoia, and earlier versions.

References:

- [How to Determine File System of a Drive on Mac - OS X Daily](https://osxdaily.com/2023/01/30/how-to-determine-file-system-of-a-drive-on-mac)
- [Server Fault - How do I identify the file system of a drive in Mac OS?](https://serverfault.com/questions/276091/how-do-i-identify-the-file-system-of-a-drive-in-mac-os)
