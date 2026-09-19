---
audio: false
generated: true
image: false
lang: en
layout: post
title: X99 ReBAR Support Inquiry
translated: false
type: note
---

**Question:** Does the 精粤 X99M GD4 ARGB motherboard support Resizable BAR and Above 4G Decoding natively?

**Answer:**

There is no official documentation or specific user report I can find confirming that the **精粤 (Jingyu) X99M GD4 ARGB** supports these features out of the box. However, based on the broader X99 platform picture, here is what applies to your board:

---

**Short answer: Almost certainly NO natively — but partial workarounds exist.**

---

**Why it doesn't support them natively:**

The X99 chipset dates from 2014. Resizable BAR as a native BIOS feature was only introduced on Intel 400-series (Comet Lake) and AMD 400-series platforms and newer. Budget Chinese X99 boards like yours were never designed with ReBAR or Above 4G Decoding in mind, and their BIOS vendors (typically AMI Aptio-based) did not include those options.

---

**What you can try:**

There are three community paths for X99 boards, all requiring some caution:

1. **Above 4G Decoding via hidden BIOS variable** — On many X99 boards the option exists but is hidden. You can unlock it using the `setup_var` method via a GRUB EFI shell. The offset varies per board; you'd need to extract and read your BIOS's IFR (Internal Form Representation) to find the correct offset. For some X99 boards, the Above 4G Decoding offset has been found at `0x16D`, and the procedure involves setting it to `0x0`, rebooting, then `0x1` and rebooting again.

2. **ReBarDxe BIOS mod** — The `ReBarUEFI` project provides a DXE driver that can be injected into the BIOS using UEFITool to enable Resizable BAR on any supported system, with the only hard requirement being that 4G Decoding is enabled first. Without Above 4G Decoding, you're limited to BAR sizes that fit below 4 GB — typically **1 GB maximum**.

3. **Without Above 4G Decoding** — Even without 4G Decoding enabled, you can still try setting ReBAR to 256 MB, 512 MB, or 1 GB and may see some performance improvement, even if you can't reach the full VRAM size.

---

**Important caveats for your board specifically:**

- The 精粤 X99M GD4 ARGB is a budget Chinese board with limited community documentation. BIOS modding it carries brick risk, and there is no known pre-made modded BIOS for this exact model floating around.
- Similar boards like the JGINYUE X99-M D4 have reported UEFI/CSM conflicts — some users found only CSM/Legacy mode works, meaning they cannot disable CSM, which is a prerequisite for enabling ReBAR. Your board may have the same issue.
- You'd need a hardware programmer (e.g., CH341A) as a safety net before attempting any BIOS flash.

---

**References:**

- [ReBarUEFI Release Thread – WinRaid Level1Techs](https://winraid.level1techs.com/t/release-resizable-bar-bios-efi-module/100235)
- [xCuri0/ReBarUEFI GitHub](https://github.com/xCuri0/ReBarUEFI)
- [Guide: Overclock BIOS Mods for Chinese X99 MBs – WinRaid](https://winraid.level1techs.com/t/guide-overclock-bios-mods-for-chinese-x99-mbs/104683)
- [Enabling Hidden 4G Decoding – ReBarUEFI Wiki](https://github.com/xCuri0/ReBarUEFI/wiki/Enabling-hidden-4G-decoding)
