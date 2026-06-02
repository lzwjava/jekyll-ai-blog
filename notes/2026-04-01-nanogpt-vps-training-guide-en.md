---
audio: false
generated: true
image: false
lang: en
layout: post
title: NanoGPT VPS Setup and Training Guide
translated: false
type: note
---

Here's the full picture:

---

## 📊 VPS Setup Summary (ubuntu-s-1vcpu-512mb-10gb-nyc2-01)

### ✅ What's Ready

| Component | Status | Details |
|-----------|--------|---------|
| **nanoGPT code** | ✅ Ready | `/root/nanoGPT/` — train.py, model.py, sample.py |
| **Data (sample)** | ✅ Ready | `train.bin` (14M tokens), `val.bin` (100M tokens) in `/root/nanoGPT/data/fineweb/` |
| **Test config** | ✅ Ready | `config/train_fineweb_test.py` — tiny 7M model, CPU-friendly |
| **Python venv** | ✅ Ready | `/root/nanoGPT/venv/` with torch CPU + tiktoken + tqdm |
| **Train.py fix** | ✅ Done | `device = 'cpu'` hardcoded (no GPU on VPS) |
| **Test run** | ✅ Passed | 100 iters, loss 10.84 → 8.71 in ~2 min |

### ⚠️ Data Limitation

The data preparation was **killed mid-process**. Current state:
- **Val**: 100M tokens (1 shard) — full shard 0
- **Train**: 14M tokens (partial shard 1) — **only ~14% of 1 shard**
- **Full dataset**: Would be ~610 shards × 100M = **~61B tokens** (61GB raw text)

### 🧠 Full Training Config (`config/train_fineweb.py`)

```python
# Model: ~125M params (GPT-2 class, fits in 12GB VRAM)
n_layer = 12, n_head = 12, n_embd = 768
block_size = 1024, batch_size = 8 (micro)

# Effective batch size = 8 × 64 grad_accum = 512 sequences/iter
# ~500k tokens/iter → 12k iters = ~6B tokens

compile = True     # 20-30% faster
bias = False       # LLaMA-style
weight_decay = 0.1
max_iters = 12000
```

### 💾 GPU VRAM Estimates for Full Model

| Precision | Model Params | VRAM |
|-----------|-------------|------|
| `float32` | 125M | ~500MB |
| `float16` | 125M | ~250MB |
| `bfloat16` | 125M | ~250MB |
| + AdamW + gradients + activations | — | **~8-10GB** |

A **single A100 40GB** or **RTX 4090 24GB** is more than enough.

---

## 🚀 How to Transfer to GPU Droplet & Train

### Step 1 — Copy everything from VPS to your machine/laptop:
```bash
# Copy the prepared data (only ~220MB for the sample)
scp -r root@159.89.216.20:/root/nanoGPT/data/fineweb ./data/

# Copy nanoGPT code
scp -r root@159.89.216.20:/root/nanoGPT/* ./

# Copy the venv's site-packages (optional, or pip install on GPU side)
# Actually better to: pip install torch numpy tiktoken tqdm transformers
```

### Step 2 — On GPU droplet:
```bash
# Install deps
pip install torch numpy tiktoken tqdm transformers wandb

# Fix device if needed (should auto-detect CUDA)
# Check train.py line 72: device = 'cpu' → device = 'cuda'

# Run training with the real config
python train.py config/train_fineweb.py
```

### Step 3 — Monitor:
```bash
# Watch loss
python sample.py --out_dir=out-fineweb

# Or with wandb (enable in config)
wandb login
# then set wandb_log = True in config
```

---

## 🔧 What You'd Need for Full 61GB Dataset

If you want to prepare the **full 61GB** on VPS for the GPU droplet:

```bash
# On VPS — full prepare (will take ~8-10 hours on VPS CPU)
cd /root/nanoGPT/data/fineweb
rm -f train_fineweb.txt
ln -s /root/zz/datasets/fineweb_extracted_all.txt train_fineweb.txt
source /root/nanoGPT/venv/bin/activate
python prepare_fineweb.py
```

But **much faster** — prepare directly on the GPU droplet:
```bash
# On GPU droplet — just link the raw file and run prepare.py there
ln -sf /path/to/fineweb_extracted_all.txt ./data/fineweb/train_fineweb.txt
python data/fineweb/prepare_fineweb.py
```

This way the GPU droplet's faster CPU+disk can handle the tokenization.

---

## 📁 Final Directory Structure on GPU Droplet

```
nanoGPT/
├── train.py          # Training script
├── model.py           # GPT model definition
├── sample.py          # Sampling script
├── config/
│   ├── train_fineweb.py      # Full 125M model config ← USE THIS
│   └── train_fineweb_test.py # Tiny test config
├── data/fineweb/
│   ├── train.bin     # ~14M tokens (sample) or ~30GB (full)
│   ├── val.bin       # ~100M tokens
│   └── meta.pkl      # (optional) tokenizer info
└── out-fineweb/      # Checkpoints written here
```

**Bottom line**: The pipeline works. For the GPU droplet, just copy `/root/nanoGPT/` + the data, fix `device = 'cuda'` in train.py if needed, and run with `train_fineweb.py` config. Want me to prepare the full 61GB data on the VPS, or would you prefer to do that on the GPU droplet directly?
