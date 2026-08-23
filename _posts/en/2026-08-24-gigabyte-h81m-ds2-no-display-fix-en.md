---
audio: false
generated: true
image: false
lang: en
layout: post
title: Gigabyte H81M-DS2 No Display Fix
translated: false
type: note
---

**Question:** A computer with a Gigabyte GA-H81M-DS2 (Ultra Durable UEFI BIOS) won't display anything ("can't light up") — what are the likely causes and how do you fix it?

---

**Answer:**

"Can't light up" (no POST / no display) on this board is almost always one of several well-known culprits. Here's a systematic breakdown:

---

### Common Causes

**1. RAM issue** — the most frequent cause on H81 boards.
Unseated, faulty, or incompatible RAM sticks will prevent POST entirely.

**2. Wrong display output** — if a dedicated GPU is installed, the monitor cable must plug into the GPU, not the motherboard's I/O panel.

**3. CPU compatibility (BIOS version mismatch)** — early releases of Intel 8-series chipset boards (including H81) did not support Haswell Refresh processors out of the box, requiring a BIOS update first.

**4. Corrupted or bad BIOS** — if the BIOS has bad configuration values, the board may fail to POST. Clearing the CMOS values and resetting to defaults can resolve this.

**5. Power supply insufficient or failing** — to meet expansion requirements, it is recommended to use a power supply of 500W or greater; using one that doesn't provide enough power can prevent normal operation.

**6. Short circuit or hardware fault** — a short circuit somewhere on the board can prevent it from starting; common failure points include MOSFETs, capacitors, and resistors.

---

### How to Fix — Step by Step

**Step 1 — Check the monitor cable**
Make sure the cable goes into the GPU (if one is installed), not the motherboard video output.

**Step 2 — Reseat / test the RAM**
Remove all RAM sticks, clean the gold contacts with an eraser, and re-insert one stick at a time. Try each slot. Use known-compatible DDR3 RAM.

**Step 3 — Clear the CMOS**
Use the CMOS jumper (short it for a few seconds with power disconnected) or remove the CMOS battery for a minute, then reinsert. This resets all BIOS values to default.

**Step 4 — Strip down to minimum components**
Boot with only CPU + 1 RAM stick + PSU connected (no GPU, no drives, no extra cards). If it POSTs, add parts back one by one.

**Step 5 — Test the PSU**
Swap in a known-good power supply. A failing PSU can cause no-POST symptoms with no obvious signs.

**Step 6 — Check CPU seating**
Reseat the CPU carefully. Inspect the LGA1150 socket for bent pins.

**Step 7 — Inspect the board for damage**
Check the circuitry — coils, MOSFETs, capacitors, and inductors. A failed power rail can stop the board from functioning. Look for bulging capacitors or burn marks.

**Step 8 — Re-flash the BIOS (last resort)**
If the board shows POST codes but keeps cycling, a BIOS reflash may be needed. Gigabyte's Q-Flash tool allows BIOS recovery from a USB drive without needing to enter Windows.

---

### Quick Summary Table

| Cause | Fix |
|---|---|
| RAM not seated | Reseat / swap stick/slot |
| Monitor plugged into wrong port | Move cable to GPU |
| Corrupted CMOS | Clear CMOS / remove battery |
| CPU incompatible (no BIOS update) | Flash BIOS with supported CPU first |
| Weak PSU | Replace PSU (500W+ recommended) |
| Hardware short/damage | Inspect board, take to repair shop |

---

**References:**
- [GA-H81M-DS2 User's Manual (Gigabyte official PDF)](https://download.gigabyte.com/FileList/Manual/mb_manual_ga-h81m-ds2_4001_e.pdf)
- [SOLVED: GA-H81M-DS2 Constant Power Cycling (Badcaps forum)](https://www.badcaps.net/forum/troubleshooting-hardware-devices-and-electronics-theory/troubleshooting-desktop-motherboards-graphics-cards-and-pc-peripherals/85547-solved-gigabyte-ga-h81m-ds2-rev-3-0-constant-power-cycling)
- [GA-H81M-DS2 Repair Guide & Schematics (DIY Laptop Repair forum)](https://www.diy-laptoprepair.com/forum/fix-GIGABYTE-GA-H81M-DS2-repair-guide-schematics.php)
- [No Signal Troubleshooting — PCPartPicker community](https://pcpartpicker.com/forums/topic/109914-no-signal-on-my-monitor)
