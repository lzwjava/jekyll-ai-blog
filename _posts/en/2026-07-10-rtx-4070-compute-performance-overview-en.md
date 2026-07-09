---
audio: false
generated: true
image: false
lang: en
layout: post
title: RTX 4070 Compute Performance Overview
translated: false
type: note
---

Question: What are the TFLOPS and overall compute performance specs of the RTX 4070?

Answer:

The RTX 4070 (non-Super) is Ada Lovelace (AD104 die, cut-down). Specs relevant to your ML workloads:

**Core specs**

- CUDA cores: 5888
- Boost clock: 2475 MHz
- Memory: 12GB GDDR6X, 192-bit bus
- Memory bandwidth: 504 GB/s
- TDP: 200W

**Compute throughput**

| Precision | TFLOPS/TOPS |
| --- | --- |
| FP32 (CUDA cores) | ~29 TFLOPS |
| FP16 Tensor (dense) | ~116 TFLOPS |
| FP16 Tensor (2:4 sparsity) | ~233 TFLOPS |
| INT8 (dense) | ~233 TOPS |
| INT8 (sparse) | ~466 TOPS |
| FP8 (dense, Ada's native tensor precision) | ~233 TFLOPS |

No FP64 tensor path worth mentioning — Ada cards aren't built for that, ignore it for your use case.

**What this means for your workloads**

For your GPT-2 760M-scale training and nanochat experiments on this box:

- 12GB VRAM is your real constraint, not compute. A 760M param model in fp16/bf16 is ~1.5GB just for weights, but Adam optimizer states (2x fp32 momentum+variance) plus activations will eat the rest fast. You're likely already using gradient checkpointing or a small batch size — if not, that's your first lever.
- No native FP64, so anything relying on double precision (some numerical stability tricks) will silently fall back to slow emulated paths — avoid.
- Memory bandwidth (504 GB/s) is usually your bottleneck for small-batch inference, not the 29 TFLOPS FP32 — memory-bound, not compute-bound, at your model scale. This is why quantization (int8/int4) helps disproportionately on this card vs. compute-bound giant clusters.
- Compare to your MI300X: 192GB HBM3 at ~5.3 TB/s bandwidth and ~163 TFLOPS FP32 (much higher FP64 too) — roughly 10x the bandwidth, so full DeepSeek v4 MoE-scale training stays cloud-side; RTX 4070 is your local iteration/debugging rig before scaling out.

Practical rule of thumb: on 4070, target models where weights + optimizer state + activations fit under ~10GB (leaving headroom for CUDA context), use bf16/fp16 autocast, and reach for gradient checkpointing or LoRA rather than full fine-tunes once you're above ~1-2B params.
