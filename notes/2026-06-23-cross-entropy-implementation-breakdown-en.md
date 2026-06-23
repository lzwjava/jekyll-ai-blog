---
audio: false
generated: true
image: false
lang: en
layout: post
title: Cross Entropy Implementation Breakdown
translated: false
type: note
---

**Question:** How is `F.cross_entropy` implemented internally? Show the algorithm.

**Answer:**

## `F.cross_entropy` — From PyTorch Source to Math

### What it does in one line

```
F.cross_entropy(logits, targets) = NLL(log_softmax(logits), targets)
```

Two steps fused: **log_softmax** + **negative log likelihood**.

---

### Pure Python implementation (exactly what PyTorch does)

```python
import torch

def cross_entropy_manual(logits, targets):
    """
    logits:  (B, C) raw unnormalized scores
    targets: (B,)   integer class indices
    """
    B, C = logits.shape

    # Step 1: log_softmax (numerically stable via logsumexp trick)
    # Subtract max for stability — doesn't change softmax result
    # because exp(x_i - max) / Σ exp(x_j - max) = exp(x_i) / Σ exp(x_j)
    m = logits.max(dim=1, keepdim=True).values        # (B, 1)
    shifted = logits - m                               # (B, C)
    log_sum_exp = shifted.exp().sum(dim=1, keepdim=True).log()  # (B, 1)
    log_softmax = shifted - log_sum_exp                # (B, C)

    # Step 2: NLL — pick the log-prob of the correct class
    # log_softmax[i, targets[i]] for each i in batch
    nll = -log_softmax[torch.arange(B), targets]      # (B,)

    # Step 3: mean reduction (default)
    return nll.mean()


# --- verify ---
torch.manual_seed(0)
B, C = 4, 10
logits = torch.randn(B, C)
targets = torch.randint(0, C, (B,))

loss_manual = cross_entropy_manual(logits, targets)
loss_pytorch = torch.nn.functional.cross_entropy(logits, targets)

print(f"manual:  {loss_manual.item():.6f}")
print(f"pytorch: {loss_pytorch.item():.6f}")
# manual:  2.453069
# pytorch: 2.453069  ✓
```

---

### The logsumexp trick — why it matters

Naive version **overflows** for large logits:

```python
# WRONG — exp(1000) = inf on float32
softmax = logits.exp() / logits.exp().sum()
log_softmax = softmax.log()  # nan

# CORRECT — shift by max, mathematically identical
# log(exp(x_i) / Σ exp(x_j))
# = log(exp(x_i - m) / Σ exp(x_j - m))   [m cancels]
# = (x_i - m) - log(Σ exp(x_j - m))
```

In nanoGPT's training loop, logits from a 760M model can be large — this trick is why you never see NaN losses from softmax overflow.

---

### One-hot label case (what you always hit in LM training)

For language modeling, `targets` is a single integer per position (next token). The NLL step collapses to:

```python
# Instead of full matrix multiply, just index:
loss = -log_softmax[batch_idx, targets[batch_idx]]
```

The entire `(B, C)` log_softmax matrix is computed but only `B` values are used. This is the main reason **fused kernels** exist — CUDA can avoid materializing the full softmax.

---

### What actually runs in C++/CUDA

```
F.cross_entropy
  → torch._C._nn.cross_entropy_loss
    → at::nll_loss_nd (for target)
    → at::log_softmax (CUDA kernel: "log_softmax_cuda_kernel")
```

The CUDA kernel does the logsumexp in a **single pass** over the logit vector using warp-level reductions — no intermediate softmax tensor allocated on GPU. That's the real speedup vs doing `log(softmax(x))` separately.

---

### nanoGPT usage in context

```python
# from nanoGPT/model.py — GPT.forward()
def forward(self, idx, targets=None):
    logits, _ = self.transformer(idx)          # (B, T, vocab_size)

    if targets is not None:
        # flatten (B, T, V) → (B*T, V) and (B, T) → (B*T,)
        loss = F.cross_entropy(
            logits.view(-1, logits.size(-1)),  # (B*T, vocab_size)
            targets.view(-1),                  # (B*T,)
            ignore_index=-1                    # mask padding tokens
        )
```

`ignore_index=-1` means padding positions don't contribute to the loss — internally PyTorch just zeroes those NLL values before averaging.

---

### Mental model

```
logits (B, C)
    │
    ▼
[subtract max per row]        ← overflow prevention
    │
    ▼
[exp → sum → log]             ← log(Σ exp(xⱼ - m))
    │
    ▼
log_softmax = x_i - m - log_sum_exp   ← log prob per class
    │
    ▼
[index by target class]       ← pick log p(y_true)
    │
    ▼
nll = -log_softmax[target]    ← surprise for correct class
    │
    ▼
loss = mean(nll)              ← scalar
```
