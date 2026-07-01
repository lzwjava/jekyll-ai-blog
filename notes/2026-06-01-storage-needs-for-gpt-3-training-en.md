---
audio: false
generated: true
image: false
lang: en
layout: post
title: Storage Needs for GPT-3 Training
translated: false
type: note
---

**Question:** For training GPT-3 scale from scratch, how large a volume do I need for everything — raw text, tokenized data, and all checkpoints?

**Answer:**

## GPT-3 Model Size First

```
GPT-3: 175B parameters
float32:  175B × 4 bytes = 700GB per checkpoint
float16:  175B × 2 bytes = 350GB per checkpoint
bfloat16: 175B × 2 bytes = 350GB per checkpoint
```

With AdamW optimizer states (float32 master copy + moments):

```
float32 master weights:  700GB
gradients:               700GB
momentum (m):            700GB
variance (v):            700GB
total:                  ~2.8TB per training checkpoint
```

## Reality Check — You Cannot Train True GPT-3 on MI300X

```
MI300X HBM:     192GB
GPT-3 fp16:     350GB minimum (weights alone)
                ──────────────────────────────
                doesn't fit in a single GPU
```

Even with model parallelism across multiple MI300X, a single droplet won't cut it. True GPT-3 training requires:

- 800-1000x A100 80GB (as OpenAI used)
- Or ~50x MI300X with tensor+pipeline parallelism

## What You Probably Mean — GPT-3 Small/Medium Scale

OpenAI's GPT-3 paper defines several sizes:

| Model | Params | fits MI300X? |
| ------- | -------- | -------------- |
| GPT-3 Small | 125M | ✅ trivially |
| GPT-3 Medium | 350M | ✅ |
| GPT-3 Large | 760M | ✅ |
| GPT-3 XL | 1.3B | ✅ |
| GPT-3 2.7B | 2.7B | ✅ |
| GPT-3 6.7B | 6.7B | ✅ |
| GPT-3 13B | 13B | ✅ tight |
| GPT-3 175B | 175B | ❌ needs ~50x MI300X |

## Realistic Target: GPT-3 6.7B on MI300X

```
6.7B × 4 bytes (fp32) = 26.8GB weights
AdamW full states:
  weights:    26.8GB
  grads:      26.8GB
  momentum:   26.8GB
  variance:   26.8GB
  total:     ~107GB  ← fits in 192GB HBM3 ✅
```

## Volume Size Breakdown for 6.7B

| Item | Size | Notes |
| ------ | ------ | ------- |
| Raw text (Pile-scale) | 800GB | The Pile is 825GB |
| Tokenized `.bin` | 400GB | ~half after BPE tokenization |
| Checkpoint fp32+AdamW | 107GB | full training state |
| Keep last 3 checkpoints | 321GB | |
| Best checkpoint fp16 | 13GB | inference only |
| Logs, misc | 5GB | |
| **Total** | **~1.5TB** | |

## Volume Recommendation by Target Model

| Target | Volume Size | Cost at rest/month |
| -------- | ------------ | ------------------- |
| GPT-3 Small (125M) | 200GB | $21/mo |
| GPT-3 XL (1.3B) | 300GB | $32/mo |
| GPT-3 6.7B | 1.5TB | $162/mo |
| GPT-3 13B | 2.5TB | $270/mo |
| GPT-3 175B | forget it | need cluster |

## My Recommendation for You

Given your MI300X (192GB HBM3), target **GPT-3 6.7B** — it's the largest model that fits comfortably with full AdamW states, and it's a meaningful scale jump from GPT-2 XL (1.5B).

```
Volume: 1TB initially
Cost:   $0.00015 × 1000GB = $0.15/hr at rest
        $0.15 × 24 × 30  = ~$108/month idle
```

If budget is tight, start with **GPT-3 2.7B** on a **500GB volume** (~$54/month idle) — still a serious model, half the storage cost.

## Practical Config

```python
# nanoGPT config for 6.7B
n_layer = 32
n_head = 32
n_embd = 4096
block_size = 2048

out_dir = '/mnt/data/checkpoints'
# with MI300X 192GB, can do decent batch size
batch_size = 16
gradient_accumulation_steps = 40  # effective batch ~640
```

## Bottom Line

"GPT-3" as OpenAI built it = not feasible solo. But **GPT-3 6.7B** on your MI300X is totally legit, meaningful research-grade training, and that needs a **1TB volume** at ~$108/month idle — or spin it down and snapshot just the checkpoints when not training.
