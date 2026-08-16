---
audio: false
generated: true
image: false
lang: en
layout: post
title: FP8 grad_weight backward GEMM layout
translated: false
type: note
---

This is the **`grad_weight` GEMM** in the backward pass of the FP8 linear layer. Here's the full breakdown:

## The math

For a linear layer `output = input @ weight.T` with shapes:

- `input`: `[B, K]`, `weight`: `[N, K]` → `output`: `[B, N]`

Backprop gives `grad_weight = grad_output.T @ input`, i.e. `[N, B] @ [B, K] → [N, K]` (same shape as the weight, which is what the autograd function must return).

## The layout problem

`torch._scaled_mm` is strict about memory layout:

- **1st arg (A): must be row-major (contiguous)**
- **2nd arg (B): must be column-major**

The saved FP8 tensors don't satisfy this for GEMM 2:

- `go_fp8` is `[B, N]` contiguous (row-major) — but we need `[N, B]` as the first arg
- `in_fp8` is `[B, K]` contiguous (row-major) — but the second arg must be column-major

So each operand needs rearrangement:

```python
go_T = go_fp8.t().contiguous()   # [N, B] row-major
in_col = _to_col_major(in_fp8)   # [B, K] column-major
```

**`go_T`**: `go_fp8.t()` alone would be `[N, B]` with column-major strides `(1, B)` — wrong for the first slot. `.contiguous()` forces a physical copy that rearranges memory into row-major strides `(B, 1)`. This is a real memory copy (a "transpose + copy" kernel).

**`in_col`**: `_to_col_major` does `x.t().contiguous().t()`. For `in_fp8` this yields the same logical `[B, K]` shape but with column-major strides `(1, B)` instead of `(K, 1)`, so the kernel reads down columns efficiently.

## The scales

`scale_a=go_inv` and `scale_b=in_inv` are the **inverse** quantize scales (from `_to_fp8`). The kernel computes:

```
grad_weight = (go_T * go_inv) @ (in_col * in_inv)   # in FP8 arithmetic
```

The dequantization is folded into the cuBLAS kernel itself, so `grad_weight` comes out in full precision (`grad_output.dtype`). No separate dequantize step is needed.

## Why `use_fast_accum=False` here

- `use_fast_accum=True` accumulates dot products in reduced precision (faster, slightly less accurate) — used in the **forward** pass.
- Backward uses `False` so the `[N, B] @ [B, K]` dot products accumulate in fp32, keeping gradients as precise as possible. Gradients are the most numerically sensitive part of training (they get multiplied into the optimizer state), so precision is worth the tiny speed cost.

## One subtlety: why a copy is unavoidable for the first arg

Contrast with GEMM 1 (`grad_input = grad_output @ weight`): there, `w_fp8` is `[N, K]` contiguous, so `w_fp8.t()` already has column-major strides — *no copy needed* (that's why GEMM 1 is cheap to set up). GEMM 2 needs a transpose in the *first* slot, which forces the `.contiguous()` copy. Both `go_T` and `in_col` are only computed once and reused — note `go_fp8` is shared between GEMM 1 and GEMM 2, so the quantization work is amortized across both backward matmuls.

In short: this is the standard `grad_output.T @ input` matmul, quantized to FP8 (e5m2 for the gradient, e4m3 for the input), with layout adjustments to satisfy `_scaled_mm`'s A-row-major / B-column-major requirement, dequantized internally by the scales, and accumulated in full precision for gradient accuracy.
