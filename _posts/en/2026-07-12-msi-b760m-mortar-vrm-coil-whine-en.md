---
audio: false
generated: true
image: false
lang: en
layout: post
title: MSI B760M Mortar VRM Coil Whine
translated: false
type: note
---

Question: It turned out the buzzing is actually coming from the motherboard (MSI MAG B760M Mortar WiFi) — why would that be the source?

Answer:

## This is consistent with your elimination sequence — and it's the most common outcome

Look at what you've actually tested, in order:

1. **GPU swap (AMD ↔ Nvidia), GPU removed entirely** → no change → ruled out GPU VRM
2. **Fan/mechanical contact check** → (implicitly ruled out, since you're now pointing at mobo, not a fan)
3. **Remaining candidate**: motherboard CPU VRM (or PSU, but you've localized it to the board)

This is exactly the process used in the forum threads I found — one person explicitly narrowed it down the same way you did: swapped GPU, no change, then localized the sound intensity to directly above the CPU socket area, concluding it's the motherboard's VRM.

## Why the B760M Mortar specifically is a plausible candidate

The MAG B760M Mortar WiFi is a budget mATX board (1299 CNY) with a modest VRM design — this class of board typically runs a 6-8 phase configuration for CPU Vcore, often using smaller/cheaper inductors than a high-end Z790 board. Paired with an **i9-13900KF**, which is a 24-core (8P+16E) chip that can transient-spike to 250-300W+ under all-core boost, you're asking a budget VRM to switch large currents very fast — exactly the condition that induces audible vibration in the inductor windings (the same magnetostriction mechanism I explained for PSU coil whine, just now happening in the CPU power stage inductors next to the socket).

Notably, an MSI forum thread even had a nearly identical mobo (B650M Mortar, the AM5 sibling) show up in coil-whine-adjacent troubleshooting — this "Mortar" tier of MSI board across both AM5 and LGA1700 seems to attract these reports, likely because it's the same VRM cost tier across the lineup rather than something unique to yours.

## Whether this is a problem, and what to do about it

**Is it dangerous?** No — every source I found (Tom's Hardware, Overclock.net, MSI forums) agrees: VRM coil whine doesn't damage the board or reduce lifespan. It's purely acoustic.

**Can you reduce it? Try in this order, cheapest/safest first:**

```
1. BIOS: Disable CPU C-states (C1E, C3, C6, Package C-States) or set to "Enabled"
   depending on which state currently triggers it — C-state transitions cause rapid
   VRM duty-cycle changes, a very common whine trigger. Test both ways.

2. BIOS: Adjust Loadline Calibration (LLC) by one notch up or down —
   this changes VRM switching behavior under transient load without meaningfully
   affecting stability at stock settings.

3. BIOS: If exposed, look for "VRM Switching Frequency" — MSI sometimes exposes
   this under OC settings. Nudging it shifts the fundamental whine frequency,
   sometimes out of the audible range or your ear's sensitivity range.

4. Physical test (from the Tom's Hardware thread): power on, gently press a
   pencil eraser against the large black VRM inductors near the CPU socket
   (through the airflow gaps in the VRM heatsink if there is one, or after
   removing the heatsink if accessible). If the whine changes pitch/volume
   when you press, you've confirmed it's mechanical vibration in that specific
   inductor — a thermal pad reseat under the VRM heatsink can sometimes dampen it.

5. Undervolt/underclock test: if you've applied any XMP/EXPO on the 64GB kit
   or any all-core OC, temporarily reset to full stock JEDEC + no OC.
   If whine disappears, it's load-dependent and tied to your specific
   voltage/frequency operating point — you can then hunt for a stable point
   that doesn't excite the resonance.
```

**If none of that helps and it's genuinely loud** (not just audible with your ear near the case, but audible from normal sitting distance), that crosses from "normal VRM whine" into "possible manufacturing defect" — worth an RMA request to MSI/JD before your return window closes, especially since you haven't built the final rig yet and this is exactly the stage where a board swap is cheap and easy.

Given you're about to run this box for sustained AI training workloads (constant high CPU/GPU utilization, not bursty gaming loads), a whine that shows up under sustained all-core load is worth chasing down now rather than living with it for the next 2-3 years.

References:

- [Motherboard Coil whine? Is there any way to limit it? - Tom's Hardware Forum](https://forums.tomshardware.com/threads/motherboard-coil-whine-is-there-any-way-to-limit-it.3685126/)
- [Cannot pinpoint the source of the coil whine - Tom's Hardware Forum](https://forums.tomshardware.com/threads/cannot-pinpoint-the-source-of-the-coil-whine.3784809/)
- [Please help me diagnose my AM5 instability! - Overclock.net](https://www.overclock.net/threads/please-help-me-diagnose-my-am5-instability.1802538/)
