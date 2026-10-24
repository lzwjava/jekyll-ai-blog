---
audio: false
generated: true
image: false
lang: zh
layout: post
title: FP8, FP16, BF16 详解
translated: true
type: note
---

问题：FP8、FP16、BF16 分别是什么意思？它们之间有何不同？

答案：

这些是用于机器学习中在内存中表示数字的 **floating-point number formats**。它们区别在于分配给 **exponent** (range) 和 **mantissa/significand** (precision) 的 bits 数量不同。

---

## Bit Layout Comparison

| Format | Total Bits | Sign | Exponent | Mantissa | Range | Precision |
|--------|-----------|------|----------|----------|-------|-----------|
| FP32   | 32        | 1    | 8        | 23       | ±3.4×10³⁸ | 最高 |
| FP16   | 16        | 1    | 5        | 10       | ±65,504 | 中等 |
| BF16   | 16        | 1    | 8        | 7        | ±3.4×10³⁸ | 较低 |
| FP8 (E4M3) | 8   | 1    | 4        | 3        | ±448   | 非常低 |
| FP8 (E5M2) | 8   | 1    | 5        | 2        | ±57,344 | 最低 |

---

## Each Format Explained

**FP32** — 标准的 "full precision" baseline。所有其他格式与之比较。

**FP16** — 只有 FP32 一半的 bits。节省内存并加速计算，但其较小的 exponent (5 bits) 意味着狭窄的范围，因此数字在训练中可能会 **overflow** 或 **underflow**。需要 loss scaling tricks。

**BF16** (Brain Float 16, 由 Google Brain 开发) — 也是 16 bits，但保持与 FP32 **相同的 8-bit exponent**，以精度换取范围稳定性。训练中更安全，因为 overflow 几乎消除。在 NVIDIA A100/H100、Google TPUs、AMD MI300X 等设备上原生支持。

**FP8** — 最新、最激进的 format（由 NVIDIA/ARM/Intel 在 2022 年标准化）。两个变体：
- **E4M3** — 更多 precision，用于 **forward pass**
- **E5M2** — 更多 range，用于 **backward pass / gradients**

## Why It Matters in AI

Memory & Speed:   FP8 > BF16 ≈ FP16 > FP32   (更小 = 更快)
Numerical Safety: FP32 > BF16 > FP16 > FP8    (更大 = 更安全)

- **Training**: BF16 is the sweet spot today (用于大多数 LLM training runs)
- **Inference**: 使用 FP8 或 FP16 以获得速度；当精度重要时使用 BF16
- **Consumer GPUs** (例如 RTX 3090): 原生支持 FP16 但不支持 BF16
- **Data center GPUs** (A100, H100): 原生支持所有 formats

参考文献：
- [NVIDIA FP8 Format White Paper](https://docs.nvidia.com/deeplearning/transformer-engine/user-guide/examples/fp8_primer.html)
- [BF16: The secret to high performance on Cloud TPUs](https://cloud.google.com/blog/products/ai-machine-learning/bfloat16-the-secret-to-high-performance-on-cloud-tpus)
- [Mixed Precision Training (Micikevicius et al., 2018)](https://arxiv.org/abs/1710.03740)