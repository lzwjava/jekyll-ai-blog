---
audio: false
generated: true
image: false
lang: en
layout: post
title: Training GPT-2 on SEC Filings
translated: false
type: note
---

Here's the full picture:

== DATASET ==
SEC-EDGAR — all 10-K annual reports from the SEC's EDGAR filing system.
- 17 parquet shards → tokenized with GPT-2 tokenizer (tiktoken, vocab 50257)
- 16 train shards: 1,555,060,445 tokens (1.55B)
- 1 val shard: 100,000,000 tokens
- dtype: uint16, stored as .npy files on /mnt/data/zz/datasets/sec-edgar-tok/

== MODEL ==
GPT-2 124M (standard nanoGPT architecture)
- 12 layers, 12 heads, 768 embedding dim
- 123.59M parameters
- No bias (LLaMA-style)
- Vocab: 50304 (50257 rounded for efficiency)

== TRAINING ==
- Effective batch: 32,768 tokens/step (4 batch × 1024 block × 8 grad_accum)
- 47,400 steps = ~1.55B tokens seen = 1 full epoch
- GPT-3 style optimizer: lr=6e-4, warmup 2000 steps, cosine decay to 6e-5
- Mixed precision (float16), fused AdamW
- No compile (python 3.11 inductor bug)

== TIME ==
- ~700ms/step (no compile)
- 47,400 × 0.7s ≈ 33,180s ≈ 9.2 hours
- Will finish roughly tonight / early morning

== WHAT TO EXPECT ==
- Loss started at ~10.98 (random init), already at 8.85 by step 20
- Should converge to val_loss ~3.0-3.5 range for financial text
  (for reference: github-code hit 3.466 but that dataset was noisy;
   SEC-EDGAR is cleaner, structured financial prose)
- The model will learn SEC filing language: financial tables, risk
  disclosures, MD&A sections, accounting terminology
- After training you get: out-sec-edgar-124m/ckpt.pt (latest checkpoint)

== USEFULNESS ==
This is a domain-specific LM for financial/SEC filings. Good for:
- Generating realistic 10-K style text
- Fine-tuning base for financial NLP tasks
- Continuing pretraining on related corpora

Limitations: 124M is small — don't expect GPT-4 level coherence.
It'll produce plausible SEC-sounding text but will struggle with
complex reasoning or long-range consistency.
