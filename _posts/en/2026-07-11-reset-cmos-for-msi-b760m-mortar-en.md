---
audio: false
generated: true
image: false
lang: en
layout: post
title: Reset CMOS for MSI B760M Mortar
translated: false
type: note
---

**Question:** How do I remove the BIOS/CMOS battery and drain residual power from an MSI MAG B760M Mortar motherboard, given a PSU that produces a buzzing/whining sound and no display?

**Answer:**

This is a standard troubleshooting step for a system that won't POST and has a coil-whine/buzzing sound from the PSU — it usually means the PSU is trying to deliver power but something (VRM, GPU aux power draw, or a bad CMOS state) is causing it to fault or the board isn't reaching POST. Here's exactly how to do the CMOS reset + full discharge on the B760M Mortar:

### 1. Full power down first (critical — this is the "drain" step)

```
1. Turn off PSU via the physical switch on the back
2. Unplug the PSU from the wall outlet entirely
3. Press and hold the case power button for 10-15 seconds
   (this drains capacitors on the motherboard/PSU — this IS the "放电" step)
```

The power button press with PSU unplugged is what discharges residual capacitance in the board's power delivery circuits. Without unplugging the wall power, standby voltage (+5VSB) is still live even when the system is "off."

### 2. Remove the CMOS battery

On the MAG B760M Mortar, the CMOS battery (CR2032) is located near the bottom-right of the board, below the PCIe slots, next to the SATA ports. Steps:

```
1. With PSU unplugged and power drained (step 1 done)
2. Locate the round silver coin battery (CR2032)
3. Push the small retention clip next to it — battery pops up
4. Remove it fully
5. Wait 5-10 minutes (your instinct of 5 min is correct)
6. Reinsert with + side facing up (same orientation as before)
```

### 3. Alternative: JBAT1 jumper (faster, same effect)

Instead of pulling the battery, MSI boards have a `JBAT1` (Clear CMOS) 2-pin jumper near the battery, sometimes with a small "Clear CMOS" label silkscreened on the PCB:

```
1. PSU unplugged, power drained (step 1)
2. Find JBAT1 pins (check your manual PDF — search "JBAT1" in the B760M Mortar manual)
3. Short the 2 pins with a screwdriver tip for 5-10 seconds
   (or use the jumper cap if included, short for 5-10 sec then remove)
```

This does the exact same thing as pulling the battery — resets CMOS/BIOS settings to factory default — but is faster and doesn't risk you losing the tiny battery or bending the retention clip.

### 4. After reassembly

```
1. Reinsert battery / remove jumper short
2. Reconnect 24-pin ATX + 8-pin CPU EPS power
3. Reconnect PCIe 8-pin/6+2-pin to GPU (you confirmed this is connected — good, that's necessary for GPU to get power beyond the slot's 75W)
4. Plug PSU back into wall, flip PSU switch on
5. Power on — first boot after CMOS clear will say "CMOS checksum error, press F1" or similar → just enter BIOS and load defaults or save & exit
```

### What the buzzing PSU sound most likely means

A "zizizi" (coil whine) on power-on with no display is commonly one of:
- **VRM/MOSFET coil whine** under load spike — often benign but sometimes indicates the board is drawing power and faulting before POST (common with bad CMOS state, bad RAM seating, or GPU power issue)
- **GPU not seated fully** in the PCIe slot — reseat it, you should hear/feel a click on the latch
- **RAM in wrong slots** — B760M Mortar needs specific slots for single-stick boot (usually slot 2, check the silkscreen A2/B2 near CPU)
- **PSU itself is failing** — if buzzing persists after CMOS reset, RAM reseat, GPU reseat, test with a different PSU if you have one available

### Quick diagnostic checklist if the CMOS reset doesn't fix it

```
1. Remove GPU, try booting on iGPU (if your CPU has one) via motherboard HDMI/DP
2. If iGPU works → GPU or GPU power cable issue
3. If iGPU also fails → reseat single RAM stick in slot A2, remove all other RAM
4. Check 24-pin and 8-pin CPU power are FULLY seated (common half-inserted issue causing buzzing)
5. Check for the debug LED / debug code display on B760M Mortar — it has a CPU/DRAM/VGA/BOOT LED sequence, tells you exactly which stage is failing
```

The debug LEDs (CPU, DRAM, VGA, BOOT) near the 24-pin connector are your best diagnostic tool here — check which one stays lit when you power on, that tells you exactly where it's failing rather than guessing from the buzzing sound alone.
