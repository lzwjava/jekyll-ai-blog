---
audio: false
generated: true
image: false
lang: en
layout: post
title: PyTorch Matmul Shape Broadcasting
translated: false
type: note
---

Question: How does PyTorch's `@` operator (matmul) intelligently determine output shapes, especially in batched attention like `(B, nh, T, T) @ (B, nh, T, hs) → (B, nh, T, hs)`?

Answer:

PyTorch's `@` operator (matrix multiplication) uses **broadcasting rules + dimension contraction logic** that automatically handles batched operations. Here's what's actually happening:

## The matmul Broadcasting Rules

```python
# Rule: A @ B contracts the LAST dimension of A with SECOND-TO-LAST of B
# All leading dimensions broadcast together like NumPy

# For your attention case:
# att:  (B, nh, T, T)   <- last dim is T (size to contract)
# v:    (B, nh, T, hs)  <- second-to-last dim is T (size to contract)
# Result: (B, nh, T, hs)

# Here's what actually happens:
# 1. Treat (B, nh) as batch dimensions that broadcast
# 2. For each (b, h) pair, do: (T, T) @ (T, hs) = (T, hs)
# 3. Stack results back: (B, nh, T, hs)
```

The **contraction dimension** (T) is implicit:
- `att` gives up its last dim T
- `v` gives up its second-to-last dim T
- These two T's must match (they do), and they **contract out**

The remaining dimensions **stack left-to-right**:
- From `att`: (B, nh, T) — the "row" dimension
- From `v`: (hs) — the "column" dimension
- Result: (B, nh, T, hs)

## Why This Works (The Math)

Standard matrix multiplication: `A[m, n] @ B[n, k] = C[m, k]`

In your case:
- `att` is shaped `(B, nh, T, T)` — think of it as a **batch of (B×nh) matrices**, each (T, T)
- `v` is shaped `(B, nh, T, hs)` — think of it as a **batch of (B×nh) matrices**, each (T, hs)

PyTorch flattens the batch dims, does `(B*nh, T, T) @ (B*nh, T, hs) = (B*nh, T, hs)`, then reshapes back.

## The Implementation (Under the Hood)

```python
import torch

# Minimal example
B, nh, T, hs = 2, 4, 3, 8

att = torch.randn(B, nh, T, T)  # (2, 4, 3, 3)
v = torch.randn(B, nh, T, hs)    # (2, 4, 3, 8)

# What @ does internally (simplified):
# 1. Reshape to (B*nh, T, T) and (B*nh, T, hs)
# 2. Use batched GEMM (general matrix multiply)
# 3. Reshape back to (B, nh, T, hs)

y = att @ v  # (2, 4, 3, 8) ✓

# Verify the contraction:
print(y.shape)  # torch.Size([2, 4, 3, 8])

# Manual verification (slower but shows the logic):
y_manual = torch.zeros(B, nh, T, hs)
for b in range(B):
    for h in range(nh):
        y_manual[b, h] = att[b, h] @ v[b, h]  # (T, T) @ (T, hs) = (T, hs)

assert torch.allclose(y, y_manual)
```

## Why It's "Smart"

The real genius is **you don't have to reshape manually**. PyTorch's `matmul`:
1. Infers batch dimensions (all leading dims except the last two)
2. Verifies the contraction dimension matches (T == T)
3. Calls optimized GEMM kernels for batched operation
4. Returns the result without you writing a loop

Compare to explicit loop (what happens under the hood):
```python
# Without @ smartness, you'd write:
y = torch.zeros(B, nh, T, hs)
for b in range(B):
    for h in range(nh):
        y[b, h] = att[b, h] @ v[b, h]  # ← You code this

# With @, one line handles all of it:
y = att @ v  # ← Compiler figures out the batch loop
```

The `@` operator is a thin wrapper around `torch.matmul()`, which dispatches to optimized BLAS/cuBLAS routines (or custom CUDA kernels). It's not actually determining the shape dynamically—it's **following rigid rules** (batch broadcast + contract last/second-to-last) that happen to work perfectly for attention.
