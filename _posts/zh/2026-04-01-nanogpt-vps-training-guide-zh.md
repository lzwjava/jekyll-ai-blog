---
audio: false
generated: true
image: false
lang: zh
layout: post
title: NanoGPT VPS 设置与训练指南
translated: true
type: note
---

完整情况如下：

---

## 📊 VPS Setup Summary (ubuntu-s-1vcpu-512mb-10gb-nyc2-01)

### ✅ 已准备就绪

<br/>

| Component | Status | Details |
|-----------|--------|---------|
| **nanoGPT code** | ✅ Ready | `/root/nanoGPT/` — train.py, model.py, sample.py |
| **Data (sample)** | ✅ Ready | `train.bin` (14M tokens), `val.bin` (100M tokens) in `/root/nanoGPT/data/fineweb/` |
| **Test config** | ✅ Ready | `config/train_fineweb_test.py` — tiny 7M model, CPU-friendly |
| **Python venv** | ✅ Ready | `/root/nanoGPT/venv/` with torch CPU + tiktoken + tqdm |
| **Train.py fix** | ✅ Done | `device = 'cpu'` hardcoded (no GPU on VPS) |
| **Test run** | ✅ Passed | 100 iters, loss 10.84 → 8.71 in ~2 min |

### ⚠️ 数据限制

数据准备过程**中途被终止**。当前状态：
- **Val**：100M tokens (1 shard) — full shard 0
- **Train**：14M tokens (partial shard 1) — **仅约 1 个 shard 的 14%**
- **完整数据集**：约 610 shards × 100M = **~61B tokens** (61GB raw text)

### 🧠 完整训练配置 (`config/train_fineweb.py`)

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

### 💾 完整模型的 GPU VRAM 估算

<br/>

| Precision | Model Params | VRAM |
|-----------|-------------|------|
| `float32` | 125M | ~500MB |
| `float16` | 125M | ~250MB |
| `bfloat16` | 125M | ~250MB |
| + AdamW + gradients + activations | — | **~8-10GB** |

**单个 A100 40GB** 或 **RTX 4090 24GB** 完全足够。

---

## 🚀 如何传输到 GPU Droplet 并训练

### Step 1 — 从 VPS 复制所有内容到您的机器/笔记本：

```bash
# Copy the prepared data (only ~220MB for the sample)
scp -r root@159.89.216.20:/root/nanoGPT/data/fineweb ./data/

# Copy nanoGPT code
scp -r root@159.89.216.20:/root/nanoGPT/* ./

# Copy the venv's site-packages (optional, or pip install on GPU side)
# Actually better to: pip install torch numpy tiktoken tqdm transformers
```

### Step 2 — 在 GPU droplet 上：

```bash
# Install deps
pip install torch numpy tiktoken tqdm transformers wandb

# Fix device if needed (should auto-detect CUDA)
# Check train.py line 72: device = 'cpu' → device = 'cuda'

# Run training with the real config
python train.py config/train_fineweb.py
```

### Step 3 — 监控：

```bash
# Watch loss
python sample.py --out_dir=out-fineweb

# Or with wandb (enable in config)
wandb login
# then set wandb_log = True in config
```

---

## 🔧 完整 61GB 数据集所需内容

如果您想在 VPS 上准备**完整 61GB** 数据以供 GPU droplet 使用：

```bash
# On VPS — full prepare (will take ~8-10 hours on VPS CPU)
cd /root/nanoGPT/data/fineweb
rm -f train_fineweb.txt
ln -s /root/zz/datasets/fineweb_extracted_all.txt train_fineweb.txt
source /root/nanoGPT/venv/bin/activate
python prepare_fineweb.py
```

但**更快** — 直接在 GPU droplet 上准备：
```bash
# On GPU droplet — just link the raw file and run prepare.py there
ln -sf /path/to/fineweb_extracted_all.txt ./data/fineweb/train_fineweb.txt
python data/fineweb/prepare_fineweb.py
```

这样 GPU droplet 的更快 CPU+磁盘可以处理分词。

---

## 📁 GPU Droplet 上的最终目录结构

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

**底线**：管道运行正常。对于 GPU droplet，只需复制 `/root/nanoGPT/` + 数据，在 train.py 中修复 `device = 'cuda'`（如果需要），然后使用 `train_fineweb.py` 配置运行。您希望我在 VPS 上准备完整的 61GB 数据，还是更倾向于直接在 GPU droplet 上进行？
