---
audio: false
generated: true
image: false
lang: en
layout: post
title: Proper Benchmarking for Undertrained Models
translated: false
type: note
---

Based on your training run: val loss **3.29**, 6.3B tokens, 12k iters — model is undertrained but healthy. Here's the right evaluation path:

## Why not SimpleQA

SimpleQA tests factual recall and is designed for frontier models (GPT-4 scale). Your 124M undertrained model will score near 0% — not informative.

## Right benchmarks for GPT-2 124M scale

Use **EleutherAI's `lm-evaluation-harness`** — the standard tool for this model class:

```bash
pip install lm-eval
```

Then run zero-shot evals on standard tasks:

```bash
cd ~/projects/nanoGPT
lm_eval --model hf \
  --model_args pretrained=gpt2 \
  --tasks lambada_openai,hellaswag,piqa,winogrande,arc_easy \
  --device cuda \
  --batch_size 8
```

But your model uses nanoGPT format (not HuggingFace), so you'd first need to either:

**Option A — Convert to HF format** (one-time script to map nanoGPT weights → `GPT2LMHeadModel`)

**Option B — Write a custom lm-eval model wrapper** (a Python class that loads `ckpt.pt` and exposes the logits API lm-eval expects)

**Option C — Just measure perplexity on a held-out set** (simplest — your val loss 3.29 → perplexity ≈ **26.8**)

## Reference numbers for GPT-2 124M

| Task | GPT-2 124M (full training) |
|------|---------------------------|
| LAMBADA | ~45% |
| HellaSwag | ~31% |
| PIQA | ~70% |
| WinoGrande | ~51% |

Your model at 1/50th compute will score lower — that's the expected comparison point.

**Recommendation:** Option A (convert to HF) is the cleanest path. Want me to write the weight-conversion script?
