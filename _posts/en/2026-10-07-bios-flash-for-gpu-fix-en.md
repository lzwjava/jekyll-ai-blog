---
audio: false
generated: true
image: false
lang: en
layout: post
title: BIOS Flash for GPU Fix
translated: false
type: note
---

The BIOS file is on the remote machine and verified (md5 `611b0eb7e20d4c489a0d9195352170df` matches, 16MB).

Here's the plan to flash it and finish the GPU fix:

## Step 1 — Get the BIOS file onto a USB stick

**Easiest way:** plug a **FAT32 USB stick** into the Debian machine, then tell me. I'll mount it, copy `~/E7978IMS.AA0` onto it, and safely unmount it — all remotely.

(Or copy `E7978IMS.AA0` to a USB stick yourself using the desktop file manager.)

## Step 2 — Flash with M-Flash

1. Reboot, tap **DEL** to enter BIOS (Click BIOS 5).
2. Click **M-FLASH** (bottom row button; or in Advanced mode F7 → it's in the left menu / "Utilities").
3. The system reboots into flash mode.
4. Choose **"Select one file to update BIOS"**.
5. Browse to your USB stick → select **`E7978IMS.AA0`**.
6. Confirm **Yes**. ⚠️ **Do NOT power off or reset during the flash** (takes ~1–2 min).
7. It reboots automatically.

## Step 3 — Enable "Above 4G Decoding"

After flashing, BIOS settings reset to defaults. Enter BIOS again (DEL):

1. Press **F7** for Advanced mode.
2. Go to **Settings → Advanced → PCI Subsystem Settings** (or "PCIe/PCI Subsystem").
3. **"Above 4G Decoding" → Enabled**.
4. **F10 → Save & Exit**.

## Step 4 — Verify

Boot into Debian and tell me — I'll check the BARs and run `nvidia-smi`. The driver (550.163.01) is already installed and ready.

---

⚠️ **Important notes:**

- BIOS flashing carries a small risk. Make sure power is stable and don't interrupt it.
- After the flash, if the option still isn't there, we'll check the exact menu path together — but the A.A release notes ("Support multi graphic cards") indicate it's there.

Do you have a USB stick handy? If you plug it into the Debian machine, I'll copy the file onto it for you.
