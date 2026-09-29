---
audio: false
generated: true
image: false
lang: en
layout: post
title: "760M OOM: Correction and Options"
translated: false
type: note
---

The smoke run OOM'd — and that actually revealed the real answer to your question. Let me explain what I got wrong and what's actually true.

## Correction: 760M does **NOT** fit on this card (in nanoGPT's default fp32)

My earlier probe was misleading — I had manually cast the model to bf16. But this repo's `train.py` keeps weights in **fp32** (I confirmed: existing checkpoints store `torch.float32` weights). With fp32, the real memory is:

| 760M component | Size |
| --- | --- |
| Weights (fp32) | 3.06 GB |
| Gradients (fp32) | 3.06 GB |
| AdamW states m+v (fp32) | 6.06 GB |
| **Static total** | **12.2 GB** |

The card has **only ~11.4 GB usable** (12 GB minus desktop). So even at batch size 1, just allocating the optimizer states OOMs — which is exactly what happened (`Tried to allocate 20 MiB` during Adam state init, GPU full).

## The real ceiling on this RTX 4070 (12 GB)

| Model | Params | Status (fp32) |
| --- | --- | --- |
| ~219M (existing gpt2-200m) | 219M | ✅ fits @ bs=4 (~8 GB) |
| ~350M (E=1024, L=24) | ~353M | ✅ fits @ bs=2 (~8.8 GB) |
| ~400M (E=1024, L=28) | ~403M | ✅ fits @ bs=2 (~10 GB) |
| ~500M (E=1280, L=24) | ~536M | ⚠️ bs=1 only, very tight |
| **760M** | 758M | ❌ **doesn't fit** (~12.2 GB static) |
| 1.5B (GPT-2 XL) | 1.5B | ❌ way over |

**So the largest you can train in standard fp32 nanoGPT is ~350–400M.** 760M is not reachable without a code change.

## The one way to make 760M fit: cast weights to bf16

If I add bf16 weights (a common nanoGPT mod), 760M becomes:

- static = 4.7 GB (bf16 weights + bf16 AdamW states) + ~2.3 GB activations @ bs=2 ≈ **7 GB** → fits with room.

The caveat: bf16 optimizer states are slightly less precise than fp32 master weights — usually fine for pretraining, occasionally a touch worse final loss.

## What I've already done

- ✅ Fixed the broken `shard_dir` path in `train_fineweb_760m.py`
- ✅ Created `config/train_fineweb_760m_smoke.py` (but it OOM'd at bs=2, as expected for fp32)

## Your call — which do you want?

1. **760M via bf16** — I add a `--bf16` / `model.to(torch.bfloat16)` option to `train.py`, then run the smoke test. Biggest model this card can do.
2. **~350M in fp32** — no code changes, safest quality, still ~1.6× bigger than your current 219M run.
3. **Stay at 219M** and just resume the interrupted `out-gpt2-200m` run.

I'd recommend **option 1** if your goal is max size, or **option 2** if you want the safest big model. Which one?
