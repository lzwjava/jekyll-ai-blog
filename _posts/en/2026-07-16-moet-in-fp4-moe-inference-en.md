---
audio: false
generated: true
image: false
lang: en
layout: post
title: MoET in FP4 MoE Inference
translated: false
type: note
---

Question: What does "MoET" mean in the context of running v4 flash with FP4-level throughput?

Answer: I couldn't find "MoET" as a standard, citable term in the quantization literature — it's not a paper name like GPTQ/AWQs are. Based on your context (running a flash MoE model, using "moet" to "补精度" so FP4 throughput doesn't tank quality), it's almost certainly community shorthand for **mixed-precision MoE compensation** — the general technique class covered by things like MoEQuant, AlphaQ, and LREC:

The core idea across all of these:
1. Quantize the bulk of weights (usually the FFN/expert matrices) to FP4/INT4 for the throughput win.
2. Keep a small set of "sensitive" components at higher precision — router/gate weights, first/last layers, or specific outlier channels — since these dominate output quality loss.
3. Add a lightweight error-compensation term (low-rank adapter, per-channel scale, or per-expert calibration) that's cheap to compute but corrects most of the quantization error introduced in step 1.

That's why you get FP4-level throughput/VRAM while accuracy holds close to bf16 — you're not uniformly quantizing everything, you're doing selective/mixed precision + a correction pass.

Your numbers (4 concurrent → 300 tok/s, 8 concurrent → 400 tok/s) look like a decode-bound MoE serving profile — sublinear scaling from 4→8 concurrency suggests you're hitting memory bandwidth on the expert weights, not compute. That's consistent with FP4 weight-only quant: weights are cheap to move, but KV cache + activation dequant become the bottleneck as batch grows.

If you can share which repo/tool actually prints "MoET" in its logs or docs (vLLM fork, SGLang, or a custom quant script), I can pull the exact definition instead of the generic pattern above — worth checking since these Chinese-community deployment tools often name things ad hoc.

References:
- [MoEQuant: Expert-Balanced Sampling and Affinity Guidance](https://arxiv.org/abs/2505.03804)
- [AlphaQ: Calibration-Free Bit Allocation for MoE Quantization](https://arxiv.org/html/2606.04980)
- [FP4-Quantization with Low-Rank Error Correction (LREC)](https://ieeexplore.ieee.org/document/10685437/)
- [NVIDIA NVFP4 for efficient low-precision inference](https://developer.nvidia.com/blog/introducing-nvfp4-for-efficient-and-accurate-low-precision-inference/)
