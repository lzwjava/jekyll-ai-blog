---
audio: false
generated: true
image: false
lang: en
layout: post
title: Why Your MacBook Charges Slowly
translated: false
type: note
---

Let me break down your setup:

**What you have:**
- **Baseus GaN3 Lite** — a GaN charger, likely 30W-67W USB-C output. This is a solid third-party charger, not junk.
- **Romoss power strip** — 1 input, 3 output (USB hub/splitter)
- **Phone cable** (likely USB-A to USB-C) — charging a MacBook

**The bottleneck is the cable and routing:**

If you're going: **Wall → Baseus GaN3 Lite → Romoss → phone cable → MacBook**

The problem is the **phone cable**. Here's why:

- USB-A cables **cannot negotiate USB-C Power Delivery (PD)**, which is what MacBooks need
- A USB-A to USB-C cable will cap at **5V × 2.4A = ~12W max**, regardless of how powerful the charger is
- Your MacBook's official charger is **30W-140W** depending on model
- At 12W, your MacBook will charge **very slowly** — maybe 10-15% per hour, or might even drain while using it

**What to check:**

1. **Does the Baseus GaN3 Lite have a USB-C port?** If yes, use a **USB-C to USB-C cable** directly from the charger to the Mac — skip the Romoss entirely. This will get you proper PD charging at 30W+.

2. **If you must use the Romoss**, check if it has a USB-C output port (not just USB-A). Use a USB-C to USB-C cable from that port.

3. **Phone cable = the real problem.** Even a cheap USB-C to USB-C cable will outperform a phone cable for laptop charging.

**Bottom line:** It'll work — your MacBook won't be damaged — but it'll charge painfully slowly. If you can get any USB-C to USB-C cable, even a cheap one, plug it directly into the Baseus charger's USB-C port and skip the Romoss. That alone could 3-5x your charging speed.
