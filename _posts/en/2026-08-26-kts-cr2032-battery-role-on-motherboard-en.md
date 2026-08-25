---
audio: false
generated: true
image: false
lang: en
layout: post
title: KTS CR2032 Battery Role on Motherboard
translated: false
type: note
---

**Question:** What is the KTS CR2032 lithium battery, and what is its role in a motherboard?

**Answer:**

**KTS** is a brand/manufacturer name printed on the battery. The CR2032 is the battery model — a small coin-cell (button cell) battery. Here's a breakdown:

**What is CR2032?**
- **C** = Lithium chemistry
- **R** = Round shape
- **20** = 20mm diameter
- **32** = 3.2mm thickness
- Voltage: **3V**

**What does it do on a motherboard?**

It powers the **CMOS** (Complementary Metal-Oxide Semiconductor) chip on the motherboard. Specifically it:

1. **Keeps the BIOS/UEFI settings alive** — things like boot order, system clock, and hardware configurations are stored in CMOS memory. This battery keeps that memory powered even when the PC is unplugged.
2. **Maintains the Real-Time Clock (RTC)** — so your computer knows the correct date and time even after being powered off.
3. **Preserves hardware settings** — overclocking configs, fan profiles, etc.

**Signs the CMOS battery is dead:**
- Computer loses time/date after shutdown
- BIOS resets to factory defaults on every boot
- Error messages like *"CMOS checksum error"* on startup

**KTS CR2032 Specs (typical):**
| Spec | Value |
|---|---|
| Voltage | 3V |
| Capacity | ~220 mAh |
| Type | Lithium coin cell |
| Connector | Some variants have a 2-pin plug (for laptops) |

The KTS CR2032 variant with a 2-pin plug is specifically designed for CMOS/BIOS use in laptop and desktop motherboards. The standard CR2032 without a plug sits in a holder on desktop boards and can be replaced in seconds.

**References:**
- [KTS CR2032 on Newegg](https://www.newegg.com/p/14R-09B4-00B06)
- [KTS CR2032 10-Pack on eBay](https://www.ebay.com/itm/236013234233)
- [KTS CR2032 CMOS Battery Kit (Latinafy)](https://latinafy.com/products/kts-cr2032-3v-cmos-bios-battery-kit-for-motherboards-10-units/)
