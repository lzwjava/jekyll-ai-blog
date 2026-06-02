---
audio: false
generated: true
image: false
lang: en
layout: post
title: Training GPT-3 6.7B on MI300X
translated: false
type: note
---

**Question:** Assuming nanoGPT is capable, how do I train GPT-3 6.7B end-to-end on MI300X using nanoGPT?

**Answer:**

## Full Step-by-Step

### Step 1: Setup Volume

```bash
# SSH into fresh droplet
ssh root@<new-ip>

# Mount your persistent volume
lsblk  # find your volume, e.g. /dev/sda
mkdir -p /mnt/data
mount /dev/sda /mnt/data

ls /mnt/data
# raw/  tokens/  checkpoints/
```

### Step 2: Setup Environment

```bash
# ROCm is pre-installed on AMD GPU droplet
rocm-smi  # verify MI300X visible

pip install torch torchvision --index-url https://download.pytorch.org/whl/rocm6.1
pip install numpy tiktoken datasets tqdm wandb

# Clone nanoGPT
cd /mnt/data
git clone https://github.com/karpathy/nanoGPT
cd nanoGPT
```

### Step 3: Prepare Data (The Pile or OpenWebText)

```bash
# OpenWebText (~40GB, GPT-2 style) — smaller, good start
python data/openwebtext/prepare.py

# output:
# /mnt/data/tokens/train.bin  (~17GB)
# /mnt/data/tokens/val.bin    (~8MB)
```

For GPT-3 scale you really want more data — use The Pile:

```python
# data/pile/prepare.py — write this yourself
from datasets import load_dataset
import numpy as np
import tiktoken

enc = tiktoken.get_encoding('gpt2')

def tokenize(example):
    ids = enc.encode_ordinary(example['text'])
    ids.append(enc.eot_token)
    return {'ids': ids, 'len': len(ids)}

dataset = load_dataset('EleutherAI/pile', split='train', streaming=True)

# write to binary
arr = np.memmap('/mnt/data/tokens/train.bin', dtype=np.uint16, mode='w+', shape=(400_000_000_000,))
# stream and fill...
```

### Step 4: Patch nanoGPT for 6.7B

Two critical patches:

**Patch 1 — Gradient Checkpointing:**

```python
# model.py — in GPT.forward()
from torch.utils.checkpoint import checkpoint

# replace this:
for block in self.transformer.h:
    x = block(x)

# with this:
for block in self.transformer.h:
    x = checkpoint(block, x, use_reentrant=False)
```

**Patch 2 — Fix config path for data:**

```python
# in train.py, update data_dir default
data_dir = os.path.join('/mnt/data/tokens', dataset)
```

### Step 5: Write the 6.7B Config

```python
# config/train_gpt3_6b.py

# model
n_layer = 32
n_head  = 32
n_embd  = 4096
block_size = 2048
bias = False
dropout = 0.0

# data
dataset = 'pile'  # points to /mnt/data/tokens/pile
data_dir = '/mnt/data/tokens'

# training
batch_size = 4
gradient_accumulation_steps = 160  # effective batch = 640
max_iters = 600_000
warmup_iters = 2_000
lr_decay_iters = 600_000

# optimizer
learning_rate = 1e-4
min_lr = 1e-5
beta1 = 0.9
beta2 = 0.95
weight_decay = 0.1
grad_clip = 1.0

# precision — critical for MI300X
dtype = 'bfloat16'

# checkpointing
out_dir = '/mnt/data/checkpoints'
eval_interval = 1000
save_checkpoint_interval = 1000  # nanoGPT uses eval_interval for this
keep_last_n = 3  # you need to patch this in, see below

# logging
wandb_log = True
wandb_project = 'gpt3-6b'
wandb_run_name = 'mi300x-run1'

# system
device = 'cuda'  # ROCm exposes as cuda
compile = False  # torch.compile ROCm support is patchy, try True first
```

### Step 6: Patch Checkpoint Rotation (keep last N)

nanoGPT saves one `ckpt.pt` and overwrites. Patch to keep last 3:

```python
# in train.py, find where it saves checkpoint
# replace:
torch.save(checkpoint, os.path.join(out_dir, 'ckpt.pt'))

# with:
ckpt_path = os.path.join(out_dir, f'ckpt_{iter_num}.pt')
torch.save(checkpoint, ckpt_path)

# rotate: delete old checkpoints beyond last 3
import glob
ckpts = sorted(glob.glob(os.path.join(out_dir, 'ckpt_*.pt')))
for old in ckpts[:-3]:
    os.remove(old)
    print(f"deleted old checkpoint: {old}")
```

### Step 7: Launch Training

```bash
cd /mnt/data/nanoGPT

# single GPU (MI300X has 192GB, enough for 6.7B + grad checkpointing)
python train.py config/train_gpt3_6b.py

# if you want to be safe, run in tmux
tmux new -s train
python train.py config/train_gpt3_6b.py 2>&1 | tee /mnt/data/logs/train.log
# Ctrl+B D to detach
```

### Step 8: Monitor

```bash
# GPU utilization
watch -n 1 rocm-smi

# training log
tail -f /mnt/data/logs/train.log

# wandb — open in browser
# https://wandb.ai/your-project/gpt3-6b
```

Expected output:

```
iter 0:    loss 11.07, time 4200ms, mfu 0.12%
iter 100:  loss 7.43,  time 3800ms, mfu 38.2%
iter 1000: loss 4.21,  time 3750ms, mfu 39.1%
```

### Step 9: End of Session — Safe Shutdown

```bash
# In tmux, checkpoint is saved every eval_interval
# Ctrl+C cleanly, nanoGPT saves on exit? No — so wait for a checkpoint save
# then Ctrl+C

# unmount volume
umount /mnt/data

# detach via doctl from your MacBook
doctl compute volume-action detach <volume-id> <droplet-id>

# destroy droplet
doctl compute droplet delete <droplet-id> --force
```

### Step 10: Resume Next Session

```bash
# new droplet, attach volume, mount
mount /dev/sda /mnt/data

# nanoGPT auto-resumes from latest checkpoint
python train.py config/train_gpt3_6b.py
# it finds ckpt_*.pt in out_dir and resumes automatically
```

## Expected Training Time (Rough)

GPT-3 6.7B, 300B tokens (subset of Pile):

```
MI300X theoretical: ~200 TFLOPS bf16
Realistic MFU ~40%: ~80 TFLOPS effective

6.7B params × 6 FLOPs/token × 300B tokens
= 1.2 × 10^22 FLOPs total

1.2e22 / 80e12 = 150,000 seconds
= ~42 days continuous
```

At $2/hr:

```
42 days × 24hr × $2 = ~$2,016
```

That's real money — so **train on a subset first** (10B tokens, ~3 days, ~$144) to validate loss is decreasing correctly before committing to a full run.

## Bottom Line Checklist

```
✅ Mount /mnt/data volume
✅ pip install deps (torch ROCm, tiktoken)
✅ prepare data → /mnt/data/tokens/
✅ patch gradient checkpointing in model.py
✅ patch checkpoint rotation in train.py
✅ write config/train_gpt3_6b.py
✅ tmux + launch
✅ monitor rocm-smi + wandb
✅ safe shutdown → detach volume → destroy droplet
✅ resume next session by attaching volume
```
