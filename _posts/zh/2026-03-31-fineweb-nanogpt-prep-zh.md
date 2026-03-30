---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 用于 nanoGPT 训练的 FineWeb 数据准备
translated: true
type: note
---

以下为您仓库的详细说明，以及如何为 nanoGPT 准备 FineWeb 数据：

---

## 📁 Repo Structure

- **`requirements.txt`** — `gensim`, `mediawiki-dump`, `pandas`, `pyarrow`
- **`train/`** — 用于下载、提取 FineWeb + Wikipedia 以及在其上进行 training 的脚本和 logs

## 🔄 Data Pipeline (FineWeb → nanoGPT)

您的脚本展示了一个清晰的 3 步流程：

### Step 1: Download FineWeb Parquet Shards

```bash
# 从仓库运行，例如：
bash train/wget_fineweb_mirror_1.sh      # 下载 shard 0 (~500MB-1GB)
bash train/wget_fineweb_mirror_2_5.sh    # 下载 shards 1-10
bash train/wget_fineweb_mirror_11_20.sh  # 下载 shards 11-20
```

使用 `hf-mirror.com`（亚洲地区速度更快）。Shards 会保存到 `fineweb_test_dump/` 目录中。

### Step 2: Extract Text from Parquet → Plain Text

```bash
python train/extract_fineweb.py
```

- 读取所有 `fineweb_test_dump/000_*.parquet` 文件
- 提取 `text` 列
- 写入到 `fineweb_test_dump/fineweb_extracted_all.txt`
- 每个 document 之间通过 `<|endoftext|>` token 分隔

### Step 3: Tokenize with nanoGPT's `prepare.py`

nanoGPT 需要 tokenized 数据的单个 `train.bin` / `val.bin` 文件。您需要：

1. 将 `fineweb_extracted_all.txt` 复制到您的 nanoGPT data 目录，例如：
   ```bash
   mkdir -p ~/nanoGPT/data/fineweb
   cp fineweb_test_dump/fineweb_extracted_all.txt ~/nanoGPT/data/fineweb/
   ```

2. 创建一个 `prepare.py`（或适配 nanoGPT 现有的脚本），该脚本负责：
   - 读取文本文件
   - 使用 GPT-2 BPE 进行 Tokenizes（使用 `tiktoken` 或 `transformers` tokenizer）
   - 划分为 train (90%) / val (10%)
   - 保存为 `train.bin` 和 `val.bin` (numpy uint16 arrays)

3. 运行它：
   ```bash
   cd ~/nanoGPT
   python data/fineweb/prepare.py
   ```

### Step 4: Train

```bash
cd ~/nanoGPT
python train.py config/train_fineweb.py
```

您的 `train_log_fineweb3.txt` 显示了之前使用的 config：
- **125M params** (12 layers, 12 heads, 768 embd)
- **block_size=1024**, batch_size=8, grad_accum=64
- **12K iters**, 约 3B tokens
- 在 RTX 4070 上训练，约 15% MFU, ~9.3s/iter

---

**⚠️ 注意事项：** 该服务器 **没有 GPU**（仅 1 vCPU, 2GB RAM）。在上面训练 nanoGPT 只能使用 CPU，速度会极其缓慢。Logs 显示您之前是在本地 RTX 4070 上进行的训练。

需要我仅在服务器上运行 **download + extract** 步骤来准备数据吗？还是您希望在拥有 GPU 的本地机器上进行训练？