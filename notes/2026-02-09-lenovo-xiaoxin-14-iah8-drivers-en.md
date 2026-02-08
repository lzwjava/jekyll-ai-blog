---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Lenovo Xiaoxin 14 IAH8 Driver Guide
translated: false
type: note
---

Question: My Lenovo Xiaoxin 14 IAH8 laptop — where can I download the drivers?

Answer: 

The **Lenovo Xiaoxin 14 IAH8** is the Chinese-market version of the global **IdeaPad Slim 3 14IAH8** (or very similar to IdeaPad Slim 5 14IAH8 in some configurations). Lenovo provides official drivers for this model on their support sites.

### Recommended ways to download drivers (official & safest)

1. **Use the Chinese Lenovo support site (recommended for Xiaoxin models)**  
   - Go to: https://newsupport.lenovo.com.cn/  
   - Or directly to the driver download page: https://newsupport.lenovo.com.cn/driveDownloads_index.html  
   - Options:  
     - Enter your machine's **主机编号** (S/N or serial number, usually starts with PF, R0, etc., found on the bottom sticker or in BIOS). This gives the most accurate, pre-matched drivers.  
     - Or select the model manually if you know the exact MT (machine type) like "Lenovo Xiaoxin 14 IAH8" or search under IdeaPad series.  
   - Download the "联想驱动管理" (Lenovo Driver Management) tool — it's an official one-click installer that detects your hardware and downloads/installs everything needed (chipset, storage, graphics, audio, etc.).  
   - For storage/NVMe drivers (important for your Windows install issue): Look under Chipset, Storage, or IRST/Intel RST categories after selecting Windows 11.

2. **Global Lenovo support site (works for most Xiaoxin = IdeaPad equivalents)**  
   - Go to: https://pcsupport.lenovo.com/  
   - Search for or select: **IdeaPad Slim 3 14IAH8** (this is the international equivalent).  
   - Direct link example: https://pcsupport.lenovo.com/us/en/products/laptops-and-netbooks/ideapad-s-series-netbooks/ideapad-slim-3-14iah8/downloads  
   - Click **Drivers & Software** → **Manual Update** → Select Windows 11 (64-bit) → Download categories like:  
     - Chipset  
     - Storage (Intel RST / VMD / NVMe if listed)  
     - Graphics (Intel UHD/Iris)  
     - Audio, WLAN, etc.  
   - Extract any .exe files (use 7-Zip if needed) to get the raw .inf drivers for loading during Windows Setup.

### For your specific Windows installation storage driver issue
- The prompt "安装驱动程序以显示硬件" is almost always due to missing **Intel RST (Rapid Storage Technology)** or **VMD** driver (common on Intel 12th–14th gen or newer platforms like yours).  
- Download the **Intel RST driver** package from the above sites (search for "Intel Rapid Storage" or "IRST" in the driver list).  
- Extract it to a separate FAT32 USB.  
- During setup → choose the second option (X / Load driver) → browse to the extracted folder → select the .inf file (often iaStorAC.inf or similar).

### Extra tips
- If the site asks for OS → choose **Windows 11 64-bit**.  
- Avoid third-party sites like DriverHub unless official ones fail — they can bundle unwanted software.  
- After installation, run Windows Update + Lenovo Vantage (if it installs) for remaining drivers.  
- If you have the exact serial number, use that on newsupport.lenovo.com.cn for perfect match.

This should resolve the driver loading during install and get all hardware working post-install.

References:  

- [https://pcsupport.lenovo.com/us/en/products/laptops-and-netbooks/ideapad-s-series-netbooks/ideapad-slim-3-14iah8/downloads](https://pcsupport.lenovo.com/us/en/products/laptops-and-netbooks/ideapad-s-series-netbooks/ideapad-slim-3-14iah8/downloads)
- [https://newsupport.lenovo.com.cn/driveDownloads_index.html](https://newsupport.lenovo.com.cn/driveDownloads_index.html)
- [https://psref.lenovo.com/Product/IdeaPad/IdeaPad_Slim_3_14IAH8](https://psref.lenovo.com/Product/IdeaPad/IdeaPad_Slim_3_14IAH8)