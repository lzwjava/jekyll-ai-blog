---
audio: false
generated: true
image: false
lang: en
layout: post
title: Custom Nanochat Training Setup Guide
translated: false
type: note
---

Here's the full summary:

---

## How to Set Up Nanochat and Train on Custom Data

### 1. Understanding the Difference

nanoGPT uses pre-tokenized `.bin` files (numpy memmap of uint16 token IDs, GPT-2 BPE via tiktoken).

nanochat uses **raw text parquet files** and does its own tokenization on-the-fly with its own BPE tokenizer. You CANNOT reuse `.bin` files from nanoGPT.

### 2. Prepare Your Data

nanochat expects parquet files in `~/.cache/nanochat/base_data_climbmix/` (or wherever `NANOCHAT_BASE_DIR` points). Each parquet file must have a `text` column containing raw text documents. The **last** parquet file is used for validation; all others for training.

Your source data was FineWeb-Edu parquets at `/mnt/data/zz/datasets/fineweb-edu/` (176 files, 374GB, already had a `text` column).

```bash
# Back up existing nanochat data (ClimbMix, 9 shards, 788MB)
mv ~/.cache/nanochat/base_data_climbmix ~/.cache/nanochat/base_data_climbmix.bak

# Symlink your data
ln -s /mnt/data/zz/datasets/fineweb-edu ~/.cache/nanochat/base_data_climbmix
```

### 3. Train the Tokenizer

nanochat uses its own BPE tokenizer (Rust-backed, GPT-4 style). It must be trained on the same data you'll use for pretraining:

```bash
cd /mnt/data/nanochat

# Back up old tokenizer
mv ~/.cache/nanochat/tokenizer ~/.cache/nanochat/tokenizer.bak

# Train new tokenizer (default: 32K vocab, 2B chars, ~42 seconds)
.venv/bin/python -m scripts.tok_train
```

This saves to `~/.cache/nanochat/tokenizer/` (tokenizer.pkl + token_bytes.pt).

### 4. Smoke Test

Quick sanity check (depth=4, 5 steps, ~15 seconds):

```bash
cd /mnt/data/nanochat
.venv/bin/python -m scripts.base_train \
  --depth=4 \
  --max-seq-len=512 \
  --device-batch-size=4 \
  --total-batch-size=2048 \
  --num-iterations=5 \
  --eval-every=-1 \
  --core-metric-every=-1 \
  --sample-every=-1 \
  --save-every=-1 \
  --window-pattern=L \
  --tracker=none
```

Key rule: `--total-batch-size` must be divisible by `device-batch-size * max-seq-len * world_size`. With device-batch-size=4, max-seq-len=512, 1 GPU: minimum total-batch-size = 2048.

### 5. Real Training

```bash
tmux new-session -d -s train 'cd /mnt/data/nanochat && \
.venv/bin/python -m scripts.base_train \
  --depth=12 \
  --max-seq-len=2048 \
  --device-batch-size=8 \
  --total-batch-size=65536 \
  --num-iterations=10000 \
  --eval-every=500 \
  --core-metric-every=-1 \
  --sample-every=2000 \
  --window-pattern=L \
  --tracker=none \
  --run=fineweb-edu-d12 \
  2>&1 | tee /mnt/data/nanochat/train.log'
```

Attach: `tmux attach -t train`

### Key Flags Reference

| Flag | What it does | VRAM impact |
| --- | --- | --- |
| `--depth` | Transformer layers (4=tiny, 12=small, 20=default) | High |
| `--max-seq-len` | Context length (512/1024/2048) | High |
| `--device-batch-size` | Per-GPU batch size | High — first thing to reduce if OOM |
| `--total-batch-size` | Tokens per optimizer step (must be divisible by device_batch*seq_len*GPUs) | None (uses grad accum) |
| `--num-iterations` | Total training steps | — |
| `--eval-every` | Validate every N steps (-1=disable) | — |
| `--sample-every` | Generate samples every N steps (-1=disable) | — |
| `--window-pattern` | `L`=full attention, `SSL`=alternating sliding window (needs FA3) | — |
| `--tracker` | `wandb`/`mlflow`/`none` | — |
| `--fp8` | FP8 training (H100+ only) | Saves VRAM |

### OOM Troubleshooting

If you run out of VRAM, reduce in this order:

1. `--device-batch-size 4` (or 2, or 1)
2. `--max-seq-len 1024` (or 512)
3. `--depth 8` (smaller model)
4. `--window-pattern L` (full attention, already set)

### Our Actual Run Results

- Model: 286M params (depth=12, dim=768, 12 layers, 6 heads)
- Throughput: ~55,700 tok/sec on RTX 4070
- ETA: ~3.3 hours for 10K steps (655M tokens)
- Loss at step 32: 7.25 (still warmup, dropping fast)
- VRAM: ~2.7GB used (plenty of headroom on 12GB)

### Directory Structure

```
~/.cache/nanochat/
├── base_data_climbmix -> /mnt/data/zz/datasets/fineweb-edu   # your data
├── base_data_climbmix.bak/                                     # old ClimbMix backup
├── tokenizer/
│   ├── tokenizer.pkl
│   └── token_bytes.pt
├── tokenizer.bak/                                              # old tokenizer backup
└── base_checkpoints/
    └── d4/                                                     # smoke test checkpoint
        ├── model_000005.pt
        ├── meta_000005.json
        └── optim_000005_rank0.pt
```

### Resuming Training

If interrupted, resume from a checkpoint:

```bash
.venv/bin/python -m scripts.base_train \
  --resume-from-step=5000 \
  --save-every=1000 \
  ... (same flags as before)
```
