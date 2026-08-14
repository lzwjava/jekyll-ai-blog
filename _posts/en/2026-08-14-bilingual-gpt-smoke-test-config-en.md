---
audio: false
generated: true
image: false
lang: en
layout: post
title: Bilingual GPT Smoke Test Config
translated: false
type: note
---

Done. Here's what I set up:

**`data/meta.pkl`** (in `/mnt/data/bilingual-gpt/data/`) — `train.py` reads `vocab_size` from this; set to `65536` so the model's embed/LM-head match your tokenizer.

**`/mnt/data/nanoGPT/config/train_bilingual_smoke.py`** — a smoke config:

- `dataset = '/mnt/data/bilingual-gpt/data'` (absolute path → `train.py` finds `train.bin`/`val.bin`/`meta.pkl` there; uint16 ids)
- Tiny model (6 layer / 6 head / 384 embd) sized for your 4070's ~4 GiB free VRAM — vocab 65536 is what dominates params here
- `block_size=256`, `batch_size=8`, `grad_accum=4`, `max_iters=50`, no compile, no wandb — quick end-to-end check that loss decreases and a checkpoint saves

Run it from the nanoGPT dir:

```bash
cd /mnt/data/nanoGPT
python train.py config/train_bilingual_smoke.py
```

Notes:

- VRAM is tight (~4 GiB free). If you OOM, drop `batch_size` to 4 or `block_size` to 128 and rerun.
- This is a smoke run only — for real training, scale up `n_layer/n_embd/block_size` and `max_iters`, and re-enable `compile = True` (set `always_save_checkpoint = True` once you're past the first eval).
