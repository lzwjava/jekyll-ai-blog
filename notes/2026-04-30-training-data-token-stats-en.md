---
audio: false
generated: true
image: false
lang: en
layout: post
title: Training Dataset and Token Statistics
translated: false
type: note
---

**Dataset sizes**

| File                | Size    | Contents                                                    |
| ------------------- | ------- | ----------------------------------------------------------- |
| `train_fineweb.txt` | 16 GB   | 89.6M lines of raw text (sample doc above is news/web text) |
| `train.bin`         | 7.36 GB | **3.68B GPT-2 BPE tokens** (uint16)                         |
| `val.bin`           | 12 KB   | 5,675 tokens — **tiny**, this is why val loss is jittery    |

**Training coverage**
- Tokens seen: 12,000 iters × 524,288 = **6.29B tokens**
- Epochs over `train.bin`: **~1.71** (each token seen <2× on average)

**Notes**
- Compression ratio ~2.2× (16 GB text → 7.36 GB tokens) is normal for GPT-2 BPE — ~3.7 chars/token.
- `val.bin` at 5,675 tokens is suspiciously small (~5 evaluation batches at block_size=1024). The eval_iters=200 setting will mostly re-sample the same chunk. If you re-prepare the data, carve out a real holdout (e.g., 0.5% of train.bin = ~18M tokens) — your val loss numbers would be more trustworthy.
- For reference: Chinchilla-optimal training for a 124M model is ~2.5B tokens, so at 6.3B tokens you're actually past compute-optimal. The ceiling on this run is the model size, not data — to push val loss lower without scaling the model, training longer won't help much.