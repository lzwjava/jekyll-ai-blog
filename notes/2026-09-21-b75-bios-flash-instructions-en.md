---
audio: false
generated: true
image: false
lang: en
layout: post
title: B75 BIOS Flash Instructions
translated: false
type: note
---

Everything's prepared. Here's exactly how to flash — I've already staged all the files and a one-command script.

## What I prepared

In `/home/lzw/Downloads/B75/rebar-work/`:

- **`make-usb.sh`** — one command that builds the whole bootable USB
- **`FD13LITE.img`** — FreeDOS boot image (32 MB)
- **`usb-flash/`** — the DOS flash files:
  - `fpt.exe` + `fparts.txt` (your vendor's flasher)
  - `NEWBIOS.BIN` = your final `b75_modded.bin.patched`
  - `OLDBIOS.BIN` = original (safety copy on the USB)
  - `flash.bat` = auto backup + flash script

## Steps

**1. Plug a USB stick (any size) into THIS Linux machine**, then tell me (or run):

```bash
lsblk                          # find the USB, e.g. /dev/sdb
cd /home/lzw/Downloads/B75/rebar-work
sudo ./make-usb.sh /dev/sdb     # <-- whole disk, NOT /dev/sdb1
```

The script refuses to touch non-removable disks (safety), writes FreeDOS, copies the flash files, and patches it to **boot straight to a `C:\>` prompt** (skips the FreeDOS installer). It asks you to type `YES` before erasing the USB.

**2. Move the USB to the B75 PC and boot from it.**
- Press the **boot menu key** (usually F8 / F11 / F12, depends on board) and pick the **non-UEFI / legacy** USB entry. DOS needs legacy boot, so keep CSM ON for now.

**3. At the `C:\>` prompt, type:**
```
flash.bat
```

It does two things:
1. Backs up your current BIOS → `BACKUP.BIN` (on the USB)
2. Flashes `NEWBIOS.BIN` (full 4 MB image, same `fpt -f` method your vendor's `1.BAT` uses)

**4. Wait for `FLASH OK`**, then power off.

## After flashing (order matters)

1. Power on → **BIOS setup**:
   - Enable **Above 4G Decoding**
   - Disable **CSM** (only *after* the flash is done — you needed it on to boot the DOS USB)
2. Boot into Linux and run `sudo ./ReBarState`, type `32`, reboot.
3. Verify with `dmesg | grep -i "root bus resource"` or GPU-Z.

---

⚠️ Two safety notes:
- If `flash.bat` ever reports **FAILED** — do **not** power off; just run `fpt -f NEWBIOS.BIN` again.
- Keep `B75V101_original.bin` (and the `OLDBIOS.BIN` copy on the USB) safe — that's your recovery image.

Go ahead and plug in the USB and tell me the device name (or paste `lsblk` output), and I'll run the script for you.