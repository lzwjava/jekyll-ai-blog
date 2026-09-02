---
audio: false
generated: true
image: false
lang: en
layout: post
title: Interpreting GPU Fan Behavior
translated: false
type: note
---

Question: **If a GPU is plugged into a motherboard and the PC cannot start, with the GPU fan either not spinning or spinning, what does that tell you, and how do you troubleshoot it?**

Answer:

The **fan behavior is only a symptom**. It does *not* directly tell you whether the GPU core is good or bad.

A useful way to think about the failure is:

```text
PSU
 │
 ├── 12V PCIe power ──> GPU power stages ──> GPU core / VRAM
 │
 └── 12V/5V/3.3V ──> motherboard
                         │
                         └── PCIe slot ──> GPU
```

### 1. GPU plugged in → motherboard won't start at all

For example:

```text
Press power
    ↓
No POST
No display
Maybe motherboard won't even stay powered
```

This is a **strong suspicion of a power short**, especially if the system works normally after removing the GPU.

Typical causes:

* Shorted MLCC capacitor on GPU 12 V rail
* Shorted MOSFET / DrMOS
* Failed GPU VRM controller
* Shorted GPU core
* Shorted VRAM power rail
* Damaged PCIe slot/power connector
* Bad GPU causing PSU protection to trigger

First test:

```text
GPU removed:
    motherboard starts normally?

GPU installed:
    motherboard cannot start?

=> investigate GPU power/short circuit first
```

**Do not repeatedly power-cycle a board suspected of a hard short.**

---

### 2. GPU fan does NOT spin

This alone means almost nothing.

Many modern GPUs intentionally keep the fan stopped at idle:

```text
Power ON
   ↓
GPU initializes
   ↓
Temperature low
   ↓
Fan = 0 RPM
```

So:

> **Fan not spinning ≠ GPU dead**

Instead, measure the power rails.

With the GPU **powered off and disconnected**, use resistance/continuity measurements first.

For example:

```text
Black probe → GND
Red probe  → GPU power rail
```

Look for:

```text
12V input → suspiciously low resistance?
GPU core rail → very low resistance can be normal
VRAM rail → compare with a known-good card
3.3V rail → suspicious short?
```

The important point is that **you need to identify which rail you're measuring**. Don't interpret every low-ohm reading as a short.

---

### 3. GPU fan spins immediately at 100%

This is more interesting.

A common failure pattern is:

```text
Power ON
   ↓
GPU receives power
   ↓
GPU doesn't initialize
   ↓
Fan controller/default state → 100%
   ↓
No display / no POST
```

Possible causes include:

* GPU core not powered
* GPU BIOS/VBIOS problem
* GPU core failure
* VRAM failure
* Missing power rail
* VRM controller failure
* PCIe communication failure
* GPU overheating protection/failsafe behavior

But again:

> **100% fan does not prove the GPU core is dead.**

---

# The repair workflow I would use

For a cheap GT 630/GT 730, this is actually a great learning platform.

### Step 1 — Remove GPU

Confirm:

```text
Motherboard boots normally
BIOS accessible
CPU/iGPU/display works
```

Then install GPU again.

If the motherboard becomes completely dead only when the GPU is installed:

**start with resistance/short testing before powering it again.**

---

### Step 2 — Check GPU PCIe 12 V

With GPU installed and powered:

Set multimeter:

```text
DC voltage
```

Black:

```text
GND
```

Red:

```text
GPU 12V input
```

PCIe slot provides:

```text
12 V
3.3 V
```

If the card has a 6-pin/8-pin connector, measure the corresponding 12 V input there too.

You want approximately:

```text
12 V rail ≈ 12 V
3.3 V rail ≈ 3.3 V
```

If 12 V is completely missing, don't immediately blame the GPU core.

---

### Step 3 — Find the VRM stages

On a typical GPU:

```text
12V
 │
 ▼
[Input capacitors]
 │
 ▼
[High/Low-side MOSFETs]
 │
 ▼
[Inductor]
 │
 ▼
GPU Vcore
```

and separately:

```text
12V / 3.3V
 │
 ▼
VRM
 │
 ▼
VRAM voltage
 │
 ▼
Memory chips
```

This is where your multimeter becomes much more useful than looking at the fan.

---

### Step 4 — Measure the coils

This is one of the best beginner GPU-repair techniques.

Find the large inductors/coils around the GPU:

```text
       GPU
  ┌─────────────┐
  │             │
  └─────────────┘
    █ █ █ █
    ↑ ↑ ↑ ↑
   coils
```

With power **OFF**:

```text
Black → GND
Red → each coil
```

Record the readings.

With power **ON**, measure voltage on both sides.

For example:

```text
12V input
   ↓
MOSFET
   ↓
coil
   ↓
VCORE
```

If you have:

```text
12V present
VCORE = 0 V
```

then you have narrowed the problem substantially to the GPU VRM/control path.

---

### Step 5 — Compare good vs bad

This is probably the most valuable thing you can do while learning repair.

Get two identical/very similar cheap cards:

```text
GOOD GT 730
BAD  GT 730
```

Measure the same points:

```text
12V
3.3V
Vcore
VRAM
VRM MOSFETs
inductor resistance
PCIe rails
```

Make a table:

| Test point       | Good card | Bad card |
| ---------------- | --------: | -------: |
| 12V input        |      ~12V |        ? |
| 3.3V             |     ~3.3V |        ? |
| Vcore            |         ? |        ? |
| VRAM             |         ? |        ? |
| Vcore resistance |         ? |        ? |
| VRAM resistance  |         ? |        ? |

**This is much more informative than "fan spins / fan doesn't spin."**

If you upload a clear photo of the **front and back of the GPU PCB**, I can help you identify the PCIe 12 V/3.3 V paths, VRM coils, MOSFETs, controller ICs, and the exact multimeter points to probe.
