---
audio: false
generated: true
image: false
lang: en
layout: post
title: Red Light, No Fan Fix
translated: false
type: note
---

**Question:** RTX 3060 GPU (ORFULL brand) — when power is supplied, the red LED flashes but the fans don't spin. How to fix this?

**Answer:**

There are two separate things happening here, and they point to different causes:

---

### 🔴 Red Light Flashing

The red flashing LED on an RTX 3060 typically indicates a **power delivery problem** — either a loose/faulty PCIe power cable, or an unstable/insufficient PSU voltage.

**Steps to fix the red light:**

1. **Reseat the PCIe power cable** — Unplug and firmly reconnect the 8-pin (or 6+2 pin) power connector to the GPU. Make sure it clicks in fully.
2. **Check your PSU wattage** — Verify that your PSU meets the GPU's wattage requirement, with at least 100W of headroom. The RTX 3060 recommends a **550W+ PSU**.
3. **Try a different power cable** — If your PSU has multiple 8-pin cables, swap to a different one.
4. **Full power cycle** — Cut the power completely for a few minutes to reset the lights, but watch whether they return after boot.
5. **Try a different PCIe slot** — Test the GPU in a different PCIe slot on the motherboard.

---

### 🌀 Fans Not Spinning

This is likely **normal behavior**, not a fault.

The RTX 3060 uses **Zero RPM Mode** — fans are intentionally designed not to spin at idle (below ~55–60°C). This reduces noise and extends fan life. Fans will activate once you launch a demanding game and temperatures climb.

**However**, if the red light is on *and* fans don't spin even under load, it could mean the GPU is not receiving proper power to operate at all.

---

### Summary Checklist

| Issue | Likely Cause | Fix |
|---|---|---|
| Red light flashing | Loose/bad PCIe power cable or weak PSU | Reseat cable, check PSU wattage |
| Fans not spinning (idle) | Normal Zero RPM mode | Load a game, fans should spin at ~60°C |
| Fans not spinning (under load) | Power failure / dead GPU | Reseat GPU, test in another system or RMA |

---

**References:**
- [GPU Fans Not Spinning? Causes, Fixes & When To Worry](https://gpubottleneckcalculator.com/blog/gpu-fans-not-spinning-causes-fixes/)
- [ASUS Strix 3060 Blinking Red Lights – ROG Forum](https://rog-forum.asus.com/t5/nvidia-graphics-cards/asus-strix-3060-oc-12gb-blinking-red-lights-about-pcie-power/td-p/900631)
- [GPU Has Blinking Red Light – Tom's Hardware](https://forums.tomshardware.com/threads/gpu-has-blinking-red-light.3754724/)
