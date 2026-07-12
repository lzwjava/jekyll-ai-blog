---
audio: false
generated: true
image: false
lang: en
layout: post
title: Cable Mix-Up Caused Motherboard Short
translated: false
type: note
---

Question: What's the likely root cause of the buzzing sound (滋滋响) and failure to power on, discovered on the motherboard near the SATA5/6 ports after swapping an RTX 4070 for a used AMD MI50 in this system (MSI B760M Mortar WiFi, i9-13900KF, Corsair CX650F/750F 750W PSU)?

Answer:

## Timeline reconstruction

1. System worked fine with RTX 4070.
2. You pulled the 4070, installed the used MI50, connected its power (MI50 needs **2× 8-pin PCIe power connectors, 300W total draw**, confirmed by AMD's own spec sheet and multiple vendor listings).
3. Buzzing + no boot appeared immediately at that point.
4. You reinstalled the 4070 to isolate the GPU as the cause.
5. You went back to basic power testing (the paperclip/jumper pin-4/pin-5 test you pasted — correct standard procedure to bench-test a PSU in isolation).
6. Using a stethoscope, you localized the buzzing to the **motherboard itself**, near SATA5/SATA6 — not the PSU.
7. You pulled the AIO to rule out pump/electrical noise from the cooler — buzzing persisted, so you reinstalled it.
8. Current worst symptom: **connecting only the 24-pin ATX cable (no CPU EPS, no GPU) already produces buzzing and no successful power-on.**

That last point is the most diagnostically important fact you gave me.

## Primary hypothesis: PSU cable mix-up caused a short, and the board (or a VRM stage) is now damaged

Corsair explicitly warns that on modular PSUs, the **"CPU" 8-pin cable and the "PCIe" 8-pin cable are physically the same connector shape but wired with different, non-interchangeable pinouts** — they are keyed identically but electrically incompatiblesince PCIe cables go to the graphics card while the cable marked CPU mounts in the motherboard's 8-pin header, and the two are not interchangeable. This is a very well-documented failure mode: users grab a spare 8-pin cable from the same modular PSU kit, assume it's a PCIe cable because it "looks right," and plug it into a GPU — because different manufacturers (and even different cables from the same manufacturer) use different pinouts on the PSU-side connector, this can supply incorrect voltage to the component, and the damage isn't always obvious until something fails.

This matches your evidence almost exactly:

- MI50 needs two dedicated PCIe 8-pin cables you likely don't already own in the right count/labeling (used server card, purchased separately from your CX PSU).
- The problem appeared at the exact moment of plugging in the new GPU's power cables.
- The noise is now present **even without the GPU connected**, which means the damage is no longer conditional on GPU presence — it's a standing short somewhere in the board's power delivery path (most likely a shorted MOSFET or inductor in the 12V distribution feeding the PCIe slot / auxiliary rail).
- You confirmed via stethoscope the noise source is the **board**, not the PSU — consistent with a damaged component on the motherboard now drawing current abnormally as soon as 12V is present on the 24-pin, rather than a PSU that's cycling on protection.

A shorted MOSFET (drain-source short) creates a permanent low-impedance path across the rail. That draws current the instant 12V appears on the ATX connector — independent of whether anything is plugged into SATA or PCIe — which is exactly why "only ATX connected" still buzzes and fails to boot.

## Why SATA5/6 specifically

The buzzing being audible right at SATA5/6 doesn't necessarily mean the SATA controller itself is damaged — it's more likely that the damaged component (VRM choke/MOSFET for the PCIe slot's 12V/3.3V, or a shared power stage) sits physically near that connector on the B760M Mortar's PCB layout, and the coil is now audibly oscillating under abnormal current. Coil whine/buzzing near an inductor under load (or under a fault condition drawing current) is a textbook symptom of either (a) a component right at current limit, or (b) a genuine short pulling current through that inductor continuously.

## What this is *not* likely to be

- Not the AIO — you already isolated and ruled that out.
- Not simply "MI50 has no display output" — MI50 is a passively-cooled, headless compute accelerator; even in a working state it may not output video normally without a modified vBIOS, but that's a separate configuration issue from a buzzing short and wouldn't explain buzzing with the GPU removed entirely.
- Probably not PSU-side buzzing (OCP retry chirp) — the stethoscope test already localized it to the board.

## Recommended diagnostic order (stop guessing, isolate methodically)

1. **Stop power-cycling repeatedly.** Every cycle with a live short risks cascading the damage to the CPU, PSU, or causing a genuine fire/burn risk. Visually inspect the board near SATA5/6 and the PCIe slot power stage for scorch marks, bulging/leaking capacitors, or discoloration, and smell for a burnt-electronics odor.
2. **Bench-test the PSU alone**, exactly as you were already doing with the paperclip jumper on pins 4/5 of the 24-pin — MSI's own bare-minimum boot test procedure recommends stripping the system down to CPU, cooler, one RAM stick, PSU, and monitor, removing all other peripherals, to isolate whether the fault is in the PSU/CPU path or in add-in hardware. If the PSU fan spins cleanly and stays spinning, the PSU itself is very likely fine, reinforcing that the fault is on the motherboard.
3. **Test the motherboard bare-minimum with a different, known-good PSU if you have access to one** (even a lower-wattage spare) — 24-pin + CPU EPS + one RAM stick + CPU, no GPU, no SATA. If it still buzzes and fails to power on under a completely different PSU, that conclusively proves the fault is on the motherboard, not any cable or PSU pairing.
4. **Read the EZ Debug LEDs** on the board (top-right corner near the 24-pin/DIMM slots, four LEDs labeled CPU / DRAM / VGA / BOOT top to bottom) — but note that if the board is in a hard-short state, it likely won't even get far enough into POST for these to be meaningful; they mainly matter once you've confirmed the board powers on without buzzing.
5. Get a clear photo of which LED (if any) is lit for anyone helping you further — that's what the support chat you pasted was asking for.

## Likely outcome

Given (a) the timing (fault appeared exactly when the MI50's power cables went in), (b) the well-documented CPU/PCIe cable mix-up failure mode on modular PSUs, and (c) the fault persisting with only the 24-pin connected, I'd put this at **high likelihood of permanent motherboard damage** (a shorted component in the slot/12V power delivery stage), triggered by a miswired power cable to the MI50. The CX650F/750F PSU itself is probably fine, but should be validated per step 3 before ruling it out completely.

Practical next step: don't reconnect the MI50 again until the board is confirmed dead or repaired — even if it were somehow fine, reintroducing the same load onto a board with a shorted stage would only compound the damage. If bench-testing confirms the board is toast, RMA it (MSI B760M Mortar is common enough that RMA/replacement is straightforward), and going forward, always use the two 8-pin cables explicitly stamped **"PCIe"** on the connector body, sourced from the same modular PSU kit, never CPU/EPS cables, and never mixed from a different PSU model.

One more thing worth double-checking while you're at it: your notes list the PSU as "Corsair CX650F RGB... 750瓦" — CX650F is a 650W unit; if you actually have a CX750F, that's fine, but if it's genuinely a CX650F rated 650W, that's tighter than ideal for a 253W-turbo i9-13900KF (which can transiently spike well above its rated PL2) plus a 300W MI50. Worth confirming the exact model/label on the unit once you're back to testing.

References:

- [Can I use a PCI-e cable in the 8-pin motherboard plug? – Corsair](https://www.corsair.com/us/en/explorer/diy-builder/power-supply-units/can-i-use-a-pci-e-cable-in-the-8-pin-motherboard-plug/)
- [Got a new PSU? Reusing your old cables is a gamble you shouldn't take – XDA](https://www.xda-developers.com/never-reuse-old-cables-with-new-psu/)
- [AMD Radeon Instinct MI50 GPU specs – ITCreations](https://www.itcreations.com/amd-gpu/amd-radeon-instinct-mi50-gpu)
- [MSI: What to do if there is no power after booting up or no display on the monitor](https://www.msi.com/support/technical_details/MB_Boot_No_Display)
- [MSI EZ Debug LED troubleshooting – CGDirector](https://www.cgdirector.com/msi-ez-debug-leds-troubleshooting/)
