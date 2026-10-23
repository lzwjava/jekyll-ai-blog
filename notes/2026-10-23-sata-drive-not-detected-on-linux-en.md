---
audio: false
generated: true
image: false
lang: en
layout: post
title: SATA Drive Not Detected on Linux
translated: false
type: note
---

Checked both Linux boxes at the port level — here's the situation:

## The 500 GB disk is **not electrically visible** on either machine

| Machine | SATA controller | Ports with link | Free ports |
| --- | --- | --- | --- |
| `.34` (MS-7996 desktop) | Intel Q170 AHCI | `ata4` = WD 1TB only | ata1, ata2, ata3, ata5, ata6 — all **link down** |
| `.137` (Debian) | Intel Q170 AHCI | `ata4` = faspeed 60GB only | ata1, ata2, ata3, ata5, ata6 — all **link down** |

`lsblk`, `fdisk -l`, `blkid`, `/proc/partitions` — all consistent: only the original boot disk on each box. Nothing new came up at boot, and nothing hot-plugged in while running.

One clue: on `.34` there's history of an **exFAT `sdc2`** disk mounted ~Oct 14–16 (it's gone now) — so `.34` *has* seen another disk before.

## What to check at the hardware (most likely causes, in order)

1. **Which machine did you plug it into?** Every port is silent right now, so it's not this side — it's the connection.
2. **Power**: bare SATA drives need their own SATA power plug. If the drive doesn't spin (can you feel vibration?) → no power. This is the #1 cause of "not visible at all".
3. **Seat & cable**: reseat both ends of data + power; make sure the SATA data cable clicks in.
4. **BIOS**: IDE/AHCI boot screen — does the POST show 500GB in the drive list? (Best sanity check.)
5. **Dead drive**: put it in a USB-SATA dock to verify it works at all.

## Once it's plugged in properly — I'll take it from here

Tell me which machine (or just say "done" after reseating), and I'll:

- Confirm detection (`lsblk`/`dmesg`),
- Partition + format it (ext4),
- Mount permanently (`/etc/fstab`),
- Get the disk space math going for MiniMax-H3 storage.

If it's actually in a **USB dock** instead, tell me and I'll check the Mac (`diskutil list`) or the machine's USB bus (`lsusb`) instead.

⚠️ Also, reminder from earlier: `.34`'s GPU driver is still wedged from our DeepSpeed test (system is still logging hung-task traces every few minutes, and it has 3 unkillable D-state processes) — when you're next near that box, a **reboot is the clean fix**.
