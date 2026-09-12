---
audio: false
generated: true
image: false
lang: en
layout: post
title: MODS Cannot Help a Dead Card
translated: false
type: note
---

If there's **no fan spin, no lights** — that's a **dead card** at the power-on level. MODS likely **won't help** in this case, because MODS is a software diagnostic that requires the GPU to be alive and communicating via PCIe.

Here's a breakdown:

## Can MODS help with a dead card?

**No.** MODS cannot help if:
- The GPU isn't detected by the system BIOS/PCIe
- The card doesn't power up at all
- No fan spin, no LEDs

MODS requires the GPU to be initialized (by VBIOS) and communicating over PCIe. If the card is truly "dead" (no power-on behavior), MODS has nothing to talk to.

## What to check first (hardware-level)

Since you said the PCB isn't burned and the device looks physically fine, here's the likely culprits:

**1. Power delivery failure (most common)**
- Check if the **PCIe power cables** (6-pin/8-pin) are properly seated — try different cables from the PSU
- Try a **different PSU** — the card might need more power than the current PSU can deliver
- Check the PSU's 12V rail with a multimeter

**2. Short circuit on the PCB**
- Even if no visible burn marks, there could be a short on the **VRM (voltage regulator module)** — check MOSFETs and capacitors with a multimeter in diode mode
- Measure resistance between 12V PCIe pins and ground — anything under ~100 ohms indicates a short

**3. VBIOS corruption**
- If the VBIOS is corrupted, the card may not initialize
- Some cards support **dual BIOS** — try flipping the switch (if present)
- You can try reflashing the VBIOS using another working GPU (but that requires the card to at least be detected)

**4. GPU core / memory failure**
- Cold or cracked solder joints under the GPU core or memory chips (BGA)
- This typically requires **reballing** or **reflowing** — not something MODS can diagnose

**5. Simple fixes to try first**
- **Reseat the card** in a different PCIe slot
- **Clear CMOS** (reset BIOS to defaults)
- Try the card in a **completely different system**
- Check if the fan connector on the PCB is plugged in properly

## If the card is detected by BIOS but still has issues

Once the card shows *some* sign of life (fan spins briefly, detected in BIOS), then MODS can help diagnose:
- Memory errors (MODS tests like MarchTest, Mats)
- VRAM channel failures
- GPU core compute failures
- Register read/write verification

## Quick diagnostic flow

```
Card appears dead (no fan, no lights)
        │
        ▼
Is it detected by BIOS? (beeps, POST codes?)
   ├── No  → Hardware issue (power, VRM, short, VBIOS)
   │         MODS cannot help here
   │
   └── Yes → MODS can help diagnose further
             Run: mods gputest.js -mfg
             Check error codes for specific failures
```

**TL;DR:** For a completely dead card with no fan spin, MODS won't help. Focus on **PSU testing, multimeter checks on power rails/VRMs, and trying the card in another system** first.
