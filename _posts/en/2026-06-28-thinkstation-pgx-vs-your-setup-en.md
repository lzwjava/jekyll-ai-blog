---
audio: false
generated: true
image: false
lang: en
layout: post
title: ThinkStation PGX vs Your Setup
translated: false
type: note
---

Let me check that page.This is Lenovo's ThinkStation PGX — their version of the NVIDIA DGX Spark (formerly "Project DIGITS"). It's a compact desktop AI development box built around the NVIDIA GB10 Grace Blackwell Superchip.

The relevant specs from the page:

- **SoC:** NVIDIA GB10 Grace Blackwell Superchip — a 20-core Arm Grace CPU fused to a Blackwell GPU via NVLink-C2C
- **Memory:** 128GB LPDDR5x unified (CPU+GPU share it, coherent)
- **Storage:** up to 4TB NVMe M.2
- **OS:** NVIDIA DGX OS (Ubuntu-based)
- **Price:** ~$5,079 (showing $4,825 promo), SFF form factor

The pitch is "your own little DGX." The GB10 delivers roughly **1 petaflop of FP4 (sparse)** AI compute, and the 128GB coherent pool is the actual selling point — it lets you load models that won't fit on a single discrete GPU's VRAM. Two of them can be NVLink-bridged to run ~405B-class models for inference.

How this maps to your situation, concretely:

**Where it wins over your RTX 4070 (12GB):** the 4070 caps you hard on VRAM. The PGX's 128GB unified memory means you can run/fine-tune models in the 70B range (quantized) or do LoRA on much bigger bases without the OOM dance. For your DeepSeek-v4 MoE exploration and nanochat-scale work, the memory ceiling is the thing that actually unblocks you.

**Where it loses:** FP4-petaflop marketing ≠ training throughput. LPDDR5x has far less bandwidth (~273 GB/s) than the MI300X's HBM3 (~5.3 TB/s) or even a 4090's GDDR6X. For raw training speed — your GPT-2 760M-from-scratch runs — it'll be *much* slower than the MI300X. This is a "fits big models, runs them slowly" device, optimized for inference, prototyping, and fine-tuning rather than from-scratch pretraining.

**The honest comparison for you:** at ~$5K, this is roughly 2,500 hours of MI300X dev-cloud time at $2/hr. Given you already have MI300X access for heavy training and a 4070 for local iteration, the PGX's niche is "local box that can hold a 70B model in memory for agent/inference work without renting." That's a real gap in your setup, but it's a convenience/latency purchase, not a capability you lack. If the goal is training competency that compounds, the MI300X hours buy more learning per dollar. If the goal is a quiet always-on local inference/agent host with huge memory, the PGX fits.

References:

- [Lenovo ThinkStation PGX product page](https://www.lenovo.com/us/en/p/workstations/thinkstation-p-series/lenovo-thinkstation-pgx-sff/len102s0023)
- [NVIDIA DGX Spark](https://www.nvidia.com/en-us/products/workstations/dgx-spark/)
