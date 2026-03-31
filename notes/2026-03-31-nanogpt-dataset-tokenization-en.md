---
audio: false
generated: true
image: false
lang: en
layout: post
title: Tokenizing Large Datasets for nanoGPT Training
translated: false
type: note
---

You have a 61GB raw text file. To train nanoGPT, you need to turn it into tokenized binary files. Here's what to do:

## Step 1: Clone nanoGPT on the server

```bash
cd /root
git clone https://github.com/karpathy/nanoGPT.git
cd nanoGPT
pip install --break-system-packages torch tiktoken tqdm
```

## Step 2: Tokenize the data

```bash
cd /root/nanoGPT/data
mkdir -p fineweb
```

Create the tokenizer script:

```bash
cat > fineweb/prepare.py << 'EOF'
import numpy as np
import tiktoken
from tqdm import tqdm

enc = tiktoken.get_encoding("gpt2")
EOT = enc._special_tokens["<|endoftext|>"]

input_file = "/root/zz/fineweb_extracted_all.txt"
train_file = "fineweb/train.bin"
val_file = "fineweb/val.bin"

all_tokens = []
print("Tokenizing...", flush=True)

with open(input_file, "r", encoding="utf-8") as f:
    for line in tqdm(f):
        line = line.strip()
        if not line:
            continue
        if line == "<|endoftext|>":
            all_tokens.append(EOT)
        else:
            tokens = enc.encode_ordinary(line)
            all_tokens.extend(tokens)

print(f"Total tokens: {len(all_tokens):,}", flush=True)

# 90/10 split
split = int(len(all_tokens) * 0.9)
train_ids = np.array(all_tokens[:split], dtype=np.uint16)
val_ids = np.array(all_tokens[split:], dtype=np.uint16)

train_ids.tofile(train_file)
val_ids.tofile(val_file)
print(f"train.bin: {len(train_ids):,} tokens ({len(train_ids)*2/1024/1024/1024:.1f} GB)", flush=True)
print(f"val.bin: {len(val_ids):,} tokens ({len(val_ids)*2/1024/1024/1024:.1f} GB)", flush=True)
EOF
```

Run it:

```bash
cd /root/nanoGPT
python3 data/fineweb/prepare.py
```

⚠️ **Disk problem:** 61GB text + ~25GB tokenized = 86GB. You only have 77GB. You need to tokenize in a streaming way that deletes lines as it goes. Alternative: tokenize on the server, delete the raw text immediately after.

## Step 2 (fixed): Stream-tokenize and delete raw text

```bash
cat > /root/nanoGPT/data/fineweb/prepare.py << 'PYEOF'
import numpy as np
import tiktoken
from tqdm import tqdm
import os

enc = tiktoken.get_encoding("gpt2")
EOT = enc._special_tokens["<|endoftext|>"]

input_file = "/root/zz/fineweb_extracted_all.txt"
train_file = "/root/nanoGPT/data/fineweb/train.bin"
val_file = "/root/nanoGPT/data/fineweb/val.bin"

# Count lines first
print("Counting lines...", flush=True)
with open(input_file, "r") as f:
    total_lines = sum(1 for _ in f)
print(f"Total lines: {total_lines:,}", flush=True)

split_line = int(total_lines * 0.9)

print("Tokenizing (streaming)...", flush=True)
train_chunks = []
val_chunks = []
train_count = 0
val_count = 0

with open(input_file, "r", encoding="utf-8") as f:
    for line_num, line in enumerate(tqdm(f, total=total_lines)):
        line = line.strip()
        if not line:
            continue
        if line == "<|endoftext|>":
            tok = [EOT]
        else:
            tok = enc.encode_ordinary(line)
        
        if line_num < split_line:
            train_chunks.extend(tok)
            train_count += 1
        else:
            val_chunks.extend(tok)
            val_count += 1
        
        # Flush every 50M tokens to avoid RAM explosion
        if len(train_chunks) > 50_000_000 and line_num < split_line:
            arr = np.array(train_chunks, dtype=np.uint16)
            with open(train_file, "ab") as tf:
                arr.tofile(tf)
            train_chunks = []
        if len(val_chunks) > 50_000_000 and line_num >= split_line:
            arr = np.array(val_chunks, dtype=np.uint16)
            with open(val_file, "ab") as vf:
                arr.tofile(vf)
            val_chunks = []

# Final flush
if train_chunks:
    arr = np.array(train_chunks, dtype=np.uint16)
    with open(train_file, "ab") as tf:
        arr.tofile(tf)
if val_chunks:
    arr = np.array(val_chunks, dtype=np.uint16)
    with open(val_file, "ab") as vf:
        arr.tofile(vf)

train_size = os.path.getsize(train_file)
val_size = os.path.getsize(val_file)
print(f"\nDone!", flush=True)
print(f"train.bin: {train_size/1024/1024/1024:.1f} GB ({train_size//2:,} tokens)", flush=True)
print(f"val.bin: {val_size/1024/1024/1024:.1f} GB ({val_size//2:,} tokens)", flush=True)

# Delete raw text to free disk
os.remove(input_file)
print(f"Deleted raw text. Freed 61 GB.", flush=True)
PYEOF
```

```bash
cd /root/nanoGPT
python3 data/fineweb/prepare.py
```

## Step 3: Train

After tokenization, create the config:

```bash
cat > /root/nanoGPT/config/train_fineweb.py << 'EOF'
out_dir = 'out-fineweb'
dataset = 'fineweb'
n_layer = 12
n_head = 12
n_embd = 768
block_size = 1024
dropout = 0.0
batch_size = 8
gradient_accumulation_steps = 64
max_iters = 600000
learning_rate = 6e-4
lr_decay_iters = 600000
min_lr = 6e-5
warmup_iters = 2000
weight_decay = 0.1
eval_interval = 1000
log_interval = 10
eval_iters = 200
always_save_checkpoint = True
EOF
```

```bash
cd /root/nanoGPT
python3 train.py config/train_fineweb.py
```

---

**Summary:**
1. `git clone nanoGPT` + `pip install torch tiktoken`
2. Run `prepare.py` (tokenizes + deletes raw text to free 61GB)
3. `python3 train.py config/train_fineweb.py`

Run steps 1 and 2 first. Step 3 (training) will be very slow on CPU — ideally transfer `train.bin` + `val.bin` to your RTX 4070 for actual training.