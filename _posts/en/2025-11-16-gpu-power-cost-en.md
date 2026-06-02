---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: GPU Power Consumption and Cost Estimate
translated: false
type: note
---

Using the number shown in your output:

Your GPU is pulling **about 205 watts** during the run.

A “degree of electricity” = **1 kWh**.

**If only the GPU were counted:**

* **1 hour:** 205 W ≈ **0.205 kWh**
* **24 hours:** 0.205 × 24 ≈ **4.92 kWh**

However, a real machine also includes CPU, motherboard, RAM, fans, SSD, PSU losses, etc.
A typical training rig with a 4070 usually draws **300–380 W total** at the wall.

If we use a more realistic whole-system estimate, say around **320 W** average:

* **1 hour:** 0.32 kWh
* **24 hours:** 7.68 kWh

If your workload keeps the GPU at 100% the whole time, expect your actual bill to fall in that whole-system range rather than the GPU-only number.

If you want, you can tell me your PSU model, CPU type, and how many fans/disks, and I can estimate it more accurately.
