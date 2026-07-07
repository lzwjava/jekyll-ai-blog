---
audio: false
generated: true
image: false
lang: en
layout: post
title: H200 FineWeb Tokenization Summary
translated: false
type: note
---

Here's the full summary of everything done on the H200 server:

---

**Server:** `38.80.152.249:30416` — NVIDIA H200 (140 GB VRAM, CUDA 13.0)
**Workdir:** `/workspace/zz/`

### 1. Setup

- SSH key created and added to GitHub
- `git@github.com:lzwjava/zz.git` cloned to `/workspace/zz/`
- `tmux` installed for session persistence
- Python deps: `tiktoken`, `numpy`, `pyarrow`, `tqdm`, `huggingface_hub`

### 2. Data Download

- **Script:** `h200/download_fineweb.py`
- **Dataset:** HuggingFaceFW/fineweb-edu — 44 parquet shards
- **Size:** 95 GB on disk, ~25.5B tokens
- **Coverage:** 4 CommonCrawl dumps (CC-MAIN-2013-20, 2013-48, 2014-10, 2014-15)
- **Speed:** ~20 MB/s, completed in ~75 min

### 3. Tokenization

- **Script:** `h200/tokenize_fineweb.py`
- **Tokenizer:** GPT-2 BPE (tiktoken), each doc prefixed with `<|endoftext|>`
- **Shard size:** 100M uint16 tokens per `.npy` file
- **Workers:** 96 CPU cores
- **Throughput:** ~8-10M tok/s

### 4. Results

| Metric | Value |
| -------- | ------- |
| **Output shards** | 358 (1 val + 357 train) |
| **Total tokens** | ~35.8B (incl. EOT prefixes) |
| **Output location** | `/workspace/zz/datasets/tokenized/` |
| **Output files** | `edufineweb_val_000000.npy` + `edufineweb_train_000001-000357.npy` |
| **Disk used** | ~104 GB on `/workspace` (187 GB total) |
| **Wall time** | ~45 min |

### 5. Commands

```bash
# Download (already done)
cd /workspace/zz
python3 h200/download_fineweb.py

# Tokenize (already done)
cd /workspace/zz
python3 h200/tokenize_fineweb.py
```

The tokenized data is ready for GPT-3 ablation training — nanoGPT-compatible format.
