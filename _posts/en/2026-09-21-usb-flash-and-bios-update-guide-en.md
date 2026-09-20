---
audio: false
generated: true
image: false
lang: en
layout: post
title: USB Flash and BIOS Update Guide
translated: false
type: note
---

The USB is built and verified. Here's the final checklist:

## ✅ USB ready (verified)

- FreeDOS boot files present, installer **skipped** → boots straight to `C:\>`
- `fpt.exe` + `fparts.txt` (your vendor's flasher)
- `NEWBIOS.BIN` (your patched BIOS), `OLDBIOS.BIN` (original), `flash.bat`
- 5.9 MB free — enough for the 4 MB `BACKUP.BIN` dump

## On the B75 PC

1. **Eject the USB** from this machine, plug it into the B75 PC.
2. **Boot from USB** — press the boot-menu key (usually **F8 / F11 / F12**, try Del/F2 for BIOS and look for "Boot Menu") and select the **legacy / non-UEFI** USB entry. (CSM is still on, so legacy boot works.)
3. At the prompt:

   ```
   C:\> flash.bat
   ```

4. It will:
   - dump your current BIOS → `BACKUP.BIN`
   - flash `NEWBIOS.BIN`
5. Wait for **`FLASH OK`** → power off.

## Then (order matters)

1. Boot into **BIOS setup** → enable **Above 4G Decoding**, disable **CSM**.
2. Boot into Linux → `sudo ./ReBarState` → type `32` → reboot.
3. Verify: `sudo dmesg | grep -i "root bus resource"` (last mem window ≥ `0xfffffffff`) or GPU-Z.

⚠️ If `flash.bat` says **FAILED** — don't power off; just run `fpt -f NEWBIOS.BIN` again. If the board won't POST later, clear CMOS (pull the battery if needed).

Good luck! Let me know how the flash goes, or if you want me to build a Windows `ReBarState.exe` for the verification side.
