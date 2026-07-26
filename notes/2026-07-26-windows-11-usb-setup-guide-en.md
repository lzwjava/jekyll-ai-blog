---
audio: false
generated: true
image: false
lang: en
layout: post
title: Windows 11 USB Setup Guide
translated: false
type: note
---

For your specific situation (Windows 11 install on Lenovo Xiaoxin), here's what I did earlier and the recommended approach:

## What We Did Earlier (wimlib method on Mac)

```bash
# 1. Format USB as FAT32 with GPT
diskutil eraseDisk MS-DOS WIN11 GPT /dev/disk13

# 2. Mount ISO
hdiutil attach Win11_25H2_English_x64_v2.iso

# 3. Copy everything except install.wim (it's 7.1GB > FAT32's 4GB limit)
rsync -av --exclude='sources/install.wim' /Volumes/CCCOMA_X64FRE_EN-US_DV9/ /Volumes/WIN11/

# 4. Split the large install.wim into <4GB chunks
wimlib-imagex split \
  /Volumes/CCCOMA_X64FRE_EN-US_DV9/sources/install.wim \
  /Volumes/WIN11/sources/install.swm \
  3800

# 5. Eject when done
diskutil eject /dev/disk13
```

This produces a **UEFI-bootable** USB that Windows Setup recognizes natively. The `.swm` split files are handled automatically by the installer.

## Alternative (if you have a Windows machine)

**Rufus** — simplest option:

- Select ISO → pick **GPT + UEFI (non-CSM)** → click Start
- Handles the `install.wim` size issue automatically

## Alternative (if you stick with Mac)

**balenaEtcher** — **not recommended** for Windows ISOs as discussed earlier (wrong image type).

## Key Point for Your Lenovo Xiaoxin

However — the **bigger issue** right now is the `0xC19001F4` error you're hitting. Before re-flashing, I'd check this BIOS setting first:

> **Intel VMD Controller** or **Intel RST** → set to **Disabled** / **AHCI**

That's more likely to be your actual blocker than the USB stick itself. Want me to walk you through finding it in the BIOS?
