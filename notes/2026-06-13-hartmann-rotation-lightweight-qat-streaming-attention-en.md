---
audio: false
generated: true
image: false
lang: en
layout: post
title: Hartmann Rotation, Lightweight QAT, Streaming Attention
translated: false
type: note
---

**Question:** What are the Hartmann Rotation for Q/K in attention, lightweight QAT for accuracy recovery, and streaming attention with position decay — and how do they work?

**Answer:**

These are three inference optimization techniques from a Chinese LLM team (likely **Hunyuan** from Tencent, given "Huyan model series", 128K context, and "Slim" GitHub project). Let me break each down from first principles.

---

## 1. Hadamard Rotation for Q and K (the "Hartmann Rotation")

This is almost certainly a **Hadamard rotation** (the text likely mistranslates/misspells it). It's used to fix the **outlier channel problem** in LLM quantization.

### The Problem: Outlier Channels

In transformer hidden states and Q/K projections, a small subset of channels carry disproportionately large magnitudes. Empirically (from LLM.int8(), SmoothQuant papers), ~0.1% of channels can have 100x larger values than the rest.

When you quantize to INT8/INT4:

```
quantized = round(x / scale)   where scale = max(|x|) / 127
```

If one channel has value 200 and all others are ~1, your scale = 200/127 ≈ 1.57, and all the small values collapse to ±1 — massive precision loss.

### The Fix: Hadamard Rotation

A **Hadamard matrix** H is an orthogonal matrix where every entry is ±1/√n. Key property:

```
H @ H.T = I   (orthogonal, preserves L2 norm)
```

You rotate Q and K before quantization:

```python
import torch

def hadamard_matrix(n):
    # n must be power of 2
    if n == 1:
        return torch.tensor([[1.0]])
    H_half = hadamard_matrix(n // 2)
    return torch.cat([
        torch.cat([H_half,  H_half], dim=1),
        torch.cat([H_half, -H_half], dim=1)
    ], dim=0) / (2 ** 0.5)

def rotate_for_quantization(Q, K):
    d = Q.shape[-1]
    H = hadamard_matrix(d).to(Q.device)
    # Rotate: spreads energy uniformly across all channels
    Q_rot = Q @ H.T
    K_rot = K @ H.T
    return Q_rot, K_rot
```

Because H is orthogonal, `Q_rot @ K_rot.T == Q @ K.T` — **attention scores are unchanged**. But now the energy is spread uniformly across all d channels, so no single channel dominates, and quantization scale covers all channels efficiently.

This is the core idea behind **QuaRot** (ETH Zurich, 2024) and **SpinQuant** (Meta, 2024).

---

## 2. Lightweight QAT for Final Accuracy Recovery

### Standard PTQ vs QAT

**Post-Training Quantization (PTQ)**: calibrate scales on a small dataset after training. Fast, but lossy for low-bit (W4A8, W4A4).

**Full QAT**: simulate quantization during the entire training run. Accurate, but costs as much as retraining.

**Lightweight QAT** (what they're doing): a short fine-tuning pass after PTQ, with quantization noise simulated in the forward pass.

### How Straight-Through Estimator Makes This Work

Quantization is non-differentiable (round function has zero gradient everywhere). The trick is the **Straight-Through Estimator (STE)**:

```python
class FakeQuantize(torch.autograd.Function):
    @staticmethod
    def forward(ctx, x, scale, zero_point, bits):
        # Simulate quantization in forward
        x_int = torch.round(x / scale) + zero_point
        x_int = torch.clamp(x_int, 0, 2**bits - 1)
        x_dequant = (x_int - zero_point) * scale
        return x_dequant

    @staticmethod
    def backward(ctx, grad_output):
        # STE: pass gradient straight through as if no quantization
        return grad_output, None, None, None
```

During lightweight QAT:

- Weights are full-precision in memory
- Forward pass uses fake-quantized weights (simulates INT4 noise)
- Backward pass uses STE to update scales AND weights
- Run for ~1-5% of original training steps

The quantization **scales become learnable parameters**, so the model adapts its weight distributions to be more quantization-friendly. Result: near-lossless W4A8 with a fraction of full training cost.

---

## 3. Streaming Attention with Position Decay and Token Dropping

### The Quadratic Problem

Standard attention is O(n²) in sequence length. At 128K tokens:

```
128000² = 16.4 billion attention score pairs
```

Even with FlashAttention, TTFT (time-to-first-token) is brutal. Sparse attention is needed.

### Standard Sparse Attention Failure Mode

Naive token dropping (skip computing some KV pairs) causes **error accumulation**: if token at position i is dropped, token i+1 which depends on i carries forward a corrupted state, and this compounds over the sequence.

### Their Position Decay Solution

The key insight: **early tokens (the "sink" tokens) are always critical** — this is well-established from StreamingLLM (MIT/Meta, 2023) which showed that attention always concentrates mass on the first few tokens.

Their design:

```
Sequence: [HEAD tokens: 0..K] [TAIL tokens: K+1..N]

HEAD: full causal attention (inverted triangle mask — standard)
TAIL: position-decayed attention — each token can only attend
      to a LOCAL WINDOW + the HEAD tokens
```

Visually:

```
Token position →
         0  1  2  ... K  K+1  K+2  ...  N
HEAD:    ▓  ▓  ▓  ... ▓
TAIL:    ▓  ▓  ▓  ... ▓  [w]
TAIL:    ▓  ▓  ▓  ... ▓   ▓   [w]
TAIL:    ▓  ▓  ▓  ... ▓   ▓    ▓   [w]

▓ = always attend (sink + head)
[w] = local window only
```

The "position decay factor" mathematically means the attention logit for attending to position j from position i gets multiplied by a decay term:

```python
def position_decay_mask(seq_len, head_size, window_size):
    mask = torch.full((seq_len, seq_len), float('-inf'))

    # HEAD tokens: full causal attention
    mask[:head_size, :head_size] = 0.0

    # TAIL tokens: attend to HEAD + local window
    for i in range(head_size, seq_len):
        mask[i, :head_size] = 0.0              # always see HEAD
        mask[i, max(head_size, i-window_size):i+1] = 0.0  # local window

    return mask
```

This gives you **O(n × (K + w))** complexity instead of O(n²), where K = head size, w = window size.

### Output-Aware Token Dropping

The "output-aware" part means they also selectively drop tokens in the KV cache based on their **contribution to the output** — similar to H2O (Heavy Hitter Oracle) or SnapKV. Tokens that receive low cumulative attention weight across heads are evicted from the cache, since they contribute little to future outputs.

---

## Summary Table

| Technique | Problem Solved | Key Idea | Complexity |
| --- | --- | --- | --- |
| Hadamard Rotation | Outlier channels break quantization | Orthogonal rotation spreads energy uniformly | O(d log d) via Fast Hadamard Transform |
| Lightweight QAT | PTQ residual accuracy loss | STE + learnable scales for short fine-tune | ~1-5% of full training cost |
| Streaming Attention | O(n²) at 128K context | Sink tokens + local window + decay mask | O(n(K+w)) |

All three are practical inference-time optimizations aimed at deploying a large model efficiently — not research novelties, but engineering solutions for production LLM serving.

**References:**

- [QuaRot: Outlier-Free 4-Bit Inference in Rotated LLMs](https://arxiv.org/abs/2404.00456)
- [SpinQuant: LLM quantization with learned rotations](https://arxiv.org/abs/2405.16406)
- [StreamingLLM: Efficient Streaming Language Models with Attention Sinks](https://arxiv.org/abs/2309.17453)
- [H2O: Heavy-Hitter Oracle for Efficient Generative Inference](https://arxiv.org/abs/2306.14048)
- [SmoothQuant: Accurate and Efficient Post-Training Quantization](https://arxiv.org/abs/2211.10438)
