---
audio: false
generated: true
image: false
lang: en
layout: post
title: USB Disk Device and Partition Details
translated: false
type: note
---

Your USB disk is here:

**Device: `/dev/disk12`** — a generic **"OnlyDisk"** USB flash drive, **15.7 GB**, removable, currently **not mounted**.

It has a GPT partition table with 4 partitions:

| Partition | Type | Size | Filesystem |
|---|---|---|---|
| `s1` | Microsoft Basic Data | 6.5 GB | MS-DOS (FAT) |
| `s2` | EFI | 5.3 MB | — |
| `s3` | Microsoft Basic Data | 307 KB | — |
| `s4` | Linux Filesystem | 9.2 GB | none detected |

It looks like a **bootable/multi-boot USB stick** (EFI partition + FAT data partition + a raw Linux partition), likely created by a tool like Ventoy or a Linux installer. SMART isn't supported, so can't check its health.

Want me to mount partition `s1` (the FAT one) so you can browse its contents?
