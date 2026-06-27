---
audio: false
generated: true
image: false
lang: en
layout: post
title: Add WD Blue 2TB to B760M Mortar
translated: false
type: note
---

Question: Given my MSI MAG B760M Mortar WiFi motherboard, can I add one more internal hard drive (WD Blue 2TB WD20EZBX)? Are the two conditions (free SATA port + 3.5" drive bay) correct?

Answer:

Yes, the two conditions are correct, and yes — you can install the WD20EZBX.

Let me verify the specifics for your board.

**SATA ports — B760M Mortar WiFi has 4× SATA 6Gb/s.** So you have room for up to 4 SATA drives total. Adding one HDD is fine unless all 4 are already occupied.

One thing to check on B760M boards: **SATA port and M.2 slot sharing.** On many B760M Mortar variants, populating certain M.2 slots disables a SATA port (lane sharing). Specifically, if you have an M.2 SSD in the SATA-mode M.2 slot, it can disable SATA2 (or a shared port). Check the manual's M.2/SATA combination table. If you only run NVMe (PCIe) M.2 SSDs, no SATA ports get disabled — NVMe doesn't share with SATA lanes the way SATA-mode M.2 does.

Quick check before buying:

```bash
# Linux — list current SATA devices and free ports
lsblk -o NAME,SIZE,MODEL,TRAN
# look for TRAN=sata; count how many are populated

# Check SATA controller and link status
sudo dmesg | grep -i sata
```

On Windows, open the case and physically count: SATA data cables plugged into the board vs. free SATA headers, and free SATA power connectors coming off the PSU.

**Physical bay:** B760M Mortar is mATX, so case-dependent, not board-dependent. Any standard ATX/mATX case has 3.5" bays — confirm yours has a free one. The WD20EZBX is a standard 3.5" drive.

**What you need:**
- 1× free SATA data cable (board usually ships with 2; or buy one ~5 CNY)
- 1× free SATA power connector from PSU (almost always spare)
- 1× free 3.5" bay + 4 mounting screws

**Verdict:** Pricing looks right (B760M Mortar WiFi ~1299, WD20EZBX ~428). As long as you have a free SATA port (not disabled by M.2 sharing) and a free 3.5" bay, plug it in, boot, and it'll show up — then partition/format it.

```bash
# After install, on Linux:
sudo fdisk /dev/sdX        # create partition
sudo mkfs.ext4 /dev/sdX1   # format
sudo mount /dev/sdX1 /mnt/data
```

One caveat worth flagging: WD20EZBX is a 7200 RPM CMR drive — good choice (CMR, not SMR), reliable for general storage. If this is for ML datasets or anything throughput-heavy, a SATA SSD or NVMe would be far faster, but for bulk cold storage at 428 CNY it's solid.
