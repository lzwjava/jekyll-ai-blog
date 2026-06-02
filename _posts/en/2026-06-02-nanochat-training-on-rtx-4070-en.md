---
audio: false
generated: true
image: false
lang: en
layout: post
title: Nanochat Training on RTX 4070
translated: false
type: note
---

Here's the full rundown of what happened:

## Nanochat Setup Summary on RTX 4070 Workstation

### 1. Clone the repo

SSH'd into `lzw@192.168.1.36`, cloned `https://github.com/karpathy/nanochat` to `/mnt/data/nanochat/` (3.7 MB, pure code — data is downloaded separately at runtime).

### 2. Install uv (Python package manager)

The workstation had Python 3.12.3 but no `uv`. Installed it:

```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Installed to `~/.local/bin/uv`. The project's `pyproject.toml` requires uv for dependency management — it pins `torch==2.9.1+cu128` (CUDA 12.8) via a custom PyTorch index.

### 3. Create venv and install dependencies

```
cd /mnt/data/nanochat
uv venv                    # Created .venv with CPython 3.10.20 (auto-downloaded)
uv sync --extra gpu        # Installed 81 packages including torch 2.9.1+cu128
```

Key packages: `torch`, `triton`, `nvidia-cudnn`, `nvidia-nccl`, `datasets`, `wandb`, `fastapi`, `tiktoken`, `tokenizers`, `rustbpe`. Total download ~3 GB.

### 4. Hit a wandb issue

First run crashed because `--run=rtx4070-d8` triggered wandb init, and no API key was configured. Fix: added `export WANDB_MODE=disabled` to the script. The code has a `DummyWandb()` fallback when run name is "dummy", but `WANDB_MODE=disabled` is cleaner — it lets you use any run name without wandb auth.

### 5. Wrote a custom run script for RTX 4070 (12 GB)

The default `speedrun.sh` targets 8xH100 (80 GB each, 640 GB total). Had to scale everything down for a single 12 GB card:

| Parameter | speedrun.sh (8xH100) | Our run (RTX 4070) | Why |
|-----------|----------------------|--------------------|----|
| `--depth` | 24 | 8 | Smaller model (~40M vs ~1.6B params) |
| `--device-batch-size` | 16 | 4 | Fit in 12 GB VRAM |
| `--total-batch-size` | auto (1M tokens) | 32768 | Reasonable for single GPU |
| `--max-seq-len` | 2048 | 1024 | Save VRAM |
| `--fp8` | yes | no | RTX 4070 is SM 89, no fp8 support |
| `--num-iterations` | auto (compute-optimal) | 5000 | Quick demo run |
| `--core-metric-every` | 2000 | -1 | Skip expensive CORE eval during training |
| GPUs | 8 (torchrun) | 1 (python -m) | Gradient accumulation handles it automatically |

### 6. Runtime data pipeline

nanochat downloads its own data at runtime (not bundled in the repo):

- **Step 1**: `python -m nanochat.dataset -n 8` — downloads 8 shards (~2B chars, ~800 MB) of ClimbMix pretraining data from HuggingFace to `~/.cache/nanochat/base_data_climbmix/`
- **Step 2**: `python -m scripts.tok_train` — trains a BPE tokenizer (vocab 32768) on the downloaded data
- **Step 3**: Pretraining — 5000 steps, ~103K tok/sec, ~26 min
- **Step 4**: Download SFT identity conversations (2.3 MB JSONL from Karpathy's S3)
- **Step 5**: SFT — 1500 steps, teaches the model conversation format
- **Step 6**: Eval + chat

### 7. Current status

Running in tmux session `nanochat`. Pretraining is ~1.6% done (step 81/5000), loss dropping steadily (7.73 → 6.22), VRAM usage only 2.7 GB / 12 GB with GPU at 99% utilization.

### Key takeaway

nanochat is self-contained — the only thing you need is a GPU + uv. It downloads data, trains tokenizer, pretrains, SFTs, and serves a chat UI, all from one script. The `--depth` dial controls everything else automatically (width, heads, LR, training horizon). On a 12 GB card, depth=8 is comfortable; you could push to depth=12-16 with smaller batch sizes.
