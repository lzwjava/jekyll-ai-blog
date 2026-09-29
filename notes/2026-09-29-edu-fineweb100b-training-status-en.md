---
audio: false
generated: true
image: false
lang: en
layout: post
title: Edu Fineweb100B Training Status
translated: false
type: note
---

Here's what I found — which configs/models use the `edu_fineweb100B` dataset and their actual status:

## Configs that point at `edu_fineweb100B` (FineWeb-Edu shards)

| Config | Model | Params | Target | Actually trained | Status |
|---|---|---|---|---|---|
| `train_fineweb_gpt3.py` | GPT-2 124M (L12/H12/C768) | 124M | 19,073 iters ≈ 10B tok | 15,180 iters ≈ **7.9B tok** | ⚠️ stopped early (val 3.026) |
| `train_gpt2_200m.py` | GPT-2 ~219M (L18/H16/C896) | 219M | 8,000 iters ≈ 4.2B tok | 2,500 iters ≈ **1.3B tok** | ⚠️ stopped early (val 3.459) |
| `train_gpt2_200m_smoke.py` | same 219M | 219M | 25 iters | smoke test | ✅ done |
| `train_fineweb_760m.py` | GPT-2 760M (L24/H24/C1536) | 760M | 445,000 iters ≈ 14.6B tok | **never run** | ❌ no `out-fineweb-760m/` dir |

## Key findings

1. **Best completed model on this dataset = `out-fineweb-gpt3`** (124M, val loss 3.026). Log shows it ran on an RTX 4070 (12 GB), ~11 s/iter, MFU ~12.8%, and was interrupted at step 15,180 of 19,073 (it was still improving — loss 2.75–3.1 at the end).

2. **`train_fineweb_760m.py` has a bug** — its `shard_dir` points to `/root/nanoGPT/data/fineweb/edu_fineweb100B`, which doesn't exist on this machine. It would need to be `/mnt/data/nanoGPT/data/fineweb/edu_fineweb100B` to run. This 760M model was *planned but never launched*.

3. **Two other "fineweb" configs do NOT use this dataset:**
   - `train_fineweb.py` (→ `out-fineweb`) reads the old `data/fineweb/train.bin` memmap, not the shards.
   - `train_fineweb1_5b.py` (GPT-2 XL 1.5B) also has no `shard_dir`, so it'd read `train.bin` — and was never run either.

## Summary

The `edu_fineweb100B` (140.7B tokens) dataset has been used for:
- **GPT-2 124M** → ~7.9B tokens (incomplete, ~8.6B short of target)
- **GPT-2 219M** → ~1.3B tokens (incomplete, ~3B short)

And was **planned for GPT-2 760M** (14.6B tokens) but never started, plus a broken path that needs fixing.

Want me to resume one of the incomplete runs, or fix and launch the 760M config?