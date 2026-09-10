---
audio: false
generated: true
image: false
lang: en
layout: post
title: i5-6500 Integrated GPU for Testing
translated: false
type: note
---

Question: Does the **Intel Core i5-6500** have an integrated GPU?

Answer: **Yes.** The i5-6500 (6th-gen Skylake) has an integrated GPU:

* **iGPU:** Intel HD Graphics 530
* **Execution Units:** 24 EUs
* **Base frequency:** ~350 MHz
* **Max dynamic frequency:** ~1.05 GHz
* **Video outputs:** depends on the motherboard (HDMI/DVI/DP/VGA)
* **VRAM:** uses system RAM dynamically; it doesn't have dedicated VRAM.

So if you're using an i5-6500 motherboard as a **GPU repair/test bench**, you can remove the discrete GPU and use the motherboard's video output to boot the system and test the PCIe GPU separately.

For example:

```text
i5-6500
   │
   └── HD Graphics 530
           │
           └── motherboard HDMI/DP/DVI/VGA
```

One important detail: **the motherboard must actually expose a video output**. The CPU has the iGPU, but a motherboard without display connectors can't use it directly.

I can also show you a good **i5-6500 + cheap H110/B150 motherboard setup for GPU repair testing**.