---
audio: false
generated: true
image: false
lang: en
layout: post
title: d18 Training State and Commands
translated: false
type: note
---

Done — download killed. Here's your state and the commands to run in your terminal.

## Current state

- ✅ **Tokenizer** trained (32k vocab) at `/mnt/data/nanochat-cache/tokenizer/`
- 📦 **77/170 train shards + val** downloaded (~6.9 GB) at `/mnt/data/nanochat-cache/base_data_climbmix/`
- ✅ **d18 (702M) verified** to fit: `bs=2, seq=1024` → 9.0 GB peak, ~8,100 tok/s, 57% MFU

## Commands for your terminal

**1. (Optional) Finish the download** — resumes from 77, skips existing:

```bash
cd /mnt/data/nanochat && export NANOCHAT_BASE_DIR=/mnt/data/nanochat-cache
./.venv/bin/python -m nanochat.dataset -n 170 -w 2
```

**2. Train d18 (702M) — the verified max config:**

```bash
cd /mnt/data/nanochat && export NANOCHAT_BASE_DIR=/mnt/data/nanochat-cache
./.venv/bin/python -m scripts.base_train \
  --depth=18 --max-seq-len=1024 --device-batch-size=2 \
  --tracker=none --run=d18-climbmix
```

**For a long background run** (recommended — 3.9B tokens ≈ 5.6 days):

```bash
cd /mnt/data/nanochat && export NANOCHAT_BASE_DIR=/mnt/data/nanochat-cache
nohup ./.venv/bin/python -m scripts.base_train \
  --depth=18 --max-seq-len=1024 --device-batch-size=2 \
  --tracker=none --run=d18-climbmix \
  --save-every=500 \
  > /mnt/data/nanochat-cache/train-d18.log 2>&1 &
```

## Important notes

- **`--save-every=500`** enables periodic checkpoints (default is only save at end — bad for a 5.6-day run).
- **Resume** later with `--resume-from-step=<step>` (checkpoints go to `/mnt/data/nanochat-cache/base_checkpoints/d18/`).
- **Don't** use `bs=4` (OOM) or `--max-seq-len=2048` at bs=2 (likely OOM).
- Default budget = ratio 12 → **~3.9B tokens**. For a shorter run add `--num-iterations=<N>` (e.g. 1000 ≈ 1B tokens), or `--target-param-data-ratio=4` for ~half.
- `--tracker=none` skips wandb/mlflow (there's a stale `mlflow.db` in the repo if you ever want mlflow).

Monitor progress with:

```bash
tail -f /mnt/data/nanochat-cache/train-d18.log
```
