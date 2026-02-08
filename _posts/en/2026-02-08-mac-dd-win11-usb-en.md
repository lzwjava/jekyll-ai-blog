---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Mac dd Guide for Win11 USB Boot
translated: false
type: note
---

Question: Suppose I downloaded the ISO Win11_25H2_China_GGK_Chinese_Simplified_x64.iso, how to use Terminal commands (dd) to create a bootable USB disk on a Mac?

Answer: 

**Important warning before starting:**  
The `dd` command is powerful but dangerous — typing the wrong disk identifier will **erase your Mac's internal drive or other important storage**. Double-check everything.  
For modern Windows 11 ISOs (including the China Home edition), the simple `dd` method usually works reliably for creating a bootable USB that most UEFI PCs can boot from, especially in 2025–2026 reports. Some older cases reported issues due to large install.wim files or hybrid ISO quirks, but recent user experiences (including with 25H2 builds) confirm success with direct `dd`.

### Step-by-step using Terminal (dd method)

1. **Insert your USB flash drive**  
   - Use a drive of at least 8 GB (16 GB+ recommended).  
   - **All data on the USB will be completely erased.**

2. **Open Terminal**  
   - Go to Applications → Utilities → Terminal.

3. **Identify the correct disk number of your USB**  
   Run this command:  
   ```
   diskutil list
   ```  
   Look for your USB drive in the list. It usually appears as `/dev/disk2`, `/dev/disk3`, etc. (not `/dev/disk0` or `/dev/disk1`, which are typically your Mac's internal drive).  
   Check the size and name to confirm (e.g., external, ~16 GB).  
   Example output snippet:  
   ```
   /dev/disk3 (external, physical):
      #:                       TYPE NAME                    SIZE       IDENTIFIER
      0:      GUID_partition_scheme                        *15.9 GB    disk3
   ```  
   → Here, use `/dev/disk3` (or whatever matches yours).

4. **Unmount the USB drive** (important — do not skip)  
   Replace `disk3` with your actual number:  
   ```
   diskutil unmountDisk /dev/disk3
   ```

5. **Write the ISO to the USB using dd**  
   Use `/dev/rdiskX` (raw disk) for faster speed on macOS. Replace paths and disk number:  
   ```
   sudo dd if=~/Downloads/Win11_25H2_China_GGK_Chinese_Simplified_x64.iso of=/dev/rdisk3 bs=1m
   ```  
   - `if=` → input file: path to your ISO (drag the file into Terminal to auto-fill the path, or use `~/Downloads/...`).  
   - `of=` → output: `/dev/rdisk3` (use rdisk for speed; rdiskX is the raw version of diskX).  
   - `bs=1m` → block size 1 MB (faster; some use `bs=4m` or `bs=8m`).  
   - You will be asked for your Mac password (sudo).  

   The command shows no progress by default. To see status, press **Ctrl + T** occasionally.  
   It takes 10–30 minutes depending on USB speed and Mac model.

6. **Wait for completion**  
   When finished, you will see output like:  
   ```
   XXXX+0 records in
   XXXX+0 records out
   XXXXXXXX bytes transferred in XXX.XXX secs (XX bytes/sec)
   ```

7. **Eject the USB safely**  
   ```
   diskutil eject /dev/disk3
   ```  
   (Use the original disk number, not rdisk.)  
   Then physically remove the USB.

8. **Test it**  
   Plug the USB into the target PC, enter BIOS/UEFI (usually F2, Del, F12, Esc), set USB as first boot device, enable UEFI mode (disable Legacy/CSM if needed), and boot.  
   The China edition ISO should boot into the Chinese Simplified setup screen.

**Notes and troubleshooting**  
- If the PC does not detect the USB as bootable: Try recreating with `bs=4m`, ensure UEFI boot (not Legacy), disable Secure Boot temporarily, or use a different USB port/drive.  
- The China-specific ISO (GGK edition) behaves the same as standard Windows 11 x64 ISOs for booting — no special differences reported.  
- **Safer alternatives if dd worries you** (GUI, no Terminal risk):  
  - balenaEtcher (free, very popular, works great for Windows ISOs)  
  - WinDiskWriter or similar dedicated tools mentioned in recent guides.  
- For Apple Silicon Macs, Boot Camp Assistant is not available — dd or third-party tools are the main options.

This dd method directly clones the hybrid ISO structure, preserving the EFI boot files needed for Windows 11.

References:  

- [https://www.microsoft.com/zh-cn/software-download/windows11](https://www.microsoft.com/zh-cn/software-download/windows11)  
- [https://superuser.com/questions/1885142/how-to-use-macos-to-create-a-windows-11-usb-installer-flash-drive](https://superuser.com/questions/1885142/how-to-use-macos-to-create-a-windows-11-usb-installer-flash-drive)  
- [https://gist.github.com/acarril/8c15f600cf0397dd61161a470f50f669](https://gist.github.com/acarril/8c15f600cf0397dd61161a470f50f669)  
- [https://www.pugetsystems.com/support/guides/w11-usb-macos](https://www.pugetsystems.com/support/guides/w11-usb-macos)