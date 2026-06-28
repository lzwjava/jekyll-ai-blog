---
audio: false
generated: true
image: false
lang: en
layout: post
title: DGX Spark Price $4,699
translated: false
type: note
---

Question: How much does the NVIDIA DGX Spark cost?

Let me search for current pricing.Question: How much does the NVIDIA DGX Spark cost?

Answer:

The **NVIDIA DGX Spark (Founders Edition)** currently costs **$4,699** (MSRP). The price was revised from $3,999 to $4,699 in February 2026 — an ~18% increase — due to worldwide memory supply constraints. No hardware changes came with the hike.

Pricing history for context:

- CES 2025 (Project Digits announcement): $2,999
- GTC reservations / launch (Oct 2025): $3,999
- Feb 2026 → present: $4,699

Cheaper OEM alternatives with identical GB10 internals (usually 1TB SSD instead of 4TB):

- ASUS Ascent GX10 — ~$3,266
- Dell Pro Max GB10, MSI EdgeXpert, Acer Veriton GN100, HP variants

Note: some channels like Amazon/Microcenter may still show $3,999 until they update.

For your use case — given you're already on an MI300X (192GB) and RTX 4070 — the Spark's real bottleneck is worth flagging: 273 GB/s memory bandwidth is the fundamental limit on large-model performance. The MI300X's HBM3 (~5.3 TB/s) crushes it for training; the Spark only wins on CUDA-native dev ergonomics and form factor.

References:

- [NVIDIA DGX Spark US marketplace](https://marketplace.nvidia.com/en-us/enterprise/personal-ai-supercomputers/dgx-spark/)
- [Tom's Hardware — price increase to $4,699](https://www.tomshardware.com/desktops/mini-pcs/nvidia-dgx-spark-gets-18-percent-price-increase-as-memory-shortages-bite-founders-edition-now-usd4-699-up-from-usd3-999)
- [ToolHalla — DGX Spark complete guide 2026](https://toolhalla.ai/blog/nvidia-dgx-spark-complete-guide-2026)
