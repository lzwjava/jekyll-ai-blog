---
audio: false
generated: true
image: false
lang: en
layout: post
title: MSI SATA Port Naming Guide
translated: false
type: note
---

**Question:** Are the two SATA port groups in the photo labeled `SATA_A1/A2` and `SATA5/6 (optional)`?

**Answer:**

Yes, that lines up with standard MSI SATA labeling conventions on Mortar-series boards. Here's what the naming actually tells you:

- **`SATA_A1` / `SATA_A2`** — these come directly off the chipset (or CPU-integrated SATA controller on some AM5 boards). The `_A` suffix is MSI's way of grouping ports that share a controller bank. These are always-on, full-bandwidth SATA 6Gb/s ports.

- **`SATA5` / `SATA6` (optional)** — the "(optional)" tag is the important part. On MSI boards this almost always means these ports **share PCIe lanes with an M.2 slot**, typically an M.2 SATA-mode slot or a shared switch. If you populate that M.2 slot with an NVMe/SATA SSD, `SATA5`/`SATA6` get disabled automatically — that's exactly the pattern seen on similar MSI boards, where certain SATA ports were controlled by a separate ASMedia controller versus the main chipset, with a documented dependency on which ports work under which configuration.

Practical implication for your build: if you're planning to use all your SATA drives, **check your board's manual for the specific M.2 slot that disables SATA5/6** before you populate it — this trips people up constantly, including on X570/B650 boards where the manual didn't always make the M.2/SATA conflict obvious until MSI later clarified the wording.

If you tell me the exact model (looks like it could be a B650M/B850M Mortar based on the shroud design), I can pull the specific manual and confirm exactly which M.2 slot shares lanes with SATA5/6 for your board.

References:

- [Disabled SATA ports when configuring RAID - MSI X570 (Tom's Hardware)](https://forums.tomshardware.com/threads/disabled-sata-ports-when-configuring-raid-msi-x570.3657256/)
