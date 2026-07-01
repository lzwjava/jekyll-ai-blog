---
audio: false
generated: true
image: false
lang: en
layout: post
title: Prepare FineWeb for nanoGPT Training
translated: false
type: note
---

Question: How do I download large FineWeb dataset on a DigitalOcean server (no proxy needed) using Hugging Face libraries, and prepare it for training nanoGPT to achieve GPT-2 124M level?

Answer:

## Downloading FineWeb on DigitalOcean with Hugging Face

Since you're on DigitalOcean (outside China), you can use **HuggingFace directly** — no mirror needed.

---

## 🖥️ Recommended DigitalOcean Droplet

For data prep only (no training):

- **4 vCPU, 8GB RAM, 100GB+ disk** (CPU-optimized droplet)
- Training should still happen on your RTX 4070 locally

---

## Step 1: Install Dependencies

```bash
pip install huggingface_hub datasets tiktoken numpy tqdm
```

---

## Step 2: Download FineWeb via `huggingface_hub`

FineWeb is hosted at `HuggingFaceFW/fineweb`. Use the streaming or snapshot approach:

### Option A — Stream & Write (memory-safe, recommended for 2GB RAM)

```python
# download_fineweb.py
from datasets import load_dataset
import os

output_file = "fineweb_extracted_all.txt"
total_docs = 0

# "sample-10BT" = 10 billion token sample — good for GPT-2 124M training
dataset = load_dataset(
    "HuggingFaceFW/fineweb",
    name="sample-10BT",
    split="train",
    streaming=True   # <-- key: no RAM explosion
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

Run it:

```bash
python download_fineweb.py
```

> ✅ `sample-10BT` = ~10B tokens, enough to match GPT-2 training scale
> ✅ Streaming means you never load the full dataset into RAM

---

### Option B — Download Parquet Shards Directly (faster, needs more disk)

```python
from huggingface_hub import snapshot_download

snapshot_download(
    repo_id="HuggingFaceFW/fineweb",
    repo_type="dataset",
    allow_patterns=["data/CC-MAIN-2024-10/*.parquet"],  # one crawl = ~tens of GB
    local_dir="./fineweb_parquet"
)
```

Then extract with your existing `extract_fineweb.py`.

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

# 90/10 split
split = int(len(all_tokens) * 0.9)
train_ids = np.array(all_tokens[:split], dtype=np.uint16)
val_ids   = np.array(all_tokens[split:], dtype=np.uint16)

train_ids.tofile(train_file)
val_ids.tofile(val_file)
print(f"train.bin: {len(train_ids):,} tokens")
print(f"val.bin:   {len(val_ids):,} tokens")
```

---

## Step 4: Transfer to Your GPU Machine

```bash
# From your local RTX 4070 machine:
rsync -avz --progress user@your-droplet-ip:~/fineweb/train.bin ~/nanoGPT/data/fineweb/
rsync -avz --progress user@your-droplet-ip:~/fineweb/val.bin  ~/nanoGPT/data/fineweb/
```

---

## Step 5: Train nanoGPT (GPT-2 124M config)

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
gradient_accumulation_steps = 64   # effective batch = 512 * 1024 tokens
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

## 📊 Token Budget Summary

| Dataset Subset | Tokens | Enough for 124M? |
| --- | --- | --- |
| `sample-350BT` | ~350B | ✅ Full GPT-2 scale |
| `sample-100BT` | ~100B | ✅ Strong results |
| **`sample-10BT`** | **~10B** | **✅ Good baseline** |
| Single shard | ~500M | ⚠️ Underfit |

GPT-2 was trained on ~100B tokens. `sample-10BT` gives decent results; `sample-100BT` gets you closer to the original.

---

## ⚡ Full Workflow Summary

```
DigitalOcean (data prep)          RTX 4070 local (training)
─────────────────────────         ──────────────────────────
download_fineweb.py (stream)  →   rsync train.bin / val.bin
prepare.py (tokenize)         →   python train.py
```

No proxy, no mirror — HuggingFace downloads at full speed from DigitalOcean US/EU regions.

References:

- [HuggingFaceFW/fineweb Dataset](https://huggingface.co/datasets/HuggingFaceFW/fineweb)
- [nanoGPT GitHub](https://github.com/karpathy/nanoGPT)
- [tiktoken](https://github.com/openai/tiktoken)
