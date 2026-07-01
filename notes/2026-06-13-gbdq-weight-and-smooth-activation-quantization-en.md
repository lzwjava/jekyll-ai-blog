---
audio: false
generated: true
image: false
lang: en
layout: post
title: GBDQ Weight and Smooth Activation Quantization
translated: false
type: note
---

**Question:** What is the quantization strategy described here — GBDQ for weights and Smooth Quantization for activations — and how does each technique work?

**Answer:**

This is a description of a **production LLM inference quantization pipeline**, likely from a team deploying a large model on NVIDIA Blackwell (B100/B200) GPUs with native FP4 support. Let me break it down from first principles.

---

## Why Quantize?

A transformer's memory cost at inference is dominated by:

1. **Weights** — e.g. a 70B model in BF16 = ~140GB
2. **KV cache** — grows linearly with `batch_size × seq_len × num_heads × head_dim × 2 (K+V)`

Going from 8-bit → 4-bit cuts both in half. Blackwell's tensor cores can do **native FP4 matmuls**, so you also get compute throughput gains, not just memory savings.

---

## Part 1: Weight Quantization — GBDQ

**GBDQ = Group-wise Block-wise Dynamic Quantization**

### What it means

- **Group-wise**: Instead of one global scale factor per tensor, you use one scale per *group* of N weights (e.g. N=128). This is identical to what GPTQ and AWQ do. Finer granularity = less quantization error.
- **Block-wise**: Applied per transformer block/layer, not globally.
- **Dynamic**: Quantization parameters (scale, zero-point) are computed per inference step or per calibration batch, not fixed statically.

### The reconstruction loop (key insight)

```python
# Pseudocode for layer-wise reconstruction
for layer in model.layers:
    W_fp = layer.weight.float()          # full precision
    W_q = quantize(W_fp, bits=4)         # quantize to INT4/FP4

    # Forward pass with calibration data
    out_fp = X @ W_fp.T                  # ground truth
    out_q  = X @ dequantize(W_q).T      # quantized output

    error = out_fp - out_q               # reconstruction error

    # Iteratively tune scale/zero-point to minimize error
    optimize(quantization_params, loss=MSE(error))
```

This is essentially what **GPTQ** does — it uses second-order Hessian information (from the Fisher matrix) to compensate errors weight-by-weight. GBDQ likely uses a similar or simplified version of this.

The key insight: **quantization error in weights compounds through layers**. By correcting it layer-by-layer with real activations, you avoid the cascading degradation you'd get from naive round-to-nearest.

---

## Part 2: Activation Quantization — Smooth Quantization

Activating activations is *harder* than weights because:

- Weights are static — you can calibrate offline
- Activations are **dynamic** — they change per input
- Activations have **outliers**: a few channels spike to 100x the average magnitude

### The outlier problem visualized

```
Channel:  [0,   1,   2,   3,    4,    5  ]
Value:    [0.1, 0.2, 0.1, 0.3, 89.4, 0.2]  ← channel 4 is an outlier
```

If you quantize this to INT4 (range -8 to 7), the scale = 89.4/7 ≈ 12.8. Now all small values get mapped to ~0. Massive error.

### SmoothQuant's fix

The mathematical identity being exploited:

```
Y = X @ W
  = (X / s) @ (W * s)    ← scale migrated from activation to weight
```

Where `s` is a **per-channel smoothing factor**.

```python
# Per-channel smooth factor (found via calibration)
s = max(abs(X), dim=0) ** alpha   # alpha typically 0.5

X_smooth = X / s          # activations now have smaller dynamic range
W_smooth = W * s          # weights absorb the scale

# Now quantize both — activations no longer have outliers
X_q = quantize(X_smooth, bits=4)
W_q = quantize(W_smooth, bits=4)

# Forward pass: mathematically equivalent to original
Y = X_q @ W_q   ≈   X @ W
```

The `alpha=0.5` splits the "difficulty" equally between activations and weights. The model output is **mathematically identical** to the unsmoothed version (before quantization rounding), so no retraining needed.

---

## How They Compose Together

```
Input X (FP16/BF16)
    │
    ▼
[SmoothQuant] → X_smooth (reduced outliers)
    │
    ▼
[Quantize X_smooth → FP4]    [GBDQ: W already quantized to FP4, error-corrected]
    │                               │
    └────────── FP4 matmul ─────────┘
                    │
                    ▼
              Output (dequantize → BF16)
```

On Blackwell, the FP4 matmul is a **native hardware op** — that's what makes this worth doing. You get ~2x memory reduction and Blackwell's FP4 tensor core throughput.

---

## Related Work You Should Know

| Technique | What it does |
| ----------- | ------------- |
| **GPTQ** | Layer-wise weight quantization with Hessian-based error correction — ancestor of GBDQ |
| **AWQ** | Activation-aware weight quantization — protects salient weights based on activation magnitude |
| **SmoothQuant** | Exact origin of the smooth quantization described here |
| **LLM.int8()** | Mixed-precision: keeps outlier channels in FP16, rest in INT8 |
| **QuIP#** | Incoherence processing + lattice codebooks for extreme compression |

GBDQ sounds like an internal variant of GPTQ + AWQ ideas, applied block-wise with dynamic calibration. SmoothQuant is a published technique from MIT/NVIDIA (2022).

---

## TL;DR

- **GBDQ**: Quantize weights to 4-bit, then run a calibration loop per layer to minimize reconstruction error. Prevents quantization error from compounding through depth.
- **Smooth Quantization**: Mathematically migrate activation outliers into the weights via a per-channel scale factor, making both quantizable to 4-bit without accuracy loss.
- Together: full W4A4 (4-bit weights, 4-bit activations) on Blackwell's FP4 tensor cores → ~2-4x memory savings, significant throughput gains.

**References:**

- [SmoothQuant: Accurate and Efficient Post-Training Quantization for LLMs](https://arxiv.org/abs/2211.10438)
- [GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers](https://arxiv.org/abs/2210.17323)
- [AWQ: Activation-aware Weight Quantization](https://arxiv.org/abs/2306.00978)
