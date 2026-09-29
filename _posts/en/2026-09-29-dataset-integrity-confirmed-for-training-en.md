---
audio: false
generated: true
image: false
lang: en
layout: post
title: Dataset Integrity Confirmed for Training
translated: false
type: note
---

Yes, it's OK — I verified the dataset. It's a well-formed, ready-to-train corpus. Here's what I confirmed:

## Dataset integrity check ✅

| Property | Value |
| --- | --- |
| Location | `data/fineweb/edu_fineweb100B/` |
| Shards | **1408** = 1407 train + 1 val |
| Total tokens | **~140.7B** |
| Shard size | 100M tokens each (~191 MB) |
| Dtype | `uint16` ✓ |
| Tokenizer | GPT-2 (`vocab 50257`) |
| Token ID range | 0 … 50256 ✓ (valid) |
| Doc delimiter | `<\|endoftext\|>` prepended per doc ✓ |

## It's wired up correctly in `train.py`

```python
shard_dir = '.../edu_fineweb100B'
_train_shards = glob('edufineweb_train_*.npy')   # 1407 shards
_val_shards  = glob('edufineweb_val_*.npy')      # 1 shard (100M tokens)
```

Each step samples a random shard and loads `block_size` contiguous tokens — the standard nanoGPT sharded-loader flow. This is exactly what the `train_fineweb_gpt3.py`, `train_fineweb.py`, and `train_gpt2_200m.py` configs already used.

## Two small notes (not blockers)

1. **Name vs. actual size:** the dir is named `edu_fineweb100B`, but it actually holds **~140.7B tokens**, not 100B. That's more data, which is fine — just be aware your "100B" run actually has ~140B available.

2. **Val split is only 1 shard (100M tokens)** — plenty for eval, no action needed.

So yes: it's a clean, complete FineWeb-Edu corpus, and it's safe/appropriate to train on. What config/model were you planning to train with it?
