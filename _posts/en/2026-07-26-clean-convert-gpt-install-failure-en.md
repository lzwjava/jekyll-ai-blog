---
audio: false
generated: true
image: false
lang: en
layout: post
title: Clean Convert GPT Install Failure
translated: false
type: note
---

Question: Windows 11 installation failed after doing clean/convert gpt and letting Setup auto-create partitions — need the actual error to diagnose.

Answer: "Installation failed" alone isn't enough to pinpoint the cause — Setup gives a specific error code or message when it fails (usually during the "copying files" or first reboot stage). Common ones on Lenovo Xiaoxin + fresh clean/convert:

- **"Windows cannot be installed to this disk. The selected disk has an MBR partition table..."** → you converted to GPT but BIOS is still set to Legacy/CSM boot instead of UEFI. Fix: enter BIOS (`F2`), set **Boot Mode = UEFI** (not Legacy), disable CSM/Secure Boot compatibility mode if needed.
- **"We couldn't create a new partition or locate an existing one... 0x80300001"** → USB boot media not detected as UEFI, or missing storage driver. Re-flash your Windows 11 USB with Rufus in **GPT + UEFI** mode.
- **Error during file copy, then reboots and fails again** → corrupt USB media (bad flash) or bad ISO. Re-download ISO, re-flash USB.
- **Stuck/fails right after first automatic reboot** → BIOS boot order still pointing to USB instead of the new Windows partition on the internal disk — go into BIOS and set the NVMe/SSD as first boot device (or remove USB and it should proceed).

Can you tell me:
1. The exact error message/code (photo helps if you have one)
2. At what point it failed — during file copy, or after a reboot

That'll tell me exactly which of the above it is.
