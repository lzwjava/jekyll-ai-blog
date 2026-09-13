---
audio: false
generated: true
image: false
lang: en
layout: post
title: GT 730 vs M60 Not Identical
translated: false
type: note
---

**Question:** How does the GT 730 compare to the Tesla M60, are they the same card, and does the GT 730 have a 384-bit memory bus?

**Answer:**

No, the GT 730 and Tesla M60 are **completely different cards** — not the same at all. And the GT 730 does **not** have a 384-bit memory bus. Here's the full breakdown:

---

### NVIDIA GeForce GT 730 — Memory Bus

The GT 730 actually comes in **three variants** with different bus widths, which causes a lot of confusion:

| Variant | GPU | CUDA Cores | Memory Bus |
| --- | --- | --- | --- |
| GT 730 DDR3 | GF108 (Fermi) | 96 | **128-bit** |
| GT 730 DDR3 | GK208 (Kepler) | 384 | **64-bit** |
| GT 730 GDDR5 | GK208 (Kepler) | 384 | **64-bit** |

The Fermi-based GT 730 (GF108) uses a **128-bit** memory bus with DDR3 memory.

The more common Kepler-based GT 730 (GK208) has 384 CUDA cores but uses only a **64-bit** memory interface, with 2 GB of DDR3 memory and 14.4 GB/s bandwidth.

**There is no GT 730 with a 384-bit bus.** That number (384) refers to its CUDA core count, not bus width — easy to mix up.

---

### NVIDIA Tesla M60 — A Completely Different Beast

The Tesla M60 is a dual-GPU server/virtualization accelerator based on the **Maxwell** architecture, featuring **4096 CUDA cores total** (2048 per GPU) and **16 GB of GDDR5** memory (8 GB per GPU).

Its memory interface is **256-bit per GPU** (512-bit total across both GPUs), with a memory bandwidth of **160.4 GB/s per GPU** (320 GB/s total).

It consumes up to **300W** and is designed for enterprise virtual workstations and desktops.

---

### GT 730 vs Tesla M60 — Side by Side

| Spec | GT 730 (best variant) | Tesla M60 (per GPU) |
| --- | --- | --- |
| Architecture | Kepler | Maxwell |
| CUDA Cores | 384 | 2048 |
| VRAM | 2 GB GDDR5 | 8 GB GDDR5 |
| Memory Bus | 64-bit | 256-bit |
| Bandwidth | ~14–28 GB/s | ~160 GB/s |
| Use Case | Budget desktop | Data center / vGPU |
| TDP | ~23–49W | 300W (whole card) |

They share **no similarity** — the M60 is a professional dual-GPU data center card, while the GT 730 is a low-end consumer desktop card from a different era and architecture.

**References:**

- [VideoCardz – GT 730 (GF108)](https://videocardz.com/nvidia/geforce-700/geforce-gt-730)
- [GPUZoo – GT 730 DDR3 64-bit](https://www.gpuzoo.com/GPU-NVIDIA/GeForce_GT_730_DDR3_64-bit.html)
- [GPUZoo – GT 730 DDR3 128-bit](https://www.gpuzoo.com/GPU-NVIDIA/GeForce_GT_730_DDR3_128-bit.html)
- [NVIDIA Tesla M60 Datasheet (PDF)](https://images.nvidia.com/content/tesla/pdf/188417-Tesla-M60-DS-A4-fnl-Web.pdf)
- [VideoCardz – Tesla M60](https://videocardz.net/nvidia-tesla-m60)
