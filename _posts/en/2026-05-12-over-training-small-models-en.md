---
audio: false
generated: true
image: false
lang: en
layout: post
title: Over-Training Small Models
translated: false
type: note
---

Question: Given that we have 140 billion tokens instead of 100 billion, what are the implications for training the GPT-2 124M model — should we train longer, and what does this mean for text quality?

Answer:

## The Big Picture: You Are Enormously Data-Rich

The first thing to calculate is where you stand relative to scaling laws.

The Chinchilla research showed that the optimal balance is approximately **20 tokens per parameter** for large-scale transformer models — a model with 70B parameters should train on ~1.4T tokens to be compute-optimal.

For your 124M model:

| Metric | Value |
| --- | --- |
| Chinchilla optimal tokens | 124M × 20 = **~2.5B tokens** |
| Your current `max_iters=19073` plan | 19,073 × 524,288 = **~10B tokens** |
| Your full dataset | **140B tokens** |
| Full dataset / Chinchilla optimal | **~56×** over-trained |
| Full dataset / your planned run | **~14×** more data than you'll use |

Your planned 10B-token run already trains **4× beyond Chinchilla optimal**. The 140B you have on disk is 56× Chinchilla. This is a good thing.

---

## Over-Training Small Models Is the Modern Meta

A Chinchilla optimal model requires 15–25 tokens per parameter to train. Meta's recent Llama 3 70B model was trained with about 200 tokens per parameter — about 10× the Chinchilla point. Microsoft's Phi-3 went even further. The rationale: if you're stuck with a small model at inference time, you want it trained on as much data as possible so it "punches above its weight."

For your 124M model, training on 140B tokens (1,129 tokens/param) would produce a dramatically smarter model than the Chinchilla-optimal 2.5B — it just takes wall-clock time you may not have.

---

## What's Realistically Trainable on Your RTX 4070

At ~11 sec/iter with `compile=True`, here's the full picture:

| `max_iters` | Tokens seen | Wall time | % of 140B data used |
| --- | --- | --- | --- |
| 5,000 | 2.6B | ~15 hrs | 1.9% |
| 19,073 | 10B | ~40–50 hrs | 7.1% |
| 50,000 | 26B | ~6 days | 18.6% |
| 100,000 | 52B | ~12.7 days | 37% |
| 267,029 | **140B (full)** | **~34 days** | 100% |

A full single-epoch run over your 140B would take ~34 days uninterrupted — possible but risky on a single consumer GPU (thermal throttle, power cut, etc.). The **sweet spot for quality vs time** on an RTX 4070 is probably **50,000–100,000 iters (~6–13 days)**, which gets you 26–52B tokens seen — well into "over-trained small model" territory.

---

## Config Changes to Train Longer

```python
# Aggressive quality run — ~13 days, 52B tokens seen
max_iters = 100_000
lr_decay_iters = 100_000
warmup_iters = 2000          # scale warmup proportionally

# Everything else unchanged
batch_size = 4
block_size = 1024
gradient_accumulation_steps = 128
compile = True
always_save_checkpoint = True   # CRITICAL — checkpoint every 500 iters
```

**Critical point:** with `always_save_checkpoint = True` and `eval_interval = 500`, you save every 500 iters. That means you can kill and `--init_from=resume` at any time with no loss. The 34-day full run is survivable in segments.

---

## About Your `shard_dir` Name Mismatch

Your data lives in `edu_fineweb100B` but holds 140B tokens. This is purely cosmetic — nanoGPT doesn't care about the directory name, only what's inside. No action needed. Just be aware:

- Do **not** re-run the tokenizer — it would clobber `val_000000.npy` (your fixed validation shard)
- The partial last shard (36.3M tokens, shard 1407) is loaded fine by nanoGPT's sampler

---

## Recommendation

1. **Start your planned 19,073-iter run now** — good baseline, ~40–50 hrs, resumes cleanly
2. **After it completes, immediately resume** with `max_iters=100_000` — no data wasted, just continues the cosine schedule from where it left off (update `lr_decay_iters` accordingly before resuming)
3. The 140B tokens is a genuine asset — use as much of it as your time budget allows

References:

- [Chinchilla Scaling Laws — 20 tokens per parameter](https://mbrenndoerfer.com/writing/chinchilla-scaling-laws-compute-optimal-training-resource-allocation)
- [Revised Chinchilla laws — over-training small models (Llama 3, Phi-3 strategy)](https://www.educatingsilicon.com/2024/04/29/revised-chinchilla-scaling-laws-impact-on-llm-compute-and-token-requirements/)
- [Original Chinchilla paper (Hoffmann et al. 2022)](https://arxiv.org/pdf/2203.15556)
