---
audio: false
generated: true
image: false
lang: en
layout: post
title: G-Force Radar Meter
translated: false
type: note
---

This is a **G-force meter / accelerometer gadget** — a small handheld device that measures and displays acceleration forces.

Reading the orange LCD:

- **Circular radar plot** (left) — a 2D scatter/crosshair showing G-force direction on X/Y axes, scaled `-2 ... -1 ... 1 ... 2` (i.e. ±2G range). The center dot marks current/resting position.
- **MAX GFORCE** — the peak acceleration recorded.
- **0.51** — the max G-force value measured (0.51G).
- **→ AA** — directional/axis indicator (likely the dominant axis or a label).

The hardware: it's mounted on a breadboard/dev board with a USB-C port and a blue side button — almost certainly a hobbyist/DIY build using an **MPU-6050 / ADXL345-class IMU** + a microcontroller (looks like a small dev board, possibly something like a Seeed XIAO, RP2040, or similar) driving a monochrome LCD. The orange backlight is a classic STN/segment-style LCD.

These are popular as:
- **Car/motorsport telemetry toys** (measure cornering, braking, launch G's)
- **Maker projects** for learning IMU sensor fusion
- **EDC fidget gadgets** in the hobbyist electronics scene

If you want, I can sketch the minimal firmware to build one — read an MPU-6050 over I²C, compute the resultant G vector, track max magnitude, and render the radar plot. It's ~80 lines of MicroPython or Arduino C. Want it?
