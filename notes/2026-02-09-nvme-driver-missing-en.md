---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Missing NVMe Driver for Windows Setup
translated: false
type: note
---

**Question:** Why can't Windows find/load any drivers from my FAT32 USB with these extracted Lenovo driver .exe files (like chipset-KZSC030FLWDYANE0.exe, intelVGA-KZSG0A0FT22GJNE0.exe, etc.) plugged in during installation on Lenovo Xiaoxin 14 IAH8?

**Answer:**

The main problem is that **none of the .exe files you listed** (from ~/Downloads/driver) contain the **storage/NVMe/Intel RST/VMD drivers** needed for Windows setup to detect your SSD. Those files are for other hardware:

- chipset-KZSC030FLWDYANE0.exe → Chipset drivers (post-install)
- intelVGA-KZSG0A0FT22GJNE0.exe → Intel Graphics
- audio-KZSA050F2QF1NNE0.exe → Audio
- camera-KZSD040FAVJPUNE0.exe → Camera
- fingerprint-KZSD030F36UBVNE0.exe → Fingerprint
- RTKwlan-KZSW060F0H46SNE0.exe → WiFi (Realtek)
- etc.

None are the **Intel Rapid Storage Technology (IRST/RST)** or **VMD** package that provides the .inf files (like iaStorAC.inf, iaStorVD.inf, or VMD.inf) required during the "Load driver" step when the SSD isn't visible.

### Why Nothing Shows Up When You Browse the USB
Even if you copied these .exe files to the FAT32 USB:
- Windows setup **cannot run .exe installers** — it only looks for raw driver files (.inf + .sys + .cat).
- You must **extract** the correct RST .exe first (on another PC), find the subfolder with .inf files (often in `f6flpy-x64`, `VMD`, `Production`, or `Win64`), and copy **only that folder** (or its contents) to the USB root or a simple folder like `\IRST`.
- Your current files don't have those storage .inf files, so browsing shows nothing compatible → "no drivers found" or empty list.

### Recommended Fix: Two Paths (Choose One)

**Path 1: Easiest & Most Reliable – Disable VMD in BIOS (No Driver Needed)**
- Restart laptop → press **F2** (or Fn+F2) repeatedly at Lenovo logo to enter BIOS.
- Go to **Configuration** tab (or **Advanced** / **Device Configuration**).
- Look for:
  - **Intel VMD controller** / **VMD Setup Menu** / **Intel Volume Management Device** → set to **Disabled**.
  - **SATA Controller Mode** / **Storage Mode** → set to **AHCI** (not RAID or RST).
- **F10** → Save & Exit → Yes.
- Boot back to Windows USB installer → SSD should now appear automatically in the drive list (no "Load driver" needed).
- This works because VMD hides the NVMe SSD from standard Windows setup unless the special VMD driver is loaded. Disabling it uses native AHCI/NVMe mode (fine for most users, loses RAID if you ever need it).

**Path 2: Keep VMD Enabled – Load Proper RST/VMD Driver**
1. On another Windows PC, download the **latest Intel RST driver** (includes VMD support for 13th/14th gen):
   - From Intel: https://www.intel.com/content/www/us/en/download/720755/intel-rapid-storage-technology-driver-installation-software-with-intel-optane-memory.html (or search "Intel RST driver VMD").
   - Or from Lenovo global for IdeaPad Slim 3 14IAH8 (equivalent model): Check under Storage/Chipset on https://pcsupport.lenovo.com → search "IdeaPad Slim 3 14IAH8" → Drivers → Storage → Intel Rapid Storage Technology.
2. Run the .exe with command to extract (open Command Prompt in the download folder):
   ```
   SetupRST.exe -extractdrivers C:\ExtractedRST
   ```
   (Or use 7-Zip to extract if -extractdrivers doesn't work.)
3. In the extracted folder, find subfolder with .inf files (e.g., `f6flpy-x64`, `VMD`, `Drivers\VMD`).
   - Common files: iaStorVD.inf, iaStorAC.inf, VMD.inf.
4. Copy that entire subfolder (or just the .inf/.sys/.cat files) to FAT32 USB root (e.g., USB:\VMD\ or USB:\IRST\\).
5. During Windows setup:
   - At "Where do you want to install Windows?" → **Load driver** → **Browse** → select USB → open the folder with .inf → select the matching driver (try VMD or RST variants) → OK.
   - SSD should appear after loading.

After install (either path), run Lenovo Vantage + Windows Update for full drivers (including the ones you already have).

Try **Path 1 first** — BIOS disable fixes this instantly for most Lenovo IdeaPad/Slim models with Intel 13th/14th gen in 2026.

**References:**

- [https://www.youtube.com/watch?v=Sp2AYnGfIOk](https://www.youtube.com/watch?v=Sp2AYnGfIOk)
- [https://www.intel.com/content/www/us/en/support/articles/000092508/technologies.html](https://www.intel.com/content/www/us/en/support/articles/000092508/technologies.html)
- [https://www.youtube.com/watch?v=41C71-dvv-4](https://www.youtube.com/watch?v=41C71-dvv-4)
- [https://www.reddit.com/r/intel/comments/1762sj6/intel_rst_vmd_driver_is_now_an_exe_and_not](https://www.reddit.com/r/intel/comments/1762sj6/intel_rst_vmd_driver_is_now_an_exe_and_not)
- [https://support.lenovo.com/us/en/solutions/ht506197-nvme-ssd-pci-device-will-be-invisible-when-intel-vmd-is-enabled-lenovo-thinksystem](https://support.lenovo.com/us/en/solutions/ht506197-nvme-ssd-pci-device-will-be-invisible-when-intel-vmd-is-enabled-lenovo-thinksystem)
