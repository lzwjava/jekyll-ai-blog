---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-haiku
title: Fiber Optic Signal Spreading Explained
translated: false
type: note
---

**Dispersion** in fiber optics refers to the **spreading out of a light signal** as it travels through the fiber, which causes the signal to become distorted and weaker.

Think of it like this: when you send a pulse of light down a fiber, different components of that light travel at slightly different speeds. By the time the signal reaches the other end, what was once a sharp, clean pulse has become stretched out and blurry—like watching ink diffuse through water.

**There are two main types:**

**Chromatic Dispersion** - Different wavelengths (colors) of light travel at different speeds through the fiber. A pulse containing multiple wavelengths spreads out because each wavelength arrives at slightly different times.

**Modal Dispersion** - In multi-mode fiber (like 1000Base-SX uses), light can take multiple paths through the fiber. Each path travels a slightly different distance, so light taking different modes arrives at different times, causing the signal to spread.

**Why it matters for 1000Base-SX:**

The 275m full-duplex limit exists partly because of dispersion. Over longer distances, the signal spreads so much that:

- Pulses overlap with each other
- The receiver can't distinguish between 1s and 0s clearly
- Bit errors increase

Multi-mode fiber has worse dispersion than single-mode fiber, which is why 1000Base-SX has a shorter range (275m) compared to single-mode alternatives like 1000Base-LX (up to 10km).
