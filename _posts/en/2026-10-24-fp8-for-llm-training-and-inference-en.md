---
audio: false
generated: true
image: false
lang: en
layout: post
title: FP8 for LLM Training and Inference
translated: false
type: note
---

Question: Why is FP8 used in LLM training or inference?

Answer:

**FP8 (8-bit Floating Point)** is adopted in LLMs primarily for **speed, memory savings, and energy efficiency** without dramatically sacrificing model quality. Here's the breakdown:

---

### 1. Memory Reduction (2–4× vs FP32)

| Format | Bits | Relative Size |
|--------|------|---------------|
| FP32   | 32   | 4×            |
| BF16 / FP16 | 16 | 2×         |
| **FP8**    | **8** | **1×**   |

Halving the precision from BF16 → FP8 cuts memory for weights, activations, and KV-cache by ~50%, allowing larger models or bigger batch sizes on the same hardware.

---

### 2. Hardware Throughput (2× over FP16)

NVIDIA H100/H200 and Blackwell GPUs have dedicated **FP8 Tensor Cores** that deliver roughly **2× the FLOPS** vs FP16. NVIDIA's Transformer Engine exploits this automatically.

---

### 3. Two FP8 Variants for Different Roles

- **E4M3** (4 exponent + 3 mantissa bits) — higher precision, used for **weights & activations** (forward pass)
- **E5M2** (5 exponent + 2 mantissa bits) — higher dynamic range, used for **gradients** (backward pass)

---

### 4. Inference: KV-Cache and Latency

During inference, FP8 quantization of the **KV-cache** alone can save 40–50% memory, enabling longer context windows or more concurrent requests. Latency also drops thanks to faster Tensor Core operations.

---

### 5. Training Stability Techniques

FP8's limited range requires careful handling:

- **Per-tensor / per-channel scaling** — each tensor gets its own scale factor
- **Delayed scaling** — scale factors updated periodically to avoid overflow/underflow
- **Master weights in BF16/FP32** — optimizer states stay in higher precision; only compute uses FP8

---

### Why Not INT8?

INT8 is fixed-point and works well for inference, but **not for training** (gradients need floating-point semantics). FP8 gives the best of both: the compactness of 8 bits with the dynamic range of floating-point.

---

### Summary

| Benefit        | Training | Inference |
|----------------|----------|-----------|
| Memory savings | ✅ activations/grads | ✅ weights/KV-cache |
| Speed boost    | ✅ ~2× matmul FLOPS | ✅ lower latency |
| Energy savings | ✅ | ✅ |
| Risk           | Gradient underflow (mitigated by scaling) | Slight accuracy loss (mitigated by calibration) |

References:

- [NVIDIA Transformer Engine – FP8 Training](https://docs.nvidia.com/deeplearning/transformer-engine/user-guide/index.html)
- [FP8 Formats for Deep Learning (Micikevicius et al., 2022)](https://arxiv.org/abs/2209.05433)
- [NVIDIA H100 Tensor Core GPU Architecture Whitepaper](https://resources.nvidia.com/en-us-tensor-core/gtc22-whitepaper-hopper)
