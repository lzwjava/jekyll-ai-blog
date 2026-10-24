---
audio: false
generated: true
image: false
lang: en
layout: post
title: "nanochat: nanoGPT's Spiritual Successor"
translated: false
type: note
---

nanochat isn't a fork of nanoGPT — it's its **successor/spiritual evolution** (same lineage, Karpathy's "nano" series, rewritten from scratch as a proper package). nanoGPT was the minimal proof-of-concept ("the simplest, fastest repository for training/finetuning medium-sized GPTs", ~300 lines in one `train.py`); nanochat is the full industrial pipeline built around the same core GPT idea.

## Scope ("full-stack" vs pretrain-only)

**nanoGPT** — one job:
- `train.py` (pretrain on OpenWebText, DDP, autocast, AdamW), `model.py` (GPT-2 block, learned positional embeddings), `sample.py`, data-prep scripts
- Single stage: pretraining → sample text. That's it.

**nanochat** (~7000 lines) covers every LLM stage:
- Tokenization: trains its **own BPE tokenizer** in GPT-4 style (`tokenizer.py`, `scripts/tok_train.py`) vs nanoGPT's tiktoken dependency
- Pretraining (`base_train.py`), **SFT** (`chat_sft.py`), **RL** (`chat_rl.py`), **eval** (CORE score, bits-per-byte, MMLU/GSM8K/ARC/humaneval tasks), and a **chat CLI** (`chat_cli.py`)
- An inference **engine with KV cache** (`engine.py`) and sandboxed **Python code execution** as a tool (`execution.py`)

## "One dial" design — the big philosophical difference

nanoGPT: you set `n_layer`, `n_head`, `n_embd`, `learning_rate`, etc. manually.
nanochat: you set a single `--depth` integer; everything else (width, heads, LR, weight decay, training horizon) is **derived automatically from scaling laws** so every size comes out compute-optimal. `--depth=26` ≈ GPT-2 capability. This is why the repo's goal is the "time-to-GPT-2" leaderboard — beat GPT-2's CORE score in ~1.65 hrs on 8×H100 for <$50 (vs $43K in 2019).

## Model architecture & training differences (`gpt.py`, `optim.py`)

| | nanoGPT | nanochat |
|---|---|---|
| Positional encodings | learned | **rotary embeddings** |
| Attention | full causal | causal with **per-layer sliding window** (tiled) |
| QK scaling | 1/√d | split scale, `q *= 1.2` |
| Optimizer | AdamW | **MuonAdamW** (Muon on matrix params grouped by shape + AdamW on the rest), with a distributed variant that gathers gradients for Muon's orthogonalization |
| Mixed precision | `torch.amp.autocast` | **explicit `COMPUTE_DTYPE`** global (bf16/fp16/fp32, env-overridable) — no autocast anywhere |
| FP8 | — | **yes** — `fp8.py`, exactly what we discussed: custom `_Float8Matmul` autograd around `torch._scaled_mm`, e4m3 for activations/weights, e5m2 for grads |
| Attention impl | SDPA | flash_attention.py wrapper (FA3 when available, SDPA fallback) |
| Logging | print + plot.py | mlflow + wandb + checkpoint manager |

## Operational differences

- **Data**: nanoGPT downloads OpenWebText and pre-tokenizes once; nanochat has a distributed shard-based tokenized dataloader (`dataloader.py`, `dataset.py`) — data format matters for the CORE leaderboard
- **Parallelism**: both use DDP; nanochat adds gradient accumulation auto-handling (runs on 1 GPU too), async gradient reduction in `DistMuonAdamW`, `allow_in_graph`-ready compiled training
- **Deliverable**: nanoGPT gives you a raw sampler; nanochat gives a chat assistant you can actually talk to (with tool use)

## Practical summary

If nanoGPT is the "here's everything in one file, read it all" educational artifact, nanochat is "the same spirit, productionized": same GPT core, but with a scaling-law-tuned hyperparameter system, Muon optimizer, FP8, explicit precision control, sliding-window + RoPE attention, SFT/RL stages, a leaderboard-optimized speedrun, and proper package structure with tests. The `fp8.py` we looked at is a good example of the nanochat philosophy: take a 2000-line torchao subsystem and shrink it to 150 lines targeted at exactly what the repo needs.
