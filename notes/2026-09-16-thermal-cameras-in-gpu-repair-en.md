---
audio: false
generated: true
image: false
lang: en
layout: post
title: Thermal Cameras in GPU Repair
translated: false
type: note
---

Question: Do GPU repair technicians use thermal cameras to diagnose/test GPUs such as the RTX 4070?

Answer: Yes. **Thermal imaging is a very common diagnostic tool for board-level GPU repair**, especially when the card has a short, abnormal power draw, or a component overheating.

For an RTX 4070-class card, a technician might use a thermal camera to find:

* **Shorted MLCC/capacitors** — one capacitor or power rail gets noticeably hotter.
* **Bad MOSFETs / VRM stages** — abnormal hotspot around the GPU/memory power circuitry.
* **Shorted GPU core or memory rail** — useful for locating which power rail is problematic.
* **Bad GDDR6X/GDDR6 memory chips** — one chip can run substantially hotter than neighboring chips.
* **Poor heatsink contact / thermal paste or pad problems** — GPU hotspot temperature becomes abnormal.
* **Cracked solder joints / damaged components** — sometimes visible indirectly through abnormal heat distribution.
* **VRM imbalance** — compare temperatures across inductors/MOSFETs under load.

A typical workflow is roughly:

```text
GPU doesn't work
      │
      ├── Measure resistance on power rails
      │
      ├── Check power consumption
      │
      ├── Power board / inject voltage if appropriate
      │
      └── Thermal camera
             │
             ├── Find abnormal hotspot
             ├── Identify component / rail
             └── Replace / rework component
```

The important distinction is **diagnosis vs. testing**.

### For repair

Thermal cameras are extremely useful because a failed component often converts electrical energy into heat:

```text
I²R loss → heat → thermal camera sees hotspot
```

For example, suppose a 1.0 V rail is shorted and the repair tech injects 1 A:

```text
P = V × I = 1.0 W
```

If most of that 1 W is dissipated by one tiny capacitor or IC, it can become an obvious thermal hotspot.

Technicians sometimes use **IPA/alcohol or freeze spray** in combination with a thermal camera. Alcohol evaporates faster from the hottest component; freeze spray can reveal where heat returns first.

### For normal GPU testing

Thermal cameras are also useful, but less essential.

You can run something like:

```bash
# stress GPU
gpu-burn
```

or a benchmark/stress test while watching:

```text
GPU core
GPU hotspot
VRAM
VRM
inductors
MOSFETs
PCB
```

A healthy board generally has a relatively understandable thermal pattern. A single component that is dramatically hotter than its peers is suspicious.

For example:

```text
Normal:

VRM:  █████████
      ████████
      ████████


Suspicious:

VRM:  ████████
      ████████
      █████████████████  ← abnormal MOSFET
```

### But thermal camera ≠ magic GPU tester

This is important.

A thermal camera **doesn't tell you that a GPU is electrically healthy**. It only shows surface temperature/emissivity.

For serious RTX 4070 repair, you'd normally combine:

```text
Multimeter
    +
Oscilloscope
    +
Bench PSU
    +
Thermal camera
    +
GPU diagnostic software
```

The thermal camera becomes particularly valuable when you already know **something is electrically wrong and need to locate the physical source**.

If you're thinking about buying one for GPU repair, I can also compare **cheap $200–500 thermal cameras vs. FLIR/HIKMICRO/UNI-T**, and explain what resolution/thermal sensitivity actually matters for finding tiny GPU-board shorts.
