---
audio: false
generated: true
image: false
lang: en
layout: post
title: FineWeb Dataset and Training Explanation
translated: false
type: note
---

Three things going on here. Let me untangle them.

## 1. Why the corpus is 140B but training "sees" 10B

These are independent. The downloader fills a **pool**; `max_iters` decides the **training budget**. They don't have to match.

**Corpus on disk** (`data/fineweb/edu_fineweb100B/`):
- 1407 train shards × 100M tokens + 1 val shard = **~140.7B tokens** (uint16 .npy, 263 GB)
- Each shard from `prepare_fineweb.py` is `shard_size = 1e8` exactly

**Training budget** (config `train_fineweb_gpt3.py:29`):
- `max_iters = 19073` × 524,288 tokens/step ≈ **10.0B tokens**
- The comment on that line literally says: `# ~10B tokens; bump toward ~190k for full 100B`

**Sampler** (`train.py:126–129`): every batch picks a **random shard** then **random positions** inside it. With replacement. Over 19k iters it samples ~7% of the corpus — many tokens never seen once, none seen twice. So having extra shards costs nothing; the model just samples from a bigger pool.

## 2. Why the downloader was sized for "100B / 400 GB" but produced 140B

`plan_and_download_fineweb_gpt3.py:40` uses `BYTES_PER_TOKEN = 4.0`, then downloads until raw parquet bytes ≥ 400 GB. That 4× ratio is conservative — real FineWeb-Edu English under the GPT-2 BPE is closer to **~2.85 bytes/token**, so 400 GB of raw text tokenizes to **~140B tokens, not 100B**. Not a bug, just a loose estimate biased toward "download a bit too much" rather than too little. Folder is named `edu_fineweb100B`, which is now misleading — it's effectively a 140B-token corpus.

## 3. "Bigger model → more tokens? More iters → overfit?"

**More tokens, yes.** Chinchilla rule of thumb is ~20 tokens / parameter for compute-optimal training; recent practice (LLaMA / GPT-3 style) trains 5–40× past that for better inference-time quality. Rough targets:

| model                | params | Chinchilla (~20×) | "overtrained" (~80×) |
| -------------------- | ------ | ----------------- | -------------------- |
| GPT-2 124M (current) | 124 M  | 2.5 B             | ~10 B ← you are here |
| GPT-2 medium         | 350 M  | 7 B               | ~28 B                |
| GPT-2 large          | 770 M  | 15 B              | ~60 B                |
| GPT-2 XL             | 1.5 B  | 30 B              | ~120 B               |

So with 140B on disk you can comfortably go to ~1B params Chinchilla-optimal, or train medium/large to "overtrained" regime. Note medium won't fit at the current `batch_size=4 × block_size=1024` on a 12 GB 4070 — you'd need to drop micro-batch to 1–2 and bump `gradient_accumulation_steps` to keep 0.5M tokens/step.

**More iters → overfit?** *Not in this setup.* Overfitting needs many epochs over a finite dataset. Here the sampler draws fresh positions from 140B tokens with replacement; 19k iters cover ~10B / 140B ≈ 7% of the corpus. Increasing `max_iters` just walks further along the Chinchilla curve with diminishing returns — train loss keeps dropping, val tracks it, no overfit. You'd only see overfitting if (a) you shrank the pool, or (b) you trained long enough to loop the corpus many times (≥ ~140B × several = hundreds of B tokens, i.e. multiplying iters by ~20+).

## Practical next steps

If you want a stronger model from the **same** 140B pool:

- **Easiest win**: keep 124M, extend `max_iters` to ~38k (≈20B, 160 tok/param) — still ~1 day on this box. Cosine schedule needs `lr_decay_iters` bumped too.
- **Bigger model**: switch to gpt2-medium (`n_layer=24, n_head=16, n_embd=1024` → 350M), drop `batch_size` to 1–2, raise `gradient_accumulation_steps` to keep ~0.5M tok/step, set `max_iters ≈ 40k` (≈20B = Chinchilla-3×). Expect ~3–4× wall-clock per step → multi-day run.
- **Don't** bother re-downloading; the current 140B pool is already sized for everything up to ~1B params.

Want me to draft a `train_fineweb_gpt2_medium.py` config sketch, or extend the current run instead?
