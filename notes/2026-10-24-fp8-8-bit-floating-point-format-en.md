---
audio: false
generated: true
image: false
lang: en
layout: post
title: "FP8: 8-Bit Floating Point Format"
translated: false
type: note
---

Question: What does FP8 mean in detail?

Answer:

**FP8** = **8-bit Floating Point** — a number format that uses only **8 bits** to represent a decimal number.

---

## Why 8 Bits Is Challenging

A floating-point number has 3 parts:

```
[ Sign | Exponent | Mantissa ]
```

With only 8 bits total, you have to make a hard trade-off between **range** (exponent) and **precision** (mantissa). This is why FP8 comes in **two variants**:

---

## Two FP8 Variants

### E4M3 — "More Precision"

```
[ 1 sign | 4 exponent | 3 mantissa ]
Max value: ±448
Used in: forward pass (activations, weights)
```

### E5M2 — "More Range"

```
[ 1 sign | 5 exponent | 2 mantissa ]
Max value: ±57,344
Used in: backward pass (gradients)
```

---

## Visual Analogy

Think of 8 bits like a ruler with only **8 tick marks**:

| Format | You get... |
|--------|-----------|
| FP32   | A ruler with 4 billion tick marks — very precise |
| FP16   | A ruler with 65,536 tick marks |
| **FP8**| A ruler with only **256 tick marks** — very coarse |

So FP8 can only represent **256 distinct values** total. It's a very rough approximation.

---

## So Why Use It?

| Benefit | Detail |
| --------- | -------- |
| 🚀 **2× faster** than FP16 | Less data to move through memory |
| 💾 **Half the memory** of FP16 | Fit larger models on same GPU |
| ⚡ **Higher throughput** | H100 GPU does 4× more FP8 ops than FP16 |

---

## Where FP8 Is Used Today

- **NVIDIA H100 / H200** — first GPUs with native FP8 Tensor Cores
- **LLM inference** — running models like LLaMA, GPT at high speed
- **LLM training** — experimental, requires careful scaling (e.g., FP8 in Transformer Engine)
- **Not** on consumer GPUs (RTX 3090, 4090 do not have native FP8 support)

---

## Key Takeaway

> FP8 is a **speed/memory optimization** — you trade numerical precision for performance. It's only practical because modern neural networks are surprisingly tolerant of low-precision arithmetic, especially during inference.

---

References:

- [NVIDIA FP8 Primer](https://docs.nvidia.com/deeplearning/transformer-engine/user-guide/examples/fp8_primer.html)
- [FP8 Formats for Deep Learning (2022 paper)](https://arxiv.org/abs/2209.05433)
