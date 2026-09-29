---
audio: false
generated: true
image: false
lang: en
layout: post
title: nanochat d18 Fits 12GB Card Best
translated: false
type: note
---

nanochat is a much better fit for "biggest model on this 12 GB card" — and it's already installed and working here (torch 2.9.1, flash-attn 2.8.3, rustbpe all OK, internet to HuggingFace works, disk available).

## Why nanochat is more memory-efficient

It uses a fundamentally different stack than nanoGPT:

- **fp32 master weights + bf16 compute** (better precision than nanoGPT's pure-bf16 option)
- **Muon optimizer** (1 momentum buffer instead of AdamW's 2) — halves optimizer memory
- **Flash Attention 3** — never materializes the O(T²) attention matrix
- **Sliding-window attention** (SSSL) — ¾ of layers use half-context windows

## What I measured (empirically, on your 4070)

| nanochat depth | params | VRAM (bs=1, seq 1024) | verdict |
| --- | --- | --- | --- |
| d12 | 286M | 3.4 GB | ✅ |
| d16 | 537M | 6.7 GB | ✅ |
| **d18** | **702M** | **8.9 GB** | ✅ **fits** |
| d20 | 897M | — | ❌ OOM (optimizer states) |
| d24 | 1.38B | — | ❌ OOM |

## The comparison you asked about

| Approach | Max params on 12 GB | Quality note |
| --- | --- | --- |
| nanoGPT fp32 | ~350–400M | safe |
| nanoGPT bf16 (needs code change) | ~760M | pure bf16, precision risk |
| **nanochat** | **~700M (d18)** | fp32 master + Muon + FA — best |

**So nanochat's d18 (~702M) is essentially your 760M target** — slightly fewer params but trained with fp32 master weights and a faster-converging optimizer, so it will likely beat a 760M nanoGPT model in quality.

## Caveats (not blockers)

1. **Data:** nanochat has no local dataset — it downloads **ClimbMix-400B** parquet shards from HuggingFace on demand (~8 shards/800 MB for the tokenizer, ~170 shards/17 GB for a full GPT-2-grade run). Internet ✅ and disk ✅ (590 GB free).
2. **Tokenizer:** it trains its own 32k-vocab BPE first (`scripts/tok_train`).
3. **`torch.compile`** (on by default in `base_train`) adds memory — d18 might get tight with it on. **d16 (537M) is the safe pick with compile**, d18 if you want to push.

## My recommendation

Use **nanochat d18** for the biggest model this card can do (~700M, fp32-master quality). Steps would be:

```
python -m nanochat.dataset -n 8          # download ~800MB for tokenizer
python -m nanochat.dataset -n 170 &      # download the rest in background
python -m scripts.tok_train              # train tokenizer
python -m scripts.base_train --depth=18 --max-seq-len=1024 --device-batch-size=1 ...
```

Want me to kick off the data download + tokenizer training, then a smoke run of `d18`? Or start with the safer `d16`?
