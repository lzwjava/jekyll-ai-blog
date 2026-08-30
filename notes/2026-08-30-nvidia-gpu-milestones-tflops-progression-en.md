---
audio: false
generated: true
image: false
lang: en
layout: post
title: Nvidia GPU Milestones TFLOPS Progression
translated: false
type: note
---

Now I have all the data needed. Let me build a chart and a comprehensive table.

**Question:** What are the key Nvidia GPU milestones with their TFLOPS / PFLOPS numbers?

**Answer:**

Here's the compute performance progression across every major Nvidia GPU generation:The chart uses a log scale because the numbers span 4 orders of magnitude. Here's the full breakdown in detail:

---

| GPU | Year | Arch | FP32 TFLOPS | FP16 TFLOPS | Notes |
| --- | --- | --- | --- | --- | --- |
| **GTX 980** | 2014 | Maxwell | ~5.1 | ~5.1 | No Tensor Cores; FP16 = FP32 |
| **GTX 1080 Ti** | 2017 | Pascal | ~11.3 | ~11.3 | First to break 10 TFLOPS FP32 |
| **RTX 2080 Ti** | 2018 | Turing | ~13.4 | ~107.9 (Tensor) | First hardware RT + Tensor Cores |
| **RTX 3080** | 2020 | Ampere | ~29.8 | ~119 (Tensor) | ~2× jump over 2080 Ti |
| **A100** | 2020 | Ampere | ~19.5 | ~312 (Tensor) | Data center; HBM2e; MIG |
| **H100** | 2022 | Hopper | ~67 | ~1,979 (Tensor) | Transformer Engine, FP8 |
| **H200** | 2024 | Hopper+ | ~67 | ~3,958 (Tensor FP8) | 141 GB HBM3e; same die as H100 |
| **B200** | 2025 | Blackwell | ~75 | ~4,500 (FP16 Tensor) | 9 PFLOPS FP4; 180 GB HBM3e |

---

A few key observations:

**FP32** grew from ~5 → ~75 TFLOPS over a decade — roughly **15×**. Solid, but modest. The real explosion happened in AI-precision formats.

**FP16 Tensor** went from effectively nothing to 4,500 TFLOPS FP8 dense on the B200, which is roughly **2.3× the H100's 1,979 TFLOPS**, and thousands of times more than Maxwell could offer.

**FP4 (B200's party trick):** Tensor Core performance reaches 9 PFLOPS FP4 dense (18 PFLOPS with 2:4 structured sparsity) — a completely new precision tier that H100 had no native support for at all.

**The GB200 NVL72 rack** pools 72 B200s, reaching 1,440 petaFLOPS of total FP4 Tensor Core performance — over 1 exaFLOP in a single rack.

---

**References:**

- [NVIDIA B200 Specs & Benchmarks — Spheron](https://www.spheron.network/blog/nvidia-b200-complete-guide/)
- [NVIDIA B200 SXM Specs — Flopper.io](https://flopper.io/gpu/nvidia-b200-sxm-180gb)
- [NVIDIA Blackwell B200 Datasheet](https://www.primeline-solutions.com/media/categories/server/nach-gpu/nvidia-hgx-h200/nvidia-blackwell-b200-datasheet.pdf)
- [NVIDIA Data Center GPU Specs — IntuitionLabs](https://intuitionlabs.ai/articles/nvidia-data-center-gpu-specs)
- [Comparing Nvidia B200 and H100 — Civo](https://www.civo.com/blog/comparing-nvidia-b200-and-h100)
