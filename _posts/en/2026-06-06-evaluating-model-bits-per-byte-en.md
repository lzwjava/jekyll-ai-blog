---
audio: false
generated: true
image: false
lang: en
layout: post
title: Evaluating Model Bits per Byte
translated: false
type: note
---

**Question:** What does "val bpb" mean for your nanochat model, and is 0.8658 bpb good?

**Answer:**

**bpb** = **bits per byte** — a language-agnostic evaluation metric for language models.

It measures how many bits you need to encode one byte of validation data on average:

```
bpb = cross_entropy_loss / ln(2)
```

**Is 0.8658 bpb good?**

Yes, that's solid. Context:

- **English text** (Wikipedia, books): typically 1.5–2.0 bpb
- **Your nanochat-d12 on validation set**: 0.8658 bpb → well below natural English
  - This is expected; validation losses are usually lower than real-world perplexity because the validation set often comes from the same distribution as training
  - Suggests your model isn't overfitting badly (Chinchilla-optimal ratio helps)

**Related metric — perplexity:**
```
perplexity = 2^bpb = 2^0.8658 ≈ 1.84
```

This is exceptionally low perplexity for a 286M model with just 5.7B tokens. For comparison:
- GPT-2 (1.5B tokens): ~29 perplexity on WikiText-103
- Your model: ~1.84 on your validation set (likely a subset of pretraining data)

**Practical takeaway:** Your model is memorizing/fitting the validation set very well. This is normal and good during training. The real test is generalization—how it performs on held-out data outside the training distribution. If your downstream tasks (next-token prediction on novel text, instruction-following, etc.) perform well, this bpb is a strong signal.

**Quick check:** What's your test set bpb? If test bpb >> val bpb, you have distribution shift or overfitting to watch.
