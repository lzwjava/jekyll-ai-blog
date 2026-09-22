---
audio: false
generated: true
image: false
lang: en
layout: post
title: Cold Die VCore Fault
translated: false
type: note
---

Good — that symptom narrows it down a lot. **A cold die = the GPU core rail (VCore/VDDC) is never coming up.** If VCore were on, the die would warm even with no display. So the fault is almost certainly in the power path *before* the core.

Here's the exact test sequence for a GA104 card (RTX 3060 Ti/3070), from input to core:

---

## Step 1 — Power OFF, check for shorts (resistance/continuity mode)

This is the most important first test. A dead short on any rail will keep the card from powering up.

| Test point | Expected | Fault if |
|-----------|----------|----------|
| **12V input** (8-pin + PCIe 12V pins) to ground | ~500 Ω – several kΩ | near 0 Ω = shorted high-side MOSFET or cap |
| **VCore (VDDC)** rail — big inductors around the die | **very low Ω (0.5–2 Ω)** is *normal* for GPU core | 0.0 Ω = dead short; 10+ Ω could be fine |
| **VMEM (VRAM)** inductors | ~10–100 Ω | 0 Ω = shorted VRAM/MOSFET |
| **5V / 3.3V / 1.8V** rails | ~kΩ | 0 Ω = short |

> ⚠️ VCore is normally very low resistance because the die draws huge current. Don't mistake 1 Ω for a short.

---

## Step 2 — Power ON, measure in DC volts (this is where your fault will show)

Check in this exact order:

### A. Input power present?
1. **12V on the 8-pin PCIe power connector** → expect **12 V**
2. **12V on PCIe slot pins** → expect **12 V**
3. **5V and 3.3V** present on the board → expect **5 V / 3.3 V**

If 12V is missing → power supply/cable/fuse problem. If 12V is present but nothing else → go to B.

### B. Standby / low rails
4. **5V** rail → expect **5.0 V**
5. **3.3V** rail → expect **3.3 V**
6. **1.8V** rail (often near the BIOS chip / memory) → expect **1.8 V**

### C. The critical one — VRAM and VCore
7. **VMEM (VRAM)** inductors → expect **1.35 V** (GDDR6)
8. **VCore (VDDC)** inductors around the die → expect **0.6–1.1 V** (rises at boot)

**If VMEM is present but VCore = 0 V → the VRM is not starting.** This is the classic "cold die" fault.

---

## Step 3 — If VCore = 0 V, test the VRM controller

The core VRM controller (often **uP9512 / NCP45491 / IR35217** style on GA104 boards) needs:

1. **VCC** (controller supply, usually 5V or 12V) → present?
2. **EN / EN_VCORE** (enable pin) → expect **~3.3 V** (this is the "turn on core" signal from the GPU/BIOS)
3. **PGOOD / PowerOK** output → should be high once running

**Key diagnostic:** if EN is **0 V**, the GPU/BIOS is *not commanding* the core to turn on → problem is upstream (BIOS, crystal, reset, or the die itself). If EN is **3.3 V** but no VCore → the VRM controller or a MOSFET/driver is dead.

---

## Quick decision tree

```
Power on, die cold
├─ No 12V input          → PSU / cable / fuse
├─ No 5V / 3.3V          → low-rail converter dead
├─ 5V/3.3V OK, no VMEM   → VRAM VRM or its enable
├─ VMEM OK, no VCore     → core VRM: check controller VCC + EN + MOSFETs
└─ VCore present but die cold → die itself dead (rare) or VRM not delivering under load
```

---

## What to tell me next

Measure these and give me the numbers:
1. **12V** at the 8-pin input
2. **5V and 3.3V**
3. **1.8V**
4. **VMEM** (inductor near VRAM)
5. **VCore** (inductor around the die)
6. **EN** on the core VRM controller (if you can identify the controller chip)

I'll cross-reference against GA104 expectations and pinpoint whether it's the **VRM controller, a MOSFET, or the enable signal** that's dead.