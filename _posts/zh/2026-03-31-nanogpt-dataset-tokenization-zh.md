---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 为 nanoGPT 训练对大型数据集进行分词
translated: true
type: note
---

你有一个 61GB 的原始文本文件。为了训练 nanoGPT，你需要将其转换为 tokenized 的二进制文件。以下是操作步骤：

## Step 1: 在服务器上克隆 nanoGPT

```bash
cd /root
git clone https://github.com/karpathy/nanoGPT.git
cd nanoGPT
pip install --break-system-packages torch tiktoken tqdm
```

## Step 2: 对数据进行 Tokenize

```bash
cd /root/nanoGPT/data
mkdir -p fineweb
```

创建 tokenizer 脚本：

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
print(f"train.bin: {len(train_ids):,} tokens ({len(train_ids)*2/1024/1024/1024:.1f} GB)")
print(f"val.bin: {len(val_ids):,} tokens ({len(val_ids)*2/1024/1024/1024:.1f} GB)")
EOF
```

运行它：

```bash
cd /root/nanoGPT
python3 data/fineweb/prepare.py
```

⚠️ **磁盘问题：** 61GB 文本 + 约 25GB tokenized 数据 = 86GB。你只有 77GB。你需要以流式（streaming）方式进行 tokenize 并随之删除行。替代方案：在服务器上进行 tokenize，完成后立即删除原始文本。

## Step 2 (修正版): 流式 Tokenize 并删除原始文本

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

## Step 3: 训练

Tokenize 完成后，创建配置文件：

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

**总结：**
1. `git clone nanoGPT` + `pip install torch tiktoken`
2. 运行 `prepare.py`（进行 tokenize 并删除原始文本以释放 61GB 空间）
3. `python3 train.py config/train_fineweb.py`

先执行步骤 1 和 2。步骤 3（训练）在 CPU 上会非常慢——理想情况下，应将 `train.bin` + `val.bin` 传输到你的 RTX 4070 上进行实际训练。