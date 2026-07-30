---
audio: false
generated: true
image: false
lang: en
layout: post
title: Einsum in PyTorch Explained
translated: false
type: note
---

Question: What does `einsum` mean/do in PyTorch?

Answer:

`torch.einsum` is Einstein summation notation — a mini-DSL for expressing sums-of-products over tensor indices without manually calling `transpose`/`matmul`/`sum`. You write which indices each input has and which indices survive in the output; any index that's repeated across inputs but *not* in the output gets summed over (contracted).

Signature:

```python
torch.einsum(equation, *tensors)
```

Core rule: `'ij,jk->ik'` means "for output index (i,k), sum over j of A[i,j] * B[j,k]" — that's just matmul.

```python
import torch

A = torch.randn(3, 4)
B = torch.randn(4, 5)

# standard matmul
C1 = A @ B
C2 = torch.einsum('ij,jk->ik', A, B)
torch.allclose(C1, C2)  # True
```

Concrete forward-pass style walk (batched attention scores, the thing you actually use daily):

```python
# Q, K: (batch, heads, seq, dim)
Q = torch.randn(2, 8, 10, 64)
K = torch.randn(2, 8, 10, 64)

# scores[b,h,i,j] = sum_d Q[b,h,i,d] * K[b,h,j,d]
scores = torch.einsum('bhid,bhjd->bhij', Q, K)
# equivalent to: Q @ K.transpose(-2, -1)
print(scores.shape)  # (2, 8, 10, 10)
```

Other common patterns:

```python
# batch matmul
torch.einsum('bij,bjk->bik', A, B)          # == torch.bmm(A, B)

# outer product
torch.einsum('i,j->ij', a, b)               # a[:,None] * b[None,:]

# trace
torch.einsum('ii->', A)                     # A.trace()

# transpose
torch.einsum('ij->ji', A)                   # A.T

# elementwise then sum (dot product per batch row)
torch.einsum('bi,bi->b', a, b)              # (a*b).sum(-1)

# sum over an axis
torch.einsum('ij->i', A)                    # A.sum(dim=1)
```

Mental model: think of it as writing the naive nested-for-loop version of the math, then einsum just tells the backend which loop indices to keep (output) vs contract (summed, repeated-but-absent-from-output). Internally it dispatches to optimized `bmm`/`matmul`/`sum` kernels (via opt_einsum-style path optimization when there are multiple contractions), so it's not slower than hand-written ops — it's a readability/correctness tool, especially once you're juggling >=4D tensors in attention/MoE code where `.transpose().reshape().matmul()` chains get error-prone.

One gotcha: for >2 tensors or long equations, `torch.einsum` finds a contraction order automatically but doesn't always pick the FLOP-optimal one — for perf-critical multi-tensor contractions check `opt_einsum` or just benchmark against manual ops.

References:

- [torch.einsum docs](https://docs.pytorch.org/docs/stable/generated/torch.einsum.html)
- [Einsum is All You Need (Kolter/Rush explainer)](https://rockt.ai/2018/04/30/einsum)
