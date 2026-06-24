---
audio: false
generated: true
image: false
lang: en
layout: post
title: Delete First, Learn Attention
translated: false
type: note
---

**Question:** What's your goal in simplifying Transformer and attention — what are you actually trying to strip away, and what would "simpler than nanoGPT" look like?

**Answer:**

You're thinking like Karpathy did when he wrote nanoGPT, but one step further. The Musk principle: *delete first, justify adding back*.

Here's what I think you're actually targeting:

**What nanoGPT still has that you could delete:**

```python
# nanoGPT has all this ceremony:
- Learning rate scheduler (cosine warmup)
- Gradient clipping
- Weight decay / AdamW tuning
- Dropout
- Flash attention
- DDP multi-GPU
- Checkpoint save/load
- Wandb logging
- Gradient accumulation
- Mixed precision (fp16/bf16)
```

**Your "plain congee" version — absolute minimum that still learns:**

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

# Everything in ~100 lines, no config, no classes you don't need

B, T, C = 4, 64, 64  # batch, context, channels
vocab = 65  # Shakespeare chars

# Single attention head — see the raw mechanism
def attention(q, k, v):
    T = q.size(-2)
    w = q @ k.transpose(-2, -1) / C**0.5          # (B, T, T)
    w = w.masked_fill(torch.triu(torch.ones(T,T), diagonal=1).bool(), float('-inf'))
    w = F.softmax(w, dim=-1)
    return w @ v                                   # (B, T, C)

# One block — no class, just functions
def block(x, Wqkv, Wproj, W1, W2):
    B, T, C = x.shape
    qkv = x @ Wqkv                                # (B, T, 3C)
    q, k, v = qkv.split(C, dim=-1)
    x = x + attention(q, k, v) @ Wproj
    x = x + F.relu(x @ W1) @ W2                  # FFN
    return x

# No learning rate schedule — just constant lr
# No gradient clipping
# No dropout
# No checkpoint
# SGD instead of AdamW even
```

**The real insight you're pointing at:**

nanoGPT teaches Transformer. Your version should teach *why attention works at all* — the single question: **"how does token i look at token j?"**

Strip to that. One head. No multi-head. No positional encoding even (let it fail, then add). Watch the loss curve. That's the learning.

**删掉顺序 (deletion order):**

1. Multi-head → single head
2. AdamW → SGD
3. LR schedule → constant
4. LayerNorm → nothing (see it break)
5. Residual → nothing (see it break)
6. Multiple blocks → one block
7. DataLoader → `x = data[i:i+T]` inline

Each deletion teaches you what that piece actually *does* — which is the whole point of building it yourself.

You're not building a tool. You're building a microscope. Simpler is sharper.
