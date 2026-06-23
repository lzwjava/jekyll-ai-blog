---
audio: false
generated: true
image: false
lang: en
layout: post
title: Same Information, Different Scale
translated: false
type: note
---

Yes, exactly.

**PPL = exp(L)** where L is the cross-entropy loss — they are the same information, different scale.

```python
import torch
import torch.nn.functional as F

logits = torch.randn(8, 512, 50257)   # (batch, seq_len, vocab)
targets = torch.randint(0, 50257, (8, 512))

loss = F.cross_entropy(logits.view(-1, 50257), targets.view(-1))
ppl  = torch.exp(loss)

print(f"loss={loss:.4f}  ppl={ppl:.1f}")
# loss=10.8239  ppl=50257.0  ← random init → ppl ≈ vocab_size ✓
```

The relationship is exact:

```
L   = -1/N · Σ log P(xᵢ | x<ᵢ)    # nats (natural log)
PPL = exp(L)
```

So:

| L (loss) | PPL | Meaning |
|----------|-----|---------|
| ln(50257) ≈ 10.82 | ~50257 | random model |
| 3.0 | ~20 | GPT-2 small on WebText |
| 1.5 | ~4.5 | strong model |
| 0.0 | 1.0 | perfect / memorized |

**Why two names for the same thing?**

- **L (loss)** is what the optimizer sees — additive, differentiable, numerically stable
- **PPL** is what humans read — "model is as uncertain as picking from N equally likely tokens"

In your nanoGPT training loop, you're already minimizing PPL — you just see it as `loss`. Log it both ways:

```python
print(f"iter {step} | loss {loss.item():.4f} | ppl {torch.exp(loss).item():.1f}")
```

On your MI300X GPT-2 760M run: what's your current val loss settling at? Should be around 2.85–3.1 on OpenWebText after full training.
