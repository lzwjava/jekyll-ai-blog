---
audio: false
generated: true
image: false
lang: en
layout: post
title: BIOS Update and GPU Fix
translated: false
type: note
---

✅ USB disk is ready. Here's what I did:

| Step | Result |
|---|---|
| Wiped Debian installer image | ✅ |
| Created MBR + single FAT32 partition (`/dev/sdb1`) | ✅ label `USB`, 4GB |
| Copied BIOS file | ✅ `E7978IMS.AA0` (16MB) |
| Safely unmounted | ✅ |

**The USB is now safe to unplug** (it's already unmounted).

## Now flash the BIOS

1. **Unplug the USB** from the Debian machine (it's unmounted, safe to remove).
2. **Reboot** the machine and tap **DEL** to enter BIOS.
3. In BIOS, click **M-FLASH** (bottom row button in Click BIOS 5, or press F7 for Advanced mode → it's in the left column / "Utilities").
4. The system will reboot into M-Flash mode.
5. Select **"Select one file to update BIOS"**.
6. Choose your USB drive → select **`E7978IMS.AA0`**.
7. Confirm **Yes**. ⚠️ **Do not power off or interrupt** — wait for it to finish (~1–2 min) and reboot on its own.

## Then enable the GPU fix

After flashing, enter BIOS again (DEL):

1. **F7** → Advanced mode.
2. **Settings → Advanced → PCI Subsystem Settings** (or similar).
3. **"Above 4G Decoding" → Enabled**.
4. **F10** → Save & Exit.

## Finally

Boot into Debian and tell me — I'll verify the BARs are now assigned and run `nvidia-smi` to confirm the Tesla M40 is working.

Good luck with the flash — and remember: **don't interrupt the BIOS update**. Let me know when you're done and I'll take it from there. 🚀
