---
audio: false
generated: true
image: false
lang: en
layout: post
title: ClimbMix Fits nanoGPT, Not nanochat
translated: false
type: note
---

Good find — but here's the key insight: **this dataset is GPT-2-tokenized, so it's a match for nanoGPT, not nanochat.** And it's the *same data* nanochat already uses.

## What `nvidia/Nemotron-ClimbMix` actually is

| Property | Value |
| --- | --- |
| Content | 400B-token "ClimbMix" (NVIDIA's high-quality edu-filtered corpus) |
| Tokenization | **GPT-2 tokenizer** (vocab 50257 — same as nanoGPT!) |
| License | **CC-BY-NC-4.0** (non-commercial / research only) |
| Files | `part_*.tokenized.jsonl` (full, ~**2 TB** total) + `climbmix_small/*.tokenized.parquet` (~**40 GB**, 100 shards) |
| Extra | Ships a ready `nanoGPT/config/train_gpt2_climbmix.py` (GPT-2 XL 1.5B) + `detokenize_climbmix.py` |

## Compatibility — this is the deciding factor

**✅ For nanoGPT — perfect fit.** Same GPT-2 vocab (50257), no re-tokenization needed. NVIDIA literally ships a nanoGPT config (`train_gpt2_climbmix.py`) that's identical in shape to your existing `train_fineweb1_5b.py` (L48/H25/C1600 = 1.5B). The tokenized parquet/jsonl just needs converting to nanoGPT's `.bin`/`.npy` loader format.

**❌ For nanochat — wrong tokenizer.** nanochat trains its own 32k-vocab BPE and reads *raw text* parquet. The NVIDIA data is GPT-2-tokenized, so it doesn't fit nanochat's pipeline. You'd have to detokenize (lossy) or re-tokenize.

## The important part: nanochat *already* uses this dataset

nanochat's default `karpathy/climbmix-400b-shuffle` **is the same NVIDIA ClimbMix 400B**, just:

- re-shuffled and repackaged as **raw-text parquet** (what nanochat needs)
- **MIT licensed** (vs NVIDIA's CC-BY-NC)
- stored efficiently (~17 GB for 170 shards, not 2 TB of JSONL)

So for nanochat there's **no reason to switch** — it already uses ClimbMix, in a better format.

## My recommendation

| Goal | Use | Why |
| --- | --- | --- |
| Train **nanochat** on ClimbMix | `karpathy/climbmix-400b-shuffle` (already wired) | raw text, MIT, efficient |
| Train **nanoGPT** on ClimbMix | `nvidia/Nemotron-ClimbMix` (small = 40 GB, or full = 2 TB) | GPT-2 vocab matches, ships a ready config |
| Stay simplest | your existing **FineWeb-Edu 100B** (263 GB local) | already downloaded, no license issues |

**Bottom line:** if you want to run nanochat, just use its built-in ClimbMix (`karpathy/climbmix-400b-shuffle`) — it's literally this NVIDIA dataset in the right format. The `nvidia/Nemotron-ClimbMix` release is only worth downloading if you specifically want to train **nanoGPT** on ClimbMix (GPT-2 tokenizer matches), and even then the `climbmix_small` 40 GB subset is the practical starting point.

Which path do you want — nanochat with its built-in ClimbMix, or nanoGPT with the NVIDIA tokenized data?
