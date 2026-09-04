---
audio: false
generated: true
image: false
lang: en
layout: post
title: "PCIe x16: Lanes, Not Bits"
translated: false
type: note
---

**Question:** Is the "x16" in PCIe x16 referring to bits?

**Answer:**

No — the "x16" refers to the number of **lanes**, not bits.

Here's how it works:

- **"x"** stands for "by" (as in "by 16")
- **Each lane** is a separate high-speed serial connection that carries data in both directions simultaneously
- **More lanes = more bandwidth**

| Slot | Lanes | Approx. Bandwidth (PCIe 3.0) |
|---|---|---|
| PCIe x1 | 1 lane | ~1 GB/s |
| PCIe x4 | 4 lanes | ~4 GB/s |
| PCIe x8 | 8 lanes | ~8 GB/s |
| PCIe x16 | 16 lanes | ~16 GB/s |

**Key points:**
- PCIe x16 is the **largest and fastest** standard slot, used almost exclusively for **dedicated GPUs (graphics cards)**
- Each lane itself uses multiple bits internally, but the "x16" number is purely about lane count
- The ASUS H81M-K has **1x PCIe x16** slot, meaning it can fit one full-size graphics card

Think of lanes like **highway lanes** — x16 is a 16-lane highway, allowing much more traffic (data) to flow at once compared to a x1 single-lane road.
