---
audio: false
generated: true
image: false
lang: en
layout: post
title: ReBarUEFI B75 BIOS Flash Drive
translated: false
type: note
---

Here's what's on the USB drive:

## `/dev/sdb` — 14.65 GiB USB drive (model "YGS")

**Partition:** `sdb1` — 32 MB FAT16, bootable, label `FD13-LITE` (rest of the 14.6 GB is unallocated)

## What it is

A **bootable FreeDOS 1.3 "Lite" USB stick** purpose-built for **BIOS firmware flashing** — specifically a **"ReBarUEFI - B75 BIOS flash"** tool.

**Key files at the root:**
- `flash.bat` — the main script: backs up current BIOS to `BACKUP.BIN`, then flashes `NEWBIOS.BIN` using Intel's Flash Programming Tool (`fpt.exe`)
- `fpt.exe` — Intel Flash Programming Tool
- `NEWBIOS.BIN` / `OLDBIOS.BIN` — new/old BIOS images (4 MB each)
- `BACKUP.BIN` — backup of the original BIOS (4 MB)
- `fparts.txt` — flash chip part list
- `KERNEL.SYS` + `COMMAND.COM` + `fdconfig.sys` + `fdauto.bat` — FreeDOS boot environment
- `setup.bat` — FreeDOS installer
- `freedos/` — FreeDOS system files
- `packages/` — FreeDOS package archives (.zip)

## What `flash.bat` does

1. Backs up the current BIOS: `fpt -d BACKUP.BIN`
2. Flashes the new BIOS: `fpt -f NEWBIOS.BIN`
3. On success: tells you to power off/on. On failure: warns you **not** to power off and to retry.

## ⚠️ Caution

This is a **BIOS firmware flashing disk** (for an Intel B75 motherboard, adding ReBar/UEFI support). Flashing the wrong BIOS or interrupting the process can **brick the machine**. Only use it on the intended hardware.

Want me to examine any file in more detail (e.g. `fparts.txt` to see the supported flash chips, or compare `NEWBIOS.BIN` vs `OLDBIOS.BIN`)?