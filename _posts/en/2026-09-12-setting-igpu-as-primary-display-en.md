---
audio: false
generated: true
image: false
lang: en
layout: post
title: Setting iGPU as Primary Display
translated: false
type: note
---

Question: In an AMI BIOS on a Huanan B75, how do you make the **integrated GPU (iGPU)** the primary display instead of the discrete GPU?

Answer:

On B75 boards, look in BIOS for a setting such as:

```text
Advanced
  → Chipset Configuration
      → Primary Display
      → Initiate Graphic Adapter
      → IGD / PEG / PCI
```

The exact name varies with the Huanan BIOS version.

Typical values:

```text
IGD   = Integrated Graphics / Intel iGPU
PEG   = PCI Express Graphics / discrete GPU
PCI   = legacy PCI graphics
```

So you want:

```text
Primary Display / Initiate Graphic Adapter = IGD
```

Then:

```text
F10 → Save & Exit → Yes
```

### Important for your B75 + Xeon setup

If you're using a **Xeon E3-12xx**, check the exact model first. Many Xeon E3 CPUs **do not have an integrated GPU**.

For example:

```text
E3-1230 / E3-1230 v2 → no iGPU
E3-1260L / E3-1260L v2 → Intel HD Graphics
```

If the CPU has no iGPU, selecting `IGD` won't give you video output.

Also, after selecting IGD, connect your monitor to the **motherboard's video output**, not the discrete GPU:

```text
CPU iGPU
   ↓
B75 motherboard HDMI / DVI / VGA
   ↓
Monitor
```

If you show me a photo of your **exact Huanan B75 BIOS screen**, I can tell you exactly which menu/item to change.
