---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Create Ubuntu Bootable USB on Mac
translated: false
type: note
---

Question: How to use dd to create a bootable Ubuntu disk from ubuntu-24.04.3-desktop-amd64.iso on macOS?

Answer: 

Here is the step-by-step guide to create a bootable USB drive for **Ubuntu 24.04.3 Desktop (amd64)** using the `dd` command on macOS. This method works reliably for both Intel and Apple Silicon Macs when targeting standard PC hardware (BIOS or UEFI).

**Important warnings**
- This process **erases everything** on the selected USB drive.
- Typing the wrong disk identifier can **erase your Mac’s internal drive**. Double-check every step.
- Use at least an 8 GB USB drive (16 GB+ recommended).

### Step-by-step instructions

1. **Insert the USB drive** and close any pop-up windows that appear.

2. **Open Terminal** (found in Applications → Utilities or via Spotlight).

3. **Identify the correct disk number**  
   Run this command:
   ```
   diskutil list
   ```
   Look for your USB drive. It usually appears as `/dev/disk2`, `/dev/disk3`, etc. (not the internal drive, which is typically `/dev/disk0` or `/dev/disk1`).

   Example output snippet:
   ```
   /dev/disk2 (external, physical):
      #:                       TYPE NAME                    SIZE       IDENTIFIER
      0:      GUID_partition_scheme                        *31.9 GB    disk2
      1:                        EFI EFI                     209.7 MB   disk2s1
      2:                  Apple_HFS Untitled                31.7 GB    disk2s2
   ```
   → In this case the whole USB device is **disk2**.

4. **Unmount the USB drive** (replace `diskN` with your number, e.g. `disk2`)
   ```
   diskutil unmountDisk /dev/diskN
   ```
   Example:
   ```
   diskutil unmountDisk /dev/disk2
   ```

   Using the faster raw device path is recommended on macOS:
   ```
   diskutil unmountDisk /dev/disk2
   ```

5. **Write the ISO to the USB drive using `dd`**  
   Use `/dev/rdiskN` (raw device — much faster than `/dev/diskN`).

   Basic safe command (recommended):
   ```
   sudo dd if=~/Downloads/ubuntu-24.04.3-desktop-amd64.iso of=/dev/rdiskN bs=4m status=progress
   ```

   Example (assuming the ISO is in Downloads and USB is disk2):
   ```
   sudo dd if=~/Downloads/ubuntu-24.04.3-desktop-amd64.iso of=/dev/rdisk2 bs=4m status=progress
   ```

   - You will be asked for your admin password (characters won’t show — normal).
   - `status=progress` shows transfer speed and bytes written (macOS Ventura and later support it well).
   - If `status=progress` is not recognized on older macOS, just remove it.

   Alternative variations people use successfully:
   ```
   sudo dd if=~/Downloads/ubuntu-24.04.3-desktop-amd64.iso of=/dev/rdisk2 bs=1m
   ```
   or
   ```
   sudo dd if=~/Downloads/ubuntu-24.04.3-desktop-amd64.iso of=/dev/rdisk2 bs=8m conv=fsync
   ```

6. **Wait for completion**  
   - It usually takes 3–15 minutes depending on USB speed.
   - When finished you’ll see output like:
     ```
     6123+0 records in
     6123+0 records out
     6426255360 bytes transferred in 421.248711 secs (15257012 bytes/sec)
     ```

7. **Ensure all data is written** and eject safely:
   ```
   sync
   diskutil eject /dev/diskN
   ```
   Example:
   ```
   sync
   diskutil eject /dev/disk2
   ```

8. **Remove the USB drive** — it is now bootable.

### Quick verification tip (optional)
After writing, run `diskutil list` again — the USB should now show partitions that match the Ubuntu ISO layout (usually an ISO9660 partition + others).

You can now use this USB to:
- Boot on a standard PC (UEFI or legacy BIOS)
- Try Ubuntu live
- Install Ubuntu

Good luck and triple-check the disk number before pressing Enter on the `dd` command!

References:  

- [https://documentation.ubuntu.com/desktop/en/latest/how-to/create-a-bootable-usb-stick](https://documentation.ubuntu.com/desktop/en/latest/how-to/create-a-bootable-usb-stick)
- [https://osxdaily.com/2015/06/05/copy-iso-to-usb-drive-mac-os-x-command](https://osxdaily.com/2015/06/05/copy-iso-to-usb-drive-mac-os-x-command)
- [https://www.cyberciti.biz/faq/creating-a-bootable-ubuntu-usb-stick-on-a-debian-linux](https://www.cyberciti.biz/faq/creating-a-bootable-ubuntu-usb-stick-on-a-debian-linux)