---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Windows 11 Driver Missing Fix Guide
translated: false
type: note
---

Question: I successfully created a bootable USB with dd on macOS, plugged it into the target machine, but during Windows 11 installation I get stuck at the "安装驱动程序以显示硬件" screen with two options: first C, second X, and I don't know which to choose so I can't continue.

Answer: 

The screen you're seeing ("安装驱动程序以显示硬件") is the Chinese-language version of the Windows Setup prompt that appears when the installer cannot detect your storage drives (SSD, NVMe, SATA HDD, etc.). This is a very common issue during Windows 11 installation, especially on newer hardware like recent Intel/AMD platforms, laptops with Intel VMD (Volume Management Device) enabled, RAID configurations, or certain NVMe controllers.

### What the buttons mean (based on standard Windows Setup behavior):
- **First option (C)** → Usually "Continue" or "取消" / "跳过" (skip / proceed without loading a driver).  
  Selecting this often leads to no drives being shown → you can't select where to install Windows → setup fails or loops.

- **Second option (X)** → Usually "Load driver" / "浏览" / "安装驱动程序" (browse to load a driver).  
  This is the correct choice in almost all cases when drives are not visible.

**What you should do right now**:
1. Choose the **second option (X)** — the one for loading / browsing drivers.
2. Windows Setup will open a file browser dialog asking you to select a driver (.inf file).
   - If you have **no additional drivers prepared**, it may show nothing useful or fail → you need to prepare them (see below).
   - If you already have a separate USB with drivers inserted → browse to that USB, navigate to the folder with extracted drivers, select the appropriate .inf file (often named something like "iaStorAC.inf" for Intel RST or similar for AMD), and click OK / Next.

### How to fix it properly (prepare storage drivers)
This prompt almost always means missing **storage controller driver** (SATA/AHCI/NVMe/RAID). The dd method creates a perfect ISO copy, so the USB itself is fine — the issue is hardware-specific.

**Steps to resolve**:
1. **On another computer** (your Mac or any working PC):
   - Go to your target machine's manufacturer website (Dell, HP, Lenovo, ASUS, MSI, Gigabyte, etc.) or motherboard model page.
   - Download the **chipset** + **storage** / **IRST** / **RAID** drivers for Windows 11 (64-bit).
     - Intel platforms: Look for "Intel Rapid Storage Technology" (IRST) or "Intel VMD" driver.
     - AMD platforms: AMD RAID driver or standard chipset drivers.
     - Laptop brands often bundle them in "Chipset" or "Storage" category.
   - Extract the downloaded file (use 7-Zip or similar if it's an .exe) to get the raw driver folder containing .inf files.

2. **Put them on a second USB drive** (FAT32 formatted, separate from your Windows install USB):
   - Copy the extracted driver folder to the root or a subfolder of this second USB.

3. **During installation** (when you see the prompt again):
   - Plug in **both** USBs (Windows one + drivers one).
   - Choose the second option (X / Load driver / Browse).
   - In the browser, select the second USB, go into the driver folder, highlight the correct .inf (try the main storage one first), click OK.
   - Windows should then detect and show your drives → you can continue to select partition and install.

### Quick alternatives if you don't want to hunt drivers
- If your PC is older/standard (pre-2020-ish Intel/AMD), try disabling **Intel VMD** or **RAID mode** in BIOS → set to **AHCI** instead → many times this lets the built-in Windows drivers work without extra loading.
- Recreate the USB with Microsoft's official Media Creation Tool (on a Windows PC) instead of dd — sometimes it injects more compatibility, but dd should be equivalent.
- For very new hardware (e.g., Intel 12th gen+ with VMD, AMD Ryzen 7000/8000/9000), the driver load is almost always required — no way around it without BIOS change.

Once you load the correct driver, the drives appear, and installation proceeds normally. This is **not** a problem with your dd-created USB; it's expected on many modern systems.

References:  

- [https://learn.microsoft.com/en-us/answers/questions/5488804/windows-11-installation-error-install-driver-to-sh](https://learn.microsoft.com/en-us/answers/questions/5488804/windows-11-installation-error-install-driver-to-sh)
- [https://www.elevenforum.com/t/install-driver-to-show-hardware-issue-on-ryzen-cpus-using-bootable-usb-from-win11-media-creation-tool.29536](https://www.elevenforum.com/t/install-driver-to-show-hardware-issue-on-ryzen-cpus-using-bootable-usb-from-win11-media-creation-tool.29536)
- [https://forums.lenovo.com/t5/Lenovo-IdeaPad-1xx-3xx-5xx-7xx-Edge-LaVie-Z-Flex-Laptops/Installation-Windows-11-Install-driver-to-show-hardware/m-p/10002482](https://forums.lenovo.com/t5/Lenovo-IdeaPad-1xx-3xx-5xx-7xx-Edge-LaVie-Z-Flex-Laptops/Installation-Windows-11-Install-driver-to-show-hardware/m-p/10002482)
- Various Reddit threads on r/buildapc and Microsoft communities describing the "install driver to show hardware" prompt and load driver solution