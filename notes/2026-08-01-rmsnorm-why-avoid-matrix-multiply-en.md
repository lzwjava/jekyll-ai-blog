---
audio: false
generated: true
image: false
lang: en
layout: post
title: "RMSNorm: Why Avoid Matrix Multiply"
translated: false
type: note
---

Here's the answer in English:

## Why not use `@` (matrix multiplication)?

RMSNorm's two steps are neither linear transforms nor involve the "sum-contraction" that `@` performs:

**1. Normalization: per-token scaling, not per-token matmul**

```python
var = x.pow(2).mean(dim=-1, keepdim=True)          # shape (N, 1), N = num_tokens
x.mul_(torch.rsqrt(var + self.eps))                # each token scaled by its own scalar
```

The normalization factor `1/√(var+eps)` is a *single scalar shared across all features in a row*. `@` performs a **sum over a contraction dimension** — there is no sum here at all. If you forced it with `@`, you'd need to build `diag(scale)`, an `(N, N)` diagonal matrix:

- Compute: `diag(s) @ x` is O(N²) in the number of *tokens*; element-wise multiply is O(N)
- Memory: an extra O(N²) diagonal matrix, semantically pointless

**2. Weight scaling: a diagonal linear map, not a full matrix**

```python
x = x.to(orig_dtype).mul_(self.weight)   # weight shape (hidden,), broadcast per column
```

Mathematically, `x * weight` is equivalent to `x @ diag(weight)` — a **diagonal** matrix product. Using `@` means materializing a `(hidden, hidden)` diagonal matrix and doing O(hidden²) matmul, where element-wise multiply is O(hidden).

If you wanted a *real* matrix multiply, that's `nn.Linear` (a fully learnable matrix). RMSNorm's weight is deliberately constrained to "one gain per dimension," so the Hadamard (element-wise) product is its intrinsic form.

## Why `mul_` (in-place) instead of `mul`?

```python
x = x.float()                       # fresh fp32 copy
...
x = x.to(orig_dtype).mul_(self.weight)
```

- **One fewer allocation**: `mul` returns a new tensor; `mul_` rewrites in place, producing no temporary. On the inference path every token passes through this on every layer, so each avoided allocation is one fewer kernel launch and less memory churn.
- **Safety**: by this point `x` is already a freshly-created copy from `x.float()` / `x.to(orig_dtype)` with no external references, so mutating it in place can't corrupt the caller's original tensor.
- **Numerics**: the statistics are computed in fp32, then the result is cast back to the original dtype before the weight scaling. Weight scaling is precision-safe (a multiply by a constant factor), so it can be done in place.

## TL;DR

`@` is sum-contraction (matmul); RMSNorm is pointwise scaling (normalization factor per row, weight per column). Using `@` would be equivalent to multiplying by a giant diagonal matrix — an O(n²) waste versus O(n). `mul_` just does that pointwise scaling in place, saving memory and allocations.
