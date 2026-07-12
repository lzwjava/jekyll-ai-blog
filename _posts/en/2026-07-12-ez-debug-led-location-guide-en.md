---
audio: false
generated: true
image: false
lang: en
layout: post
title: EZ Debug LED Location Guide
translated: false
type: note
---

Question: Where is the EZ Debug LED on MSI MAG B760M Mortar motherboard?

Answer:

On the **MSI MAG B760M Mortar (DDR5/WiFi)**, the **EZ Debug LED** is located on the **top-right edge of the motherboard**, near the **24-pin ATX motherboard power connector**.

Look for a vertical row of **four small LEDs** with labels:

```
CPU   (red)
DRAM  (yellow)
VGA   (white)
BOOT  (green)
```

Typical layout:

```
             CPU_FAN
                |
                |
        [ EZ DEBUG LED ]
        CPU   ●
        DRAM  ●
        VGA   ●
        BOOT  ●

24-pin ATX POWER
████████████████
```

On the physical board:

1. Open your case side panel.
2. Look at the **right side of the RAM sticks**.
3. Find the big **24-pin power connector**.
4. The EZ Debug LEDs are **just above the 24-pin connector**, close to the motherboard edge.

For your symptom:

> CPU fan spins, but no display / cannot boot

Check which LED stays lit:

* 🔴 **CPU LED** → CPU power cable (8-pin EPS), CPU installation, BIOS compatibility
* 🟡 **DRAM LED** → RAM not seated, wrong slot, memory training (wait 1–3 minutes after first boot)
* ⚪ **VGA LED** → GPU issue, especially relevant with your AMD MI50 experiment
* 🟢 **BOOT LED** → no boot device found (but BIOS should still display)

Since you are using **MSI MAG B760M Mortar + AMD MI50**, I would check these first:

1. Make sure the **8-pin CPU power connector (EPS12V)** at the top-left of motherboard is plugged in.
2. Remove GPU and try motherboard HDMI/DP output (only if your CPU has iGPU; KF CPUs do not).
3. Reseat RAM: use **A2 slot** (second slot from CPU).
4. Clear CMOS.
5. Check whether the **VGA EZ Debug LED stays white** — MI50 is a server GPU and sometimes has PCIe/BIOS compatibility issues.

The exact EZ Debug LED area is the small 4-light column next to the 24-pin ATX connector, not the RGB/debug display area.
