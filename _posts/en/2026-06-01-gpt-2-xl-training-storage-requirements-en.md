---
audio: false
generated: true
image: false
lang: en
layout: post
title: GPT-2 XL Training Storage Requirements
translated: false
type: note
---

**Question:** For training GPT-2 XL from scratch, how large a volume do I need to store everything — raw text data, tokenized data, and all checkpoints?

**Answer:**

## GPT-2 XL Model Size First

```
GPT-2 XL: 1.5B parameters
float32:  1.5B × 4 bytes = 6GB per checkpoint
float16:  1.5B × 2 bytes = 3GB per checkpoint
bfloat16: 1.5B × 2 bytes = 3GB per checkpoint
```

With optimizer states (AdamW stores 2 momentum terms):

```
float32 model + AdamW:
  params:          6GB
  grad:            6GB
  momentum (m):    6GB
  variance (v):    6GB
  total:          ~24GB per training checkpoint
```

## Full Breakdown

| Item | Size | Notes |
|------|------|-------|
| Raw text (WebText-scale) | 40GB | OpenWebText ~40GB compressed |
| Tokenized `.bin` files | 40GB | roughly same size after GPT-2 BPE |
| Model checkpoint (fp32+AdamW) | 24GB | full training state |
| Keep last 3 checkpoints | 72GB | safe rollback |
| Best checkpoint (inference only) | 3GB | fp16 weights only |
| Logs, tensorboard, misc | 2GB | |
| **Total** | **~157GB** | |

## Recommendation

**200GB volume** — gives you ~40GB breathing room.

```
$0.00015/GB/hour × 200GB = $0.03/hour at rest
$0.03 × 24 × 30 = ~$21.60/month
```

Cheap insurance vs running out of space mid-training at $2/hr GPU time.

## Directory Layout on Volume

```bash
/mnt/data/
├── raw/
│   └── openwebtext/        # ~40GB raw text
├── tokens/
│   └── train.bin           # ~40GB tokenized
│   └── val.bin
├── checkpoints/
│   ├── ckpt_step_10000.pt  # ~24GB each
│   ├── ckpt_step_20000.pt
│   └── ckpt_best.pt        # ~3GB fp16
└── logs/
    └── tensorboard/
```

## Practical nanoGPT Config for This

```python
# In your train.py / config
out_dir = '/mnt/data/checkpoints'
dataset = '/mnt/data/tokens'

# Save every N steps, keep last 3
save_interval = 1000
keep_last_n = 3
```

## Bottom Line

Pick **200GB** → costs **$0.03/hr** at rest, ~$21/month idle. Versus losing a training run because you hit disk full at step 50,000 — not worth it.
