---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Missing Drivers During Windows Install Fix
translated: false
type: note
---

**Question:** Why can't I find the drivers on my FAT32 USB during Windows installation on Lenovo Xiaoxin 14 IAH8 even after extracting the .exe files?

**Answer:**

This is a very common issue when loading storage drivers (especially Intel RST/IRST or VMD) during Windows setup on modern Lenovo laptops like the Xiaoxin 14 IAH8 (which uses Intel 13th/14th gen or similar Alder Lake/Raptor Lake hardware). The "nothing shows" or no drivers appear when you click **Load driver** → **Browse** usually happens for these reasons:

### Most Likely Causes & Fixes (Step-by-Step)

1. **Wrong folder structure or .inf files buried too deep**
   When you extract a Lenovo/Intel .exe driver package (using 7-Zip or right-click "Extract All"), the actual .inf files are often inside subfolders like:
   - `RST` / `VMD` / `f6flpy-x64` / `Production` / `Win64` / etc.
   Windows setup **only scans the folder you select** and its immediate subfolders — it won't dig deep automatically.

   **Fix:**
   - On another computer, extract the .exe fully.
   - Look for folders containing `.inf` files (especially files named `iaStorAC.inf`, `iaAHCIC.inf`, `VMD.inf`, `iaStorVD.inf`, or similar).
   - Copy **only the folder that contains those .inf files** (or even just the .inf + .sys/.cat files) directly to the root of your FAT32 USB (or into a simple folder like `Drivers` or `IRST`).
   - Avoid nesting too many subfolders (e.g., don't have `USB:\SomeLongPath\Sub\Sub\inf`).
   - During setup: Browse → select the USB drive → open the exact folder with the .inf files → Windows should now list matching drivers → select one (usually the RST or VMD variant) → OK.

2. **Intel VMD (Volume Management Device) is enabled in BIOS — this hides the drive unless using VMD-specific driver**
   Many 12th gen+ Intel Lenovo laptops default to **VMD enabled** (for RAID/Optane support), which makes the NVMe SSD invisible without the correct VMD driver. Standard RST drivers often fail here.

   **Best & Easiest Fix (Recommended for most users):**
   - Restart → enter BIOS (usually press **F2** or **Fn+F2** repeatedly during Lenovo logo).
   - Go to **Configuration** or **Advanced** tab.
   - Find **Intel VMD controller** (or **VMD Setup Menu**, **Intel Volume Management Device**).
   - **Disable** it (set to Disabled).
   - Also check **Storage Mode** / **SATA Configuration** → set to **AHCI** (not RAID or Intel RST Premium).
   - Save & Exit (F10 → Yes).
   - Boot back to Windows USB installer → the SSD should now appear **without loading any driver**!
   (This is the simplest solution for clean Windows installs — you lose RAID if you ever need it, but most home users don't.)

3. **Wrong driver version downloaded**
   - Lenovo's site for IdeaPad Slim 3 14IAH8 may not list a dedicated "F6" (floppy driver) package anymore — many are now .exe only.
   - Try the **latest Intel RST driver** directly from Intel (version 19.x or 20.x for 13th/14th gen):
     Download → <https://www.intel.com/content/www/us/en/download/720755/intel-rapid-storage-technology-driver-installation-software-with-intel-optane-memory.html> (or search "Intel RST VMD driver").
     Extract → look for the VMD folder or f6flpy-x64 equivalent.

4. **USB issues or Windows setup quirks**
   - Make sure the FAT32 USB is plugged into a **USB 2.0 port** if available (some setups ignore USB 3.0 during early boot).
   - Try a different USB stick (some cheap ones have compatibility issues).
   - Ensure the Windows ISO is recent (use Rufus or Microsoft's tool to remake if old).

### Quick Summary Table – What to Try First

| Step | Action | Why It Works |
|------|--------|--------------|
| 1    | Disable Intel VMD in BIOS + set AHCI | Bypasses need for special driver — drives appear natively |
| 2    | Extract .exe → copy only .inf-containing folder to USB root | Windows can now see the driver files |
| 3    | Use Intel's official latest RST/VMD driver package | Lenovo's may be outdated or mismatched |
| 4    | Check BIOS sees the SSD first | Confirms hardware is OK |

After install, install full drivers from Lenovo Vantage or the support site. If VMD was disabled, you can re-enable it later if needed (but reinstall RST software).

This should get your drive showing — the BIOS change fixes it for 80%+ of these cases on similar Lenovo models.

**References:**

- [https://www.youtube.com/watch?v=Sp2AYnGfIOk](https://www.youtube.com/watch?v=Sp2AYnGfIOk)
- [https://www.dell.com/support/kbdoc/en-mq/000188116](https://www.dell.com/support/kbdoc/en-mq/000188116)
- [https://www.intel.com/content/www/us/en/support/articles/000092508/technologies.html](https://www.intel.com/content/www/us/en/support/articles/000092508/technologies.html)
- [https://forums.lenovo.com/t5/ThinkBook-Laptops/Windows-installation-does-not-see-my-hard-drive/m-p/5212595](https://forums.lenovo.com/t5/ThinkBook-Laptops/Windows-installation-does-not-see-my-hard-drive/m-p/5212595)
- [https://www.reddit.com/r/intel/comments/1762sj6/intel_rst_vmd_driver_is_now_an_exe_and_not](https://www.reddit.com/r/intel/comments/1762sj6/intel_rst_vmd_driver_is_now_an_exe_and_not)
