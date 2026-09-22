---
audio: false
generated: true
image: false
lang: en
layout: post
title: R005 Shunt and VCore Diagnosis
translated: false
type: note
---

`R005` is a **current-sense shunt resistor** — a 0.005 Ω (5 mΩ) low-value resistor used to measure the current flowing into a power rail. And **12.3 V across it** is a great sign. Here's what it tells us:

## What R005 means

- It sits **in series with a high-current rail** — on GA104 cards it's almost always the **12V input feeding the core VRM (VCore)**.
- **12.3 V at R005 = the 12V rail is reaching the VRM's high-side MOSFETs.** ✅

> Note: "across R005" — if you measured red on one side and black on the other, 12.3 V just confirms the 12V bus is live there (the *voltage drop* across a working 5 mΩ shunt would be only millivolts, so 12.3 V means you had one probe on 12V and the other on ground/other side).

## So the input power chain is healthy

```
PSU → 8-pin → 12V bus → R005 (12.3V ✅) → VRM high-side MOSFETs → ??? (VCore)
```

The fault is now confirmed to be **after this point** — the VRM isn't turning the 12V into VCore.

## Next test: the VCore inductors (the row of grey coils around the die)

1. **Black probe** → ground (mounting hole / bracket)
2. **Red probe** → each **VCore inductor** (the grey coils closest around the GPU die)
3. Meter on **20V DC**

**Interpretation:**

| Reading | Diagnosis |
|---------|-----------|
| **0.6 – 1.1 V** | VCore is running — die should be warm; fault is elsewhere (unlikely given cold die) |
| **0 V** | **VRM not switching** — controller/MOSFET/enable fault (most likely) |
| **12 V** | High-side MOSFET is shorted → VCore shorted to input (**danger**, could kill the die) |

## Also worth measuring while you're there

The **VRM controller chip** (small QFN/IC near the VCore MOSFETs — often **uP9512 / NCP45491 / IR35217** style):
- Its **VCC pin** → expect 5V or 12V
- Its **EN (enable) pin** → expect ~3.3V (this is the GPU's "turn on the core" command)

**If EN = 0 V → the GPU/BIOS isn't commanding VCore on** (upstream fault: BIOS, crystal, reset, or dead core).
**If EN = 3.3 V but VCore = 0 V → the VRM controller or a MOSFET/driver is dead.**

---

Go measure the **VCore inductor voltage** and report back. That single number splits the whole diagnosis in half.