---
audio: false
generated: true
image: false
lang: en
layout: post
title: Distinguishing GPU Core vs VRM Failure
translated: false
type: note
---

**Question:** How do you test whether a GPU failure is in the die (GPU core) vs. a MOSFET/VRM problem — and what are the common failure types and symptoms for Nvidia GPUs?

---

**Answer:**

## 🔬 How to Distinguish GPU Die Failure vs. MOSFET/VRM Failure

### Step 1 — Visual Inspection First

VRM-related failures are often immediately apparent by physical damage — a blown MOSFET, overheated PCB area, burn marks — and spotting this upfront helps prioritize electrical testing. Look for:

- Scorched/darkened areas around the power delivery circuitry
- Swollen or cracked MOSFETs
- Burned inductors or capacitors

---

### Step 2 — Measure Power Rail Resistance & Voltage

Measuring resistance and voltage on GPU power rails provides immediate insight into short circuits, open circuits, or missing supply conditions. A shorted core or memory rail often indicates failed MOSFETs or internal GPU damage, while absent voltages may point to controller or enable-signal issues.

Use a multimeter:

- **Short to ground on the core rail** → shorted MOSFET or dead GPU core
- **Rail present but no output** → PWM controller / driver IC issue

---

### Step 3 — MOSFET Test (out-of-circuit preferred)

To test an N-channel MOSFET with an analog multimeter set to ×10K ohm range: place the black probe on the drain. Touch the gate with the red probe to pre-charge the gate capacitance. Then move the red probe to the source — the meter pointer should move to mid-scale. To discharge the FET, touch the gate pin once. Retouching source at that point should show no deflection. Those are good FET characteristics.

> ⚠️ Note: In-circuit tests are unreliable because all MOSFETs have a parasitic diode between drain and source, making a simple continuity test meaningless without controlling the gate voltage.

---

### Step 4 — The Critical "Inject Current" Test (Advanced)

A resistance test alone only catches obvious shorts. It's only when actual current is injected that a wounded GPU core reveals itself — the core heats up under injected current, confirming a dead die. This is a routine part of electronics repair: you may need to replace the MOSFET first to clear the 12V rail short, then re-test the GPU core separately to determine if it's salvageable.

This is the key diagnostic distinction:

| Test Result | Interpretation |
| --- | --- |
| Short clears after MOSFET replaced | **MOSFET failed**, GPU die may be OK |
| Core still heats up after MOSFET replaced | **GPU die is dead too** |
| Rail voltage missing, no physical damage | PWM/driver IC issue |

---

## 💥 Common Nvidia GPU Failure Modes & Symptoms

### 1. MOSFET / VRM Failure

- VRM-related failures are among the easiest GPU failures to repair, usually caused by shorted MOSFETs, dried/failed capacitors, or broken inductors — and they typically result in no power output (dead on arrival).
- **Symptom:** Fans spin, no display signal at all, sometimes burning smell

### 2. VRAM Failure

- VRAM chips (GDDR6/GDDR6X) failure is a common cause of artifacting, texture corruption, and application crashes. Defective VRAM produces repeatable visual patterns, colored blocks, or driver-level memory access errors, especially under load.
- **Symptom:** Checkerboard patterns, corrupted textures, BSOD with memory errors

### 3. GPU Core (Die) Failure

- Visual glitches, pixel trails, flashing colors, or checkerboard patterns that appear under load and progressively occur earlier in the boot process indicate failing VRAM or a degraded GPU core.
- **Symptom:** Progressive worsening artifacts → eventual black screen

### 4. Thermal / VRM Overload (Black screen under load)

- Some GPUs function normally at desktop but lose display output the moment they're stressed. This typically happens when the card overheats or power draw spikes beyond what the PSU or VRMs can support — strongly suggesting a thermal or power-delivery issue rather than a software glitch.
- **Test:** Run FurMark for 15–30 min. If the PC black-screens or restarts during FurMark, the GPU's power delivery phases or internal VRMs are failing under load.

---

## 📊 Failure Type Cheat Sheet

| Symptom | Most Likely Cause |
| --- | --- |
| No POST, no display, fans spin 100% | Dead MOSFET / VRM short |
| Artifacts then crash under load | VRAM or GPU die degradation |
| Black screen only under heavy load | VRM thermal/current overload |
| Works desktop, crashes in games | VRM weakness or early die failure |
| Physical burn/smell on PCB | Blown MOSFET (often secondary die damage) |
| Error Code 43 in Device Manager | BIOS corruption or core failure |

---

**References:**

- [GPU Repair & Fault Diagnosis Guide – Blikai](https://www.blikai.com/blog/components-parts/graphics-card-repair-gpu-components-fault-diagnosis-guide)
- [MOSFET Test Method – DigiKey Forum](https://forum.digikey.com/t/how-to-test-a-mosfet/1985)
- [RTX 4090 MOSFET + Dead Core Case Study – Yahoo/Tom's Hardware](https://tech.yahoo.com/computing/articles/gpu-surgeon-attempts-rescue-fatally-153540641.html)
- [GPU Failure Symptoms – ITU Online](https://www.ituonline.com/blogs/graphics-card-failures/)
- [FurMark VRM Stress Test Guide – PC Power Up](https://pcpowerup.co.uk/blogs/news/how-to-tell-if-your-graphics-card-is-failing-gpu-artifacts-stress-test-guide)
