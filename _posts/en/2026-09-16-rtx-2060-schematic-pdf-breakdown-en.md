---
audio: false
generated: true
image: false
lang: en
layout: post
title: RTX 2060 Schematic PDF Breakdown
translated: false
type: note
---

I read the PDF by extracting its full vector text (55 pages, ~242 KB of labels). Note: the file is a **schematic (Схема = "schematic" in Russian)**, not a boardview. Here's what's in it.

## Document identity

- **File:** `Gigabyte RTX 2060 Gaming OC Pro 6GB (GV-N2060GAMINGOC PRO-6GD) Rev 2.0 Схема.pdf` (1.1 MB, 55 pages, A4 landscape)
- **Origin:** NVIDIA reference design **PG161-A00**, Rev 2.0, dated 2019-03, customized by Gigabyte as the **GV-N2060GAMINGOC PRO-6GD** (title block says "Custom GV-N2060GAMINGOC PRO-6GD 2.0", Rev 2.0).
- **Board description:** TU106 6GB GDDR6, 192-bit, PCIe x16, outputs **DVI-D/DP + DP + HDMI**
- **Main parts:**
  - GPU: **TU104-400-A1**, BGA2228 (labeled G1A–G1U across sheets)
  - Memory: **6× Micron MT61K256M32JE-12:A**, FBGA180 GDDR6 (M9A/B/C/D, M10A/B/C/D, M11/M12)
  - ROM: **U11 W25Q80EW** (8 Mb SPI), 27 MHz crystal (Y1/Y2)

## Page map

| Pages | Content |
| --- | --- |
| 1–2 | Table of contents / Block diagram |
| 3–4 | PCI Express x16 edge + PCIe RC terminations |
| 5–14 | GPU↔memory buses FBA/FBB/FBC/FBD, CMD/CLK/WCK, data, DBI/EDC |
| 15–17 | GPU power/GND, decoupling |
| 18–23 | Display I/O: DVI-D, DP (A/B/C/D), HDMI, USB-C NC |
| 24–25 | NVHS/Frame-Lock, thermal, JTAG, GPIO, stereo |
| 26 | MISC2: ROM, XTAL, straps/RAMCFG |
| 27–31 | Power: 1V8_AON (U15 GS9216TQ), 5V (U4 MP1475DJ), PEXVDD (U13 GS9216TQ), FBVDDQ (U3 uP1666QQKF, 2-phase) |
| 32–36 | NVVDD controller (U504 uP9512R) + 6 phases (uPi DrMOS) |
| 37–39 | Input power balancing switcher, filtering/monitoring, steering/UPB/hot-plug |
| 40–42 | Type-C buck-boost, PD PPC, 12V & 3V3_A switcher (mostly title-block placeholder on this SKU) |
| 43–47 | Sequencing: 5V/1V8/NV3V3 enable, NV/PEX/FB enable, voltage monitor, discharge, misc |
| 48–50 | Logo LED, LED driver & boost, fan |
| 51–53 | Pre-filter, MECH, PTC |
| 54–55 | **Gigabyte custom pages:** MCU (U634 HT32F52241) + RGB LED / fan control |

## Key devices for troubleshooting

- **U504 uP9512R** – NVVDD PWM controller (VQFN5×5-40L)
- **U3 uP1666QQKF** – FBVDDQ controller (1.35 V, 2-phase)
- **U15 GS9216TQ** – 1V8_AON buck; **U13 GS9216TQ** – PEXVDD buck (~1.0 V)
- **U4 MP1475DJ** – 5 V buck; **U507/U510 NCP114AMX330** – 3V3_SEQ LDOs
- **U503 NCP45491** – input power monitor/balancer (GPU_ADC_IN_P/N, RSENSE)
- **U505/U506/U508/U509** – M74VHC1GT08 enable logic
- NVVDD phases use uPi DrMOS (INS17xxxxx), 0.15 µH inductors, 330 µF/820 µF polymer caps
- **U634 HT32F52241** + **U633 APL431** + **U849 APL3552** – Gigabyte MCU/LED/fan control

## Rails/sequence

`12V (PCIe 8-pin) → 5V → 3V3/3V3_SEQ → 1V8_AON → NV3V3 → PEXVDD → NVVDD / FBVDDQ`, enabled per sheets 43–44 with PGOOD chains (`PS_5V_PGOOD`, `PS_1V8_AON_PGOOD`, `PS_PEXVDD_PGOOD`, `PS_NVVDD_PGOOD`, `PS_VMON_PGOOD`, `PS_FBVDDQ_EN`).

Caveat: text extracted from a vector schematic can garble some small values/net names, so double-check any specific resistor/cap value on the actual PDF page before acting.

I have the cleaned per-page text saved at `%TEMP%\clean.txt` and can render any page to PNG if needed. What would you like to do with it — locate a net, trace a rail, or diagnose a fault?
