---
audio: false
generated: true
image: false
lang: en
layout: post
title: FineWeb Data Preparation for nanoGPT Training
translated: false
type: note
---

Here's the breakdown of your repo and how to prep FineWeb data for nanoGPT:

---

## 📁 Repo Structure

- **`requirements.txt`** — `gensim`, `mediawiki-dump`, `pandas`, `pyarrow`
- **`train/`** — Scripts and logs for downloading, extracting, and training on FineWeb + Wikipedia

## 🔄 Data Pipeline (FineWeb → nanoGPT)

Your scripts show a clear 3-step flow:

### Step 1: Download FineWeb Parquet Shards

```bash
# From the repo, e.g.:
bash train/wget_fineweb_mirror_1.sh      # Downloads shard 0 (~500MB-1GB)
bash train/wget_fineweb_mirror_2_5.sh    # Downloads shards 1-10
bash train/wget_fineweb_mirror_11_20.sh  # Downloads shards 11-20
```

Uses `hf-mirror.com` (faster for Asia). Shards go into `fineweb_test_dump/`.

### Step 2: Extract Text from Parquet → Plain Text

```bash
python train/extract_fineweb.py
```

- Reads all `fineweb_test_dump/000_*.parquet` files
- Extracts the `text` column
- Writes to `fineweb_test_dump/fineweb_extracted_all.txt`
- Each document separated by `<|endoftext|>` tokens

### Step 3: Tokenize with nanoGPT's `prepare.py`

nanoGPT expects a single `train.bin` / `val.bin` of tokenized data. You need to:

1. Copy `fineweb_extracted_all.txt` into your nanoGPT data dir, e.g.:
   ```bash
   mkdir -p ~/nanoGPT/data/fineweb
   cp fineweb_test_dump/fineweb_extracted_all.txt ~/nanoGPT/data/fineweb/
   ```

2. Create a `prepare.py` (or adapt nanoGPT's existing one) that:
   - Reads the text file
   - Tokenizes with GPT-2 BPE (`tiktoken` or `transformers` tokenizer)
   - Splits into train (90%) / val (10%)
   - Saves as `train.bin` and `val.bin` (numpy uint16 arrays)

3. Run it:
   ```bash
   cd ~/nanoGPT
   python data/fineweb/prepare.py
   ```

### Step 4: Train

```bash
cd ~/nanoGPT
python train.py config/train_fineweb.py
```

Your `train_log_fineweb3.txt` shows the config used before:
- **125M params** (12 layers, 12 heads, 768 embd)
- **block_size=1024**, batch_size=8, grad_accum=64
- **12K iters**, ~3B tokens
- Trained on RTX 4070 at ~15% MFU, ~9.3s/iter

---

**⚠️ One issue:** That server has **no GPU** (just 1 vCPU, 2GB RAM). Training nanoGPT there would be CPU-only and extremely slow. The logs suggest you trained on an RTX 4070 locally.

Want me to just run the **download + extract** steps on the server to prep the data? Or do you want to train locally on your GPU machine?
