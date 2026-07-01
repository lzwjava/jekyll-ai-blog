---
audio: false
generated: true
image: false
lang: en
layout: post
title: DigitalOcean Storage for GPT-3 XL Training
translated: false
type: note
---

**Question:** For training GPT-3 XL (1.3B) on 30B tokens, how large a DigitalOcean block storage volume do I need?

**Answer:**

## Model Checkpoint Size

```
1.3B parameters
fp32 weights:     1.3B × 4 bytes = 5.2GB
AdamW states:
  grads:          5.2GB
  momentum m:     5.2GB
  variance v:     5.2GB
total per ckpt:   ~21GB
```

Keep last 3 checkpoints:

```
21GB × 3 = 63GB
```

## Data Size

30B tokens, GPT-2 BPE, stored as uint16:

```
30B tokens × 2 bytes = 60GB
+ raw text (before tokenization): ~80GB
```

If you **delete raw text after tokenizing** (recommended):

```
tokens only: 60GB
```

## Full Breakdown

| Item | Size | Keep? |
| ------ | ------ | ------- |
| Raw text (download) | 80GB | delete after tokenizing |
| Tokenized train.bin | 57GB | ✅ |
| Tokenized val.bin | 3GB | ✅ |
| Checkpoints (last 3) | 63GB | ✅ |
| Best checkpoint fp16 | 2.6GB | ✅ |
| Logs / wandb / misc | 3GB | ✅ |
| **Total (after deleting raw)** | **~129GB** | |
| **Total (keeping raw)** | **~209GB** | |

## Recommendation

**200GB volume**

```
Cost at rest:
$0.00015 × 200GB = $0.03/hr
$0.03 × 24 × 30  = $21.60/month idle

During training (5 days):
Volume cost negligible vs $2/hr GPU
```

## Why Not 150GB?

```
129GB used + headroom:
  mid-training temp files: ~5GB
  pip packages, conda env: ~8GB
  unexpected data growth:  ~10GB
  ──────────────────────────────
  safe floor: ~152GB  ← too tight

200GB gives ~70GB breathing room ✅
```

## Bottom Line

```
200GB volume
$21.60/month idle
$0.75 for 5-day training period (volume portion)
Total training cost: ~$240 GPU + $0.75 volume = ~$241
```

Same recommendation as GPT-2 XL coincidentally — **200GB is your sweet spot** for this scale of experiment.
