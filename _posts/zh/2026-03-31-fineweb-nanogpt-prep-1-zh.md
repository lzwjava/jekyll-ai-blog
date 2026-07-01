---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 为 nanoGPT 训练准备 FineWeb 数据集
translated: true
type: note
---

问题：如何在 DigitalOcean 服务器上（无需代理）使用 Hugging Face 库下载大型 FineWeb 数据集，并将其准备好用于训练 nanoGPT 以达到 GPT-2 124M 水平？

回答：

## 在 DigitalOcean 上使用 Hugging Face 下载 FineWeb

由于你使用的是 DigitalOcean（海外服务器），你可以直接使用 **HuggingFace** —— 无需镜像。

---

## 🖥️ 推荐的 DigitalOcean Droplet 配置

仅用于数据准备（不进行训练）：

- **4 vCPU, 8GB RAM, 100GB+ 磁盘** (CPU-optimized droplet)
- 训练过程仍建议在本地的 RTX 4070 上进行

---

## Step 1: 安装依赖

```bash
pip install huggingface_hub datasets tiktoken numpy tqdm
```

---

## Step 2: 通过 `huggingface_hub` 下载 FineWeb

FineWeb 托管在 `HuggingFaceFW/fineweb`。使用 streaming 或 snapshot 方式：

### 选项 A — 流式处理并写入 (内存安全，推荐 2GB RAM 使用)

```python
# download_fineweb.py
from datasets import load_dataset
import os

output_file = "fineweb_extracted_all.txt"
total_docs = 0

# "sample-10BT" = 10 billion token 样本 — 适合 GPT-2 124M 训练
dataset = load_dataset(
    "HuggingFaceFW/fineweb",
    name="sample-10BT",
    split="train",
    streaming=True   # <-- 关键：防止内存爆炸
)

with open(output_file, "w", encoding="utf-8") as f:
    for doc in dataset:
        f.write(doc["text"].strip())
        f.write("\n<|endoftext|>\n")
        total_docs += 1
        if total_docs % 10000 == 0:
            print(f"Processed {total_docs} docs...")

print(f"Done. Total docs: {total_docs}")
```

运行脚本：

```bash
python download_fineweb.py
```

> ✅ `sample-10BT` = 约 10B tokens，足以匹配 GPT-2 的训练规模
> ✅ Streaming 意味着你永远不会将整个数据集加载到 RAM 中

---

### 选项 B — 直接下载 Parquet 分片 (速度更快，需要更多磁盘空间)

```python
from huggingface_hub import snapshot_download

snapshot_download(
    repo_id="HuggingFaceFW/fineweb",
    repo_type="dataset",
    allow_patterns=["data/CC-MAIN-2024-10/*.parquet"],  # 单个 crawl 约几十 GB
    local_dir="./fineweb_parquet"
)
```

然后使用你现有的 `extract_fineweb.py` 进行提取。

---

## Step 3: Tokenize → `train.bin` / `val.bin`

```python
# prepare.py
import numpy as np
import tiktoken
from tqdm import tqdm

enc = tiktoken.get_encoding("gpt2")
EOT = enc._special_tokens["<|endoftext|>"]

input_file = "fineweb_extracted_all.txt"
train_file = "train.bin"
val_file   = "val.bin"

all_tokens = []

with open(input_file, "r", encoding="utf-8") as f:
    for line in tqdm(f):
        line = line.strip()
        if line == "<|endoftext|>":
            all_tokens.append(EOT)
        elif line:
            tokens = enc.encode_ordinary(line)
            all_tokens.extend(tokens)

print(f"Total tokens: {len(all_tokens):,}")

# 90/10 分割
split = int(len(all_tokens) * 0.9)
train_ids = np.array(all_tokens[:split], dtype=np.uint16)
val_ids   = np.array(all_tokens[split:], dtype=np.uint16)

train_ids.tofile(train_file)
val_ids.tofile(val_file)
print(f"train.bin: {len(train_ids):,} tokens")
print(f"val.bin:   {len(val_ids):,} tokens")
```

---

## Step 4: 传输至你的 GPU 机器

```bash
# 在你本地的 RTX 4070 机器上运行：
rsync -avz --progress user@your-droplet-ip:~/fineweb/train.bin ~/nanoGPT/data/fineweb/
rsync -avz --progress user@your-droplet-ip:~/fineweb/val.bin  ~/nanoGPT/data/fineweb/
```

---

## Step 5: 训练 nanoGPT (GPT-2 124M 配置)

```python
# config/train_fineweb.py
out_dir = 'out-fineweb'
dataset = 'fineweb'

# GPT-2 124M architecture
n_layer = 12
n_head  = 12
n_embd  = 768
block_size = 1024
dropout = 0.0

# Training
batch_size    = 8
gradient_accumulation_steps = 64   # 实际有效 batch = 512 * 1024 tokens
max_iters     = 600000
learning_rate = 6e-4
lr_decay_iters = 600000
min_lr = 6e-5
warmup_iters = 2000
weight_decay = 0.1

# Logging
eval_interval = 1000
log_interval  = 10
eval_iters    = 200
```

```bash
python train.py config/train_fineweb.py
```

---

## 📊 Token 预算总结

| 数据集子集 | Tokens | 足够训练 124M 吗？ |
| --- | --- | --- |
| `sample-350BT` | ~350B | ✅ 完整 GPT-2 规模 |
| `sample-100BT` | ~100B | ✅ 强劲结果 |
| **`sample-10BT`** | **~10B** | **✅ 良好的基准 (Good baseline)** |
| 单个 shard | ~500M | ⚠️ 欠拟合 |

GPT-2 是在约 100B tokens 上训练的。`sample-10BT` 可以产生不错的效果；`sample-100BT` 则能让你更接近原始模型的表现。

---

## ⚡ 完整工作流总结

```
DigitalOcean (数据准备)            RTX 4070 本地 (训练)
─────────────────────────         ──────────────────────────
download_fineweb.py (stream)  →   rsync train.bin / val.bin
prepare.py (tokenize)         →   python train.py
```

无需代理，无需镜像 —— DigitalOcean 的美国/欧洲区域可以全速下载 HuggingFace 资源。

参考资料：

- [HuggingFaceFW/fineweb Dataset](https://huggingface.co/datasets/HuggingFaceFW/fineweb)
- [nanoGPT GitHub](https://github.com/karpathy/nanoGPT)
- [tiktoken](https://github.com/openai/tiktoken)
