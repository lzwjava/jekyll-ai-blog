---
audio: false
generated: true
image: false
lang: en
layout: post
title: Cold GPU Die VCore Fix
translated: false
type: note
---

Right — cold die confirms **VCore is never coming up**. The 12V input is fine, but the core voltage stage isn't running. Here's the complete roadmap, in order, with exact "pass/fail" decisions:

## Where we are

```
✅ 12V input present (8-pin + R005 = 12.3V)
❌ Die cold → VCore not generated
❓ 5V / 3.3V rails — NOT YET CONFIRMED
❓ VCore inductor voltage — NOT YET MEASURED
```

---

## Step 1 — Check the 5V and 3.3V rails (do this first)

The VRM controller needs a low-voltage supply to even think about switching. If 5V/3.3V is dead, VCore can never start.

| Test point | Expect | 
|-----------|--------|
| **BIOS chip pin 8** (small 8-pin SOIC near PCIe fingers) | **3.3 V** |
| **5V buck inductor** (near video outputs) | **5 V** |

- **If 5V/3.3V missing** → find and fix the 5V buck converter first. That's the root cause.
- **If 5V/3.3V OK** → go to Step 2.

---

## Step 2 — Measure VCore directly

Red probe on a **VCore inductor** (grey coil around the die), black on ground:

- **0 V** → VRM not switching → Step 3
- **12 V** → shorted high-side MOSFET → **stop testing, replace MOSFET/driver** (this can kill the die if left running)
- **0.6–1.1 V** → VCore IS running → then the cold die means the **GPU die itself is dead**

---

## Step 3 — Test the VRM controller (the brain)

Find the small IC near the VCore coils/MOSFETs (often **uP9512, NCP45491, IR35217, RT8816** style). Measure its:

1. **VCC pin** → expect **5V or 12V**
2. **EN (enable) pin** → expect **~3.3V**

| EN pin | VCC pin | Diagnosis |
|--------|---------|-----------|
| 0 V | OK | **GPU isn't commanding VCore** → fault upstream: BIOS chip, crystal/oscillator, reset circuit, or dead core |
| 3.3V | OK | **VRM controller or MOSFET/driver dead** → replace controller, check each phase's MOSFETs/driver |
| — | 0 V | Controller has **no supply** → fix the 5V/3.3V path first |

---

## Decision tree

```
Cold die
├─ 5V/3.3V missing?      → fix low-rail converter (root cause)
├─ 5V/3.3V OK, VCore=0V
│    ├─ EN=0V            → GPU not enabling core (BIOS/crystal/reset/dead core)
│    └─ EN=3.3V          → VRM controller/MOSFET/driver fault
└─ VCore=0.6-1.1V        → die itself dead (no repair, only reball/replace)
```

---

## Your next 3 measurements (report all 3)

1. **BIOS chip pin 8** → ? V
2. **5V inductor** → ? V
3. **VCore inductor** → ? V

With those three numbers I can tell you almost certainly which branch you're in. If you can also **read the VRM controller part number** (printed on the chip near the VCore coils), I'll give you the **exact pin numbers** for VCC and EN.