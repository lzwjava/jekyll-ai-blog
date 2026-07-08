---
audio: false
generated: true
image: false
lang: en
layout: post
title: FP8 Scale Denominator Clamp
translated: false
type: note
---

Question: In nanochat's FP8 quantization code, what does `.clamp(min=EPS)` do in the line `scale = fp8_max / amax.double().clamp(min=EPS)`?

Answer:

This line is from nanochat's hand-rolled FP8 quantization (replacing the torchao dependency — the commit deletes the torchao dependency and creates a custom API-matched version). Full context:

```python
scale = fp8_max / amax.double().clamp(min=EPS)
scale = scale.float()
x_scaled = x.float() * scale
x_clamped = x_scaled.clamp(-fp8_max, fp8_max)
x_fp8 = x_clamped.to(fp8_dtype)
inv_scale = scale.reciprocal()
```

**`amax`** = the tensor's absolute max (`x.abs().max()`), computed per-tensor or per-row depending on the recipe (tensorwise vs rowwise). It tells you the dynamic range you need to fit into FP8's tiny range (e.g. e4m3 has `fp8_max ≈ 448`).

**`.clamp(min=EPS)` here is a divide-by-zero guard, not a saturation clamp.** Two different clamps show up in this snippet and they do opposite jobs:

1. `amax.double().clamp(min=EPS)` — floors the *denominator*. If a tensor/row is all zeros (dead activations, a masked-out row, a zeroed gradient), `amax = 0`, and `fp8_max / 0` → `inf`/`nan`. Clamping the denominator to a tiny epsilon (`EPS`, typically something like `1e-12`) forces `scale` to just be a large finite number instead of `inf`. Downstream, `x_scaled = 0 * huge_scale = 0`, so the zero tensor correctly quantizes to zero rather than propagating NaNs through the matmul.

2. `x_scaled.clamp(-fp8_max, fp8_max)` — this is the actual *saturating* clamp on the numerator, done for the opposite reason: `.to(fp8_dtype)` in PyTorch **wraps/overflows** rather than saturating when a float exceeds the target dtype's representable range (comment literally says this — clamp prevents overflow when casting since PyTorch's default is to wrap, not saturate). Without this second clamp, an outlier value could wrap around to a huge value with the *wrong sign*, silently corrupting the matmul.

So: the first `.clamp(min=EPS)` protects the *scale computation* from a degenerate all-zero input; the second `.clamp(-fp8_max, fp8_max)` protects the *cast* from silent wraparound on outliers. Both are classic "guard the numerics at the boundary" moves you'll see in any quantization codebase (torchao, transformer_engine, bitsandbytes all have equivalent epsilon floors on the amax denominator).

One implementation detail worth noting: `amax.double()` — doing the reciprocal-scale math in fp64 before casting `scale` back to fp32 avoids precision loss when `amax` is very small, since `fp8_max / amax` can itself be numerically sensitive near the epsilon floor.

References:

- [karpathy/nanochat commit e569b59 — custom FP8 quant, replacing torchao](https://github.com/karpathy/nanochat/commit/e569b59f92aea06bf8fc1c48489b3cc2e57189f4)
