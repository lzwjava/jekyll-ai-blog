---
audio: false
generated: true
image: false
lang: en
layout: post
title: Colorful RTX 5060 Ti 16GB Review
translated: false
type: note
---

Question: What is this card — 七彩虹 (Colorful) iGame GeForce RTX 5060 Ti Ultra OC 16GB GDDR7?

Answer:

It's Colorful's mid-range Blackwell card, GB206 die, aimed at 1440p gaming. Note: it's actually **DLSS 4** (Multi Frame Gen + transformer-model Super Res/Ray Reconstruction), not "DLSS 4.5" — that number in the listing is marketing fluff, no such official version exists.

**Silicon**

- GPU: GB206 (Blackwell 2.0), 4N process, 181mm², 21.9B transistors
- CUDA cores: 4608, RT cores: 36, Tensor cores: 144
- Clocks: base 2407MHz / boost 2572MHz stock, 2632MHz with one-click OC
- FP32: ~24.3 TFLOPS

**Memory**

- 16GB GDDR7, 128-bit bus, 28Gbps effective, 448 GB/s peak bandwidth
- This is the important differentiator vs the 8GB SKU — 128-bit bus is narrow but GDDR7 speed compensates

**Power/thermals**

- TDP 180W, single 8-pin power connector, suggested PSU 600W (some listings say 450W min — 600W is the conservative Colorful number)
- Triple-fan cooler, 2.5-slot, 300.5×120×50mm, 0.97kg

**Outputs**

- 3×DisplayPort 2.1b + 1×HDMI 2.1b

**Perf context** — ~75% faster than RTX 3060 at 1440p, ~26% faster than RTX 4060 Ti, but still falls short of RTX 4070, with RTX 5070 being ~27% faster. So: solid 1440p card, not a 4070 killer.

For your use case — if you're thinking of this as a cheap local-inference box: 16GB VRAM at 448GB/s bandwidth on a 128-bit bus is workable for small quantized models (7B-13B Q4/Q5) but bandwidth-starved compared to something like a used 3090 (936GB/s, 24GB). Fine for inference testing, not great for training/fine-tuning throughput.

References:

- [BenchGame — Colorful iGame RTX 5060 Ti Ultra W 16GB specs](https://benchgame.com/graphics-card/colorful-igame-rtx-5060-ti-ultra-w-16-gb)
- [TweakTown review](https://www.tweaktown.com/reviews/11042/colorful-igame-geforce-rtx-5060-ti-ultra-oc-style-meets-great-performance/index.html)
- [DataBlitz product page — full spec sheet](https://ecommerce.datablitz.com.ph/products/colorful-igame-geforce-rtx-5060-ti-ultra-w-oc-16gb-v-gddr7-graphics-card)
