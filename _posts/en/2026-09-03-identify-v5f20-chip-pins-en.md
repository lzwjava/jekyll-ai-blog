---
audio: false
generated: true
image: false
lang: en
layout: post
title: Identify V5F20 Chip Pins
translated: false
type: note
---

Question: What are the **5 pins of the V5F20 chip** on the Quadro 410?

Answer: I don't want to guess the pinout from `V5F20` alone. That is a **top-marking**, and several different 5-pin regulator families can use similar markings.

If this is a 5-pin **voltage regulator**, the five functions are commonly some combination of:

```text
        ┌─────────────┐
 VIN ──►│ 1         5 │◄── EN / FB / NC
 GND ──►│ 2       4   │
 SW/OUT ►│ 3          │
        └─────────────┘
```

But **the exact assignment of pins 1–5 is chip-specific**. For GPU repair, getting one pin wrong can short a power rail.

### We can identify it experimentally

With the Quadro **unpowered**:

1. Put the black probe on a known **GND** point.
2. Use continuity mode to determine which V5F20 pin connects to ground.
3. Trace the other pins to:

   * an **inductor** → likely switching/output path
   * a large capacitor → power rail
   * resistor network → likely FB/EN
   * input power → VIN

Then with the board powered, we can measure each pin's DC voltage.

**Send me a close-up photo of the V5F20 and the components immediately around it.** I can identify the 5 physical pins and trace where each one goes on your actual Quadro 410 PCB.
