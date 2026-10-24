---
audio: false
generated: true
image: false
lang: en
layout: post
title: FP8, FP16, BF16 Explained
translated: false
type: note
---

Question: What do FP8, FP16, and BF16 mean, and how do they differ?

Answer:

These are **floating-point number formats** used in machine learning to represent numbers in memory. They differ in how many bits are allocated to the **exponent** (range) vs **mantissa/significand** (precision).

---

## Bit Layout Comparison

| Format | Total Bits | Sign | Exponent | Mantissa | Range | Precision |
|--------|-----------|------|----------|----------|-------|-----------|
| FP32   | 32        | 1    | 8        | 23       | ±3.4×10³⁸ | Highest |
| FP16   | 16        | 1    | 5        | 10       | ±65,504 | Medium |
| BF16   | 16        | 1    | **8**    | 7        | ±3.4×10³⁸ | Lower |
| FP8 (E4M3) | 8   | 1    | 4        | 3        | ±448   | Very Low |
| FP8 (E5M2) | 8   | 1    | 5        | 2        | ±57,344 | Lowest |

---

## Each Format Explained

**FP32** — the standard "full precision" baseline. Everything is compared against it.

**FP16** — half the bits of FP32. Saves memory and speeds up computation, but its small exponent (5 bits) means a narrow range, so numbers can **overflow** or **underflow** during training. Requires loss scaling tricks.

**BF16** (Brain Float 16, developed by Google Brain) — also 16 bits, but keeps the **same 8-bit exponent as FP32**, trading precision for range stability. Much safer for training because overflow is almost eliminated. Natively supported on NVIDIA A100/H100, Google TPUs, AMD MI300X.

**FP8** — the newest, most aggressive format (standardized by NVIDIA/ARM/Intel in 2022). Two variants:

- **E4M3** — more precision, used in the **forward pass**
- **E5M2** — more range, used in the **backward pass / gradients**

---

## Why It Matters in AI

```
Memory & Speed:   FP8 > BF16 ≈ FP16 > FP32   (smaller = faster)
Numerical Safety: FP32 > BF16 > FP16 > FP8    (larger = safer)
```

- **Training**: BF16 is the sweet spot today (used by most LLM training runs)
- **Inference**: FP8 or FP16 for speed; BF16 when accuracy matters
- **Consumer GPUs** (e.g., RTX 3090): support FP16 but not BF16 natively
- **Data center GPUs** (A100, H100): support all formats natively

---

References:

- [NVIDIA FP8 Format White Paper](https://docs.nvidia.com/deeplearning/transformer-engine/user-guide/examples/fp8_primer.html)
- [BF16: The secret to high performance on Cloud TPUs](https://cloud.google.com/blog/products/ai-machine-learning/bfloat16-the-secret-to-high-performance-on-cloud-tpus)
- [Mixed Precision Training (Micikevicius et al., 2018)](https://arxiv.org/abs/1710.03740)
