---
audio: false
generated: true
image: false
lang: en
layout: post
title: B760M Mortar WiFi CMOS Battery Guide
translated: false
type: note
---

On the MAG B760M Mortar WiFi, the CR2032 sits in a round holder near the bottom-right area of the board, usually below the PCIe x16 slot / near the SATA ports, held by a small metal retention clip.

**Remove it:**
1. Power off, unplug PSU, hold the power button 5-10s to drain residual capacitors.
2. Locate the round silver coin battery. There's a thin metal spring clip on one edge of the holder.
3. Push the clip *away* from the battery edge with your fingernail or a small flathead screwdriver — this releases the retention tension.
4. The battery will pop up slightly on a spring. Lift it out with your fingers (don't touch the flat faces if you're worried about oxidation — minor, but fine to avoid).

**Insert the new one:**
1. Check polarity: the **+** side (usually printed on the battery) faces **up**, away from the board — same orientation as the one you removed.
2. Slide it in at an angle under the clip's lip first, then press down flat until it clicks/seats fully into the holder.
3. It should sit flush, held snugly by the clip with no wobble.

**After swap:**
- CMOS resets to defaults (this is expected, it's why you're replacing it — a dead CR2032 causes clock resets / BIOS setting loss).
- Boot into BIOS (Del key), reset date/time, reload any custom settings (XMP profile, boot order, fan curves) since it's now defaulted.
- If it won't boot or beeps, double check the battery orientation and that it's seated flush — a battery in backwards won't provide voltage.

One thing worth checking: if you're getting CMOS resets on a board this age, it might be worth measuring the old battery's voltage with a multimeter first (should be ~3V; if it's under ~2.5V that confirms it's the culprit rather than a BIOS/power issue).
