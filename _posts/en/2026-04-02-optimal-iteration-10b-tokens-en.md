---
audio: false
generated: true
image: false
lang: en
layout: post
title: Optimal Iteration Count for 10B Tokens
translated: false
type: note
---

Based on your config, let me calculate whether 100,000 iterations is appropriate for 10B tokens of FineWeb:

## Current Token Throughput

With your config:

- Batch size: 16
- Block size: 1024 tokens
- Gradient accumulation: 64

**Effective batch size tokens** = 16 × 1024 × 64 = **1,048,576 tokens** (~1M tokens per iteration)

**Total tokens over 100K iterations** = 100,000 × 1M = **100B tokens**

## For 10B Tokens

To process 10B tokens:

- Required iterations = 10B ÷ 1M = **~10,000 iterations**

## Answer

**No, you don't need 100K iterations for 10B tokens.** With your current batch size, 100K iterations would process **100B tokens** — that's 10× your intended 10B dataset.

## Suggested Configurations

### For 10B tokens (as implied in comments)

```python
max_iters = 10000  # Actually ~10B tokens
lr_decay_iters = 10000
# Keep warmup_iters = 500 (5% of total is reasonable)
```

### For 100B tokens (if you want to use 100K iters)

```python
max_iters = 100000  # ~100B tokens
# This would be a 100B token run, suitable for larger pretraining
```

### If you want to keep 100K but match 10B

```python
# Option 1: Reduce batch size
gradient_accumulation_steps = 6  # 6 instead of 64
batch_size = 16
# Results in ~100K tokens/iteration × 100K = 10B tokens

# Option 2: Reduce block size
block_size = 256  # instead of 1024
# Results in ~262K tokens/iteration × 100K = 26B tokens
```

## Recommendation

For 10B tokens on a 1.5B parameter model, **10K iterations** is appropriate. The original 100K iterations comment seems to assume a much smaller batch size or longer training run. Stick with 10K iterations for your 10B token target.
