---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-haiku
title: 1000Base-SX Uses Multi-Mode Fiber
translated: false
type: note
---

Thank you for sharing this question. Let me explain why the correct answer is **C (Multi-mode Fiber)** instead of B.

## Understanding 1000Base-SX Standard

The components of **1000Base-SX**:
- **1000** = 1 Gigabit/s (one billion bits per second)
- **Base** = Baseband transmission
- **SX** = Short wavelength

## Key Difference: SX vs LX

There are two main optical fiber versions for 1000Base Ethernet:

**1000Base-SX (Short Wavelength)**
- Wavelength: 850 nm
- Transmission medium: **Multi-mode Fiber**
- Maximum distance: 275m (full-duplex) or 550m (half-duplex)
- Lower cost, suitable for short-range applications

**1000Base-LX (Long Wavelength)**
- Wavelength: 1310 nm
- Transmission medium: **Single-mode Fiber**
- Maximum distance: 5 km
- Higher cost, suitable for long-distance applications

## Why Does SX Use Multi-mode Fiber?

The characteristics of short-wavelength lasers (850 nm) determine compatibility with multi-mode fiber:
- Modal dispersion in multi-mode fiber is relatively small at 850 nm
- More cost-effective and power-efficient
- Ideal for campus networks and data centers with medium to short-distance transmission

Single-mode fiber is optimized for long wavelengths (1310 nm) and supports much greater transmission distances.

**Quick Memory Aid: SX = Short wavelength = Multi-mode fiber; LX = Long wavelength = Single-mode fiber**
