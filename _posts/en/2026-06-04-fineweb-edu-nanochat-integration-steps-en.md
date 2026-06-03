---
audio: false
generated: true
image: false
lang: en
layout: post
title: FineWeb-Edu nanochat integration steps
translated: false
type: note
---

OK, now I have the full picture. Here's what you need to do:

Your FineWeb-Edu parquet files at `/mnt/data/zz/datasets/fineweb-edu/` (176 files, 374GB) already have a `text` column — that's exactly what nanochat needs. But nanochat can't use nanoGPT's .bin files because nanochat does its own tokenization with its own BPE tokenizer.

**Step-by-step:**

**1. Link your data into nanochat's expected location**

The existing `~/.cache/nanochat/base_data_climbmix/` has only 9 shards (788MB). Replace it with your data:

```bash
# Back up existing data
mv ~/.cache/nanochat/base_data_climbmix ~/.cache/nanochat/base_data_climbmix.bak

# Symlink your FineWeb-Edu parquets
ln -s /mnt/data/zz/datasets/fineweb-edu ~/.cache/nanochat/base_data_climbmix
```

**2. Retrain the tokenizer on your data**

The existing tokenizer was trained on ClimbMix. You need one trained on FineWeb-Edu:

```bash
cd /mnt/data/nanochat
.venv/bin/python -m scripts.tok_train
```

This reads parquet files, trains a BPE tokenizer (vocab 32K by default), and saves to `~/.cache/nanochat/tokenizer/`.

**3. Train the model**

Single GPU (your RTX 4070, 12GB VRAM):

```bash
cd /mnt/data/nanochat
.venv/bin/python -m scripts.base_train \
  --depth=4 \
  --max-seq-len=512 \
  --device-batch-size=4 \
  --total-batch-size=512 \
  --num-iterations=500 \
  --eval-every=100 \
  --eval-tokens=512 \
  --core-metric-every=-1 \
  --sample-every=200 \
  --window-pattern=L
```

Key flags to adjust based on your VRAM:
- `--depth` — model depth (4 = tiny/debug, 12 = small, 20 = default)
- `--device-batch-size` — reduce to 1-2 if OOM
- `--max-seq-len` — context length (512 conserves VRAM)
- `--total-batch-size` — total tokens per step
- `--window-pattern=L` — use full attention (SDPA fallback doesn't support sliding window)
- `--num-iterations` — how many steps to train

**Important notes:**
- nanochat uses its OWN tokenizer (BPE, 32K vocab) — completely different from GPT-2's tokenizer in tiktoken
- The `.bin` files from nanoGPT are pre-tokenized with GPT-2 tokenizer and can't be reused
- Your raw text parquets ARE the right input for nanochat
- 374GB is a lot — you can use a subset by only symlinking some parquet files if training takes too long
