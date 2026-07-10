---
audio: false
generated: true
image: false
lang: en
layout: post
title: Diagnosing Buzzing After GPU Swap
translated: false
type: note
---

**Question:** After swapping out the RTX 4070 and installing an AMD Instinct MI50, the system now makes an electrical "zizi" (buzzing/sizzling) sound while powered on, and the sound stops as soon as it's powered off. How do I diagnose and fix this?

**Answer:**

Treat this as a safety triage first, then a diagnostic isolation problem. "Buzzing that starts at power-on and stops at power-off" has two very different root causes that sound almost identical to a human ear but have very different risk levels:

### 1. Immediate safety check (do this before anything else)

- Power off, unplug from the wall, and physically inspect the PCIe power connector pins (both the PSU-side and GPU-side) for discoloration, melting, or a burnt-plastic smell. A `<PASSWORD>`-style redaction doesn't apply here, but the same caution applies to physical inspection — don't skip it.
- Check that every 8-pin PCIe connector is **fully seated** — a half-inserted connector under 150–300W load is the single most common cause of a literal frying/arcing sound (not coil whine) after a card swap. This is different from coil whine — arcing is dangerous and can damage the connector or start a fire if left running.
- If you smell anything burnt or see any discoloration, do not power the system on again until you've replaced that cable.

If nothing is burnt and the pins look clean, it's very likely **coil whine**, not arcing — see below.

### 2. Understand what "coil whine" actually is

Coil whine comes from the inductors in a VRM (voltage regulator module) — either on the motherboard, the GPU, or inside the PSU. When current switches at high frequency through the coil's copper winding, the winding physically vibrates (magnetostriction) at a frequency that can fall in the audible range (2–20 kHz). This is an electromechanical resonance effect, not a fault per se — but it's much more common under specific current draw patterns.

Why swapping in the MI50 would suddenly trigger it:

- **The MI50 is a passively cooled server card.** The Instinct MI50 uses a passive cooling solution with no cooling fans, relying on 6-pin and 8-pin PCIe power connectors and a 300W TDP. Without forced airflow (server chassis normally blast air through it), it can behave erratically under thermal throttling in a desktop case — which changes its power draw pattern moment-to-moment, and *that* transient switching is exactly what triggers coil whine.
- **Idle power draw is different from a 4070.** HBM2 on the MI50 doesn't idle down as aggressively as GDDR6X on consumer cards. A sustained, slightly-higher-than-expected idle load through the PSU's 12V rail is a classic trigger for PSU-side coil whine on cheaper VRM designs (your CX650F is a decent unit, but not immune).
- **Power connector type matters.** The retail MI50 is specced as 300W with a 2x 8-pin PCIe power configuration, though some sources list 6-pin+8-pin, so confirm which your specific card uses — using the wrong PSU cable (e.g., a CPU EPS 8-pin instead of PCIe 8-pin, which have the same connector shape but different pinouts on some PSUs) can cause voltage irregularities that manifest as buzzing under load, even if it boots fine.

### 3. Isolate the source (systematic, ~10 minutes)

```bash
# Step 1: swap MI50 out, put ANY other GPU (or nothing, use onboard/no display) back in
# Power on, listen. If silent → confirmed GPU or its power delivery is the source.
# If still buzzing → it's the motherboard VRM or PSU, unrelated to the MI50 itself.

# Step 2: with MI50 installed, disconnect one of the two 8-pin cables at a time
# (system won't boot properly, that's fine — you're just listening for the noise
# during the brief power-on before it fails to POST)
# This isolates which specific power rail/cable is resonating.

# Step 3: try a different PCIe power cable/cable route from the PSU
# (different cable = different physical routing = different resonance point)
```

### 4. Fixes, in order of how likely they are to work

1. **Re-seat every connector firmly** — this alone fixes ~50% of "new noise after a swap" cases, especially if you handled cables during the RTX 4070 removal.
2. **Add airflow across the MI50** — since it's passive, a case fan or even a clip-on blower directly over the heatsink stabilizes its power draw curve and often kills the whine within minutes of the GPU no longer thermal-cycling.
3. **Try different PCIe cables from the PSU**, not just a different port — coil whine is routing- and cable-length-sensitive.
4. **Cap the MI50's power via ROCm/rocm-smi** if it's a driver-level fluctuation issue:
```bash
sudo rocm-smi --setpoweroverdrive 250   # cap to 250W instead of 300W
sudo rocm-smi --setperflevel high        # or 'auto' — test both
```
   Locking the power state instead of letting it dynamically clock can remove the transient switching that causes whine.
5. **If it persists and is loud/annoying but nothing is burnt** — it's cosmetic coil whine, common on used enterprise cards, and not damaging. Many MI50 units bought secondhand exhibit this simply from years of datacenter duty cycling.

### 5. One more thing worth checking given your workflow

You mentioned disassembling the RTX 4070 and handling the MI50 by hand. If you weren't grounded (no anti-static wrist strap, no touching a grounded metal chassis first), it's possible you introduced a small ESD event into the VRM MOSFETs on either card — this can cause exactly this kind of high-pitched buzz as a partially damaged switching MOSFET behaves erratically, distinct from harmless coil whine (which is steady and doesn't change pitch). If the noise is inconsistent, changes pitch, or gets worse over a few days, that's your signal to stop using that card and bench-test it in isolation (different PSU, different board) before trusting it under sustained ML workloads.

Given you're about to hammer this MI50 with actual training runs (16GB HBM2, sustained near-300W loads for hours), I'd resolve this now rather than defer — arcing/ESD damage under sustained heavy load is a much bigger risk than at idle.

**References:**

- [AMD Radeon Instinct MI50 Specs — TechPowerUp](https://www.techpowerup.com/gpu-specs/radeon-instinct-mi50.c3335)
- [AMD Radeon Instinct MI50 GPU — IT Creations](https://www.itcreations.com/amd-gpu/amd-radeon-instinct-mi50-gpu)
- [AMD RADEON INSTINCT MI50 GPU — Servershop24](https://www.servershop24.de/en/amd-radeon-instinct-mi50-gpu/a-133803/)
- [AMD Claims First 7nm GPUs With Radeon Instinct MI60, MI50 — Tom's Hardware](https://www.tomshardware.com/news/amd-radeon-instinct-mi60-mi50-7nm-gpus,38031.html)
