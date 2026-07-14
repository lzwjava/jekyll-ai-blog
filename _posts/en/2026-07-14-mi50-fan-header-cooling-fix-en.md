---
audio: false
generated: true
image: false
lang: en
layout: post
title: MI50 Fan Header Cooling Fix
translated: false
type: note
---

Question: You mentioned the MI50 has a fan port — how does that change the cooling plan?

Answer:

Good catch, and you're right — worth correcting. The MI50 PCB does expose a small onboard fan header (typically 2-pin or 4-pin, low current, meant for a small 40-60mm blower), separate from being a "fanless" design in the sense of having no way to attach one. What I said earlier about needing an external controller/shroud with its own power tap is only half the picture — there are two real approaches depending on what your specific card revision exposes:

**Option A — card's onboard fan header drives GPU-firmware-controlled fan curve.**
Some MI50 boards' onboard header is tied to the GPU's own thermal sensor/VBIOS fan curve, so plugging a compatible fan in gives you automatic speed ramp with load — no separate temp controller needed. This is the cleaner setup if your card supports it.

**Option B — onboard header is unregulated/fixed voltage, needs external PWM/thermistor control.**
Several documented shroud builds still add an external thermistor-based PWM controller powered via a spare 6-pin, because the onboard header alone doesn't give a proper curve — it's just a power tap, not a controlled signal.

**What to actually check before buying a fan:**
1. Measure/inspect the header pin count and pitch (2-pin DC vs 4-pin PWM) — don't guess, use a multimeter or check for markings near the heatsink
2. Confirm whether it's 5V or 12V — mismatched voltage either underdrives or over-revs the fan
3. Match a small high-static-pressure blower rated for that connector — the widely-used reference fan in shroud builds for this card is a 40mm server blower (ARCTIC S4028-15K or similar), since low-power 1-2W fans were reported as insufficient and caused throttling; 5W-class blowers perform properly but are loud

**Shroud:** you still need the ducting/shroud itself — the onboard header solves power/control, not airflow directionality. Printable shrouds for MI50/MI25/MI60 (same form factor) are available on Thingiverse and MakerWorld, some bundled with a thermistor module and fan sourced from Taobao for exactly this purpose.

**Revised concrete pick:** print or buy an MI50-specific shroud (Thingiverse "MI50 Cooling Shroud" or MakerWorld's temp-controlled variant), pair with a 40mm 5W-class server blower matched to your header's pinout/voltage, and only add an external thermistor controller if your card's onboard header turns out to be a fixed-voltage tap rather than a controlled signal.

References:
- [MI50 Cooling Shroud / Fan Adapter — Thingiverse](https://www.thingiverse.com/thing:7090347)
- [MI50 Temperature-Controlled Heatsink — MakerWorld](https://makerworld.com/en/models/1856095-mi50-temperature-controlled-heatsink)
