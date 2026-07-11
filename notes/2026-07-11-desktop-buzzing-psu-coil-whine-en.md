---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Desktop Buzzing: PSU Coil Whine"
translated: false
type: note
---

Question: My desktop makes a buzzing (滋滋 / "zī zī") noise. I swapped between an AMD GPU and an Nvidia GPU and the noise didn't change, and it's identical whether the GPU is connected or not — so I've ruled out the GPU. Given this, and my planned parts list (mostly Corsair CX650F PSU, i9-13900KF, MSI B760M Mortar, RTX 4070, etc., ~14,000 CNY total), what's going on and is this build okay?

Answer:

## The physics: what "coil whine" actually is

Every switching component on your board — PSU, VRM inductors, GPU inductors — works by rapidly chopping DC current through an inductor (a coil) at frequencies typically in the 20 kHz–1 MHz range to regulate voltage (buck converter topology). The magnetic field in the coil causes the windings to physically vibrate at that switching frequency (magnetostriction + Lorentz force on the wire). If that frequency (or a harmonic) falls in the audible range (~20 Hz–20 kHz) and the potting/varnish on the coil is loose, you hear it as a whine or buzz. It's electromechanical, not electrical damage — coil whine by itself doesn't harm the system.

Your test — swap AMD↔Nvidia GPU, no change; remove GPU entirely, no change — is actually a clean elimination experiment. It correctly rules out:

- GPU VRM inductors
- GPU power delivery board

That leaves three remaining switching-regulator subsystems, in likely order given your PSU model:

1. **PSU** (CX650F) — internal transformer/inductors on the primary and secondary side
2. **Motherboard VRM** (CPU power delivery, the inductors near the CPU socket)
3. **RAM / VRM on peripheral cards** — much less likely to be audible

## Why I'd bet on the PSU specifically

I searched for reports specific to your exact model, the CX650F, and it has a documented history of this exact complaint — users report the CX650F making a "weird crackling noise", and more broadly the CX series is commonly known for buzzing/coil whine issues attributed to lower-cost capacitor and inductor components. One thread on the CX650F specifically frames it as coil whine typically originating from the PSU, motherboard, or GPU, and recommends RMA if the unit is new.

This lines up with the CX650F's market position: it's an 80+ Bronze, non-Seasonic-platform unit at the budget end of Corsair's stack. Corsair uses cheaper OEMs (often CWT) for the CX line vs. Seasonic/Flextronics platforms for the RM/RMx series — cheaper transformers and inductors are less likely to be dipped/varnished properly, which is the actual root cause of whine (loose windings = free vibration).

## How to finish the isolation (do this before you build the new rig / decide on RMA)

```bash
# You can't run commands on a PSU, but here's the manual bisection procedure:

# 1. Isolate PSU from motherboard entirely
#    - Boot PSU alone with a "paperclip test" (short green wire PS_ON to black GND on 24-pin)
#    - Attach only a spinning HDD or a resistive load (old GPU works) as load
#    - Listen: if it still whines under load with NOTHING else connected to a board,
#      it's 100% confirmed PSU-side.

# 2. If step 1 is silent, reconnect motherboard but remove all GPUs
#    - Boot to BIOS with iGPU or no GPU
#    - Stress CPU: `stress-ng --cpu 24 --timeout 60s` (if you have a live USB/Linux)
#      or just let it idle in BIOS — VRM whine often appears under CPU load, not idle
#    - If whine appears here, it's motherboard VRM (B760M Mortar uses a fairly
#      basic 6+2+1 phase design — plausible under 13900KF's high transient draw)

# 3. Cross-check with a cardboard box isolation trick (used in real forum diagnostics):
#    - Physically remove PSU from case, run it externally, on a shelf, no metal contact
#    - This kills case resonance/rattle as a false-positive source
```

The forum reports converge on this same protocol — disconnecting components one at a time and physically removing the PSU from the chassis to run it in isolation is the standard way people confirm PSU-origin buzzing, since case panels and drive cages can resonate and make you misattribute the source.

## Verdict on your parts list

Your build is solid overall — i9-13900KF + RTX 4070 + 64GB DDR5-6000 is well-balanced for your ML/dev workload, and the AIO + case choices are fine. The one component I'd flag given your actual symptom:

**Corsair CX650F (398 CNY, 80+ Bronze)** — given it's already showing up as a documented whine offender for your exact model, and you're about to build a *new* i9-13900KF rig, I'd upgrade to the **Corsair RM650x / RM750e** class (Seasonic-adjacent platform, 80+ Gold, ~150-200 CNY more) or a **Super Flower Leadex / FSP Hydro Ti** equivalent. At your price point the delta is small (~500-700 CNY) relative to a 13900KF's transient current spikes (P-cores can pull 250W+ momentarily under all-core boost) — a cheap Bronze unit's switching inductors are exactly what gets stressed hardest by that CPU's power profile, so you're more likely to reproduce the exact whine you're currently debugging on your old rig, just louder.

Given you're 12,000+ tokens/month into GPU compute work and running the box near-continuously for training, I'd treat "silent under sustained load" as a real spec, not an afterthought — a whining PSU under 8+ hour training runs is the kind of low-grade friction that erodes focus over months.

References:

- [Corsair cx-650f psu coil whine and efficiency question - Tom's Hardware Forum](https://forums.tomshardware.com/threads/corsair-cx-650f-psu-coil-whine-and-efficiency-question.3794407/)
- [Corsair cx650m power supply making noise - Tom's Hardware Forum](https://forums.tomshardware.com/threads/corsair-cx650m-power-supply-making-noise.3339565/)
- [PSU making noise (CX650F) - Tom's Hardware Forum](https://forums.tomshardware.com/threads/psu-making-noise.3725276/)
- [Coil whine/buzzing from new Corsair PSU - Tom's Hardware Forum](https://forums.tomshardware.com/threads/coil-whine-buzzing-from-new-corsair-psu.3803602/)
