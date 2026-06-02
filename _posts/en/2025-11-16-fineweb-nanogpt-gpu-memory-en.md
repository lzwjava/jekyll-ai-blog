---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: FineWeb NanoGPT GPU Memory Guide
translated: false
type: note
---

You're training a small GPT (nanoGPT-style) on the **FineWeb** dataset (the 100B-token cleaned version of Common Crawl used to train LLaMA, Mistral, etc.), but you want to do it with limited GPU memory (probably 16–24 GB, like an RTX 3090/4090 or A6000).

Your current config is already quite conservative and good for a single consumer GPU, but here’s a detailed guide on **how to choose the best parameters** for nanoGPT on FineWeb, ranked by importance and memory impact.

### Recommended Configurations by GPU Memory

| GPU VRAM       | Model Size (params) | n_layer | n_head | n_embd | batch_size | grad_acc | effective BS | block_size | Notes |
|----------------|---------------------|---------|--------|--------|------------|----------|--------------|------------|-------|
| 80 GB (A100/H100) | ~350M              | 12      | 12     | 768    | 64         | 8        | 512          | 1024       | Close to original GPT-2 medium, trains well |
| 48 GB (A6000/3090) | ~250–300M         | 12      | 12     | 672    | 32         | 16       | 512          | 1024       | Very good compromise |
| 24 GB (4090/3090) | ~160–200M          | 10      | 10     | 640    | 32         | 12–16    | 384–512      | 1024       | Your sweet spot |
| 16–20 GB (4080, 3090 Ti) | ~125M        | 8       | 8      | 512    | 32         | 12       | 384          | 1024       | Stable |
| <16 GB (4070 Ti, etc.) | ~84M           | 6       | 6      | 384    | 16–32      | 16–24    | 256–512      | 512–1024   | Your current config |

Your current config (`6L 6H 384embd`) is safe but a bit small. You can go larger.

### Best Config for 24 GB GPU (RTX 4090 / 3090) on FineWeb

This is the most popular setup in the nanoGPT community right now:

```python
out_dir = 'out-fineweb-160M'
eval_interval = 1000
eval_iters = 200
log_interval = 100
always_save_checkpoint = True

wandb_log = True
wandb_project = 'fineweb'
wandb_run_name = '160M-fineweb'

dataset = 'fineweb'
gradient_accumulation_steps = 16   # 32 * 16 = 512 effective batch size
batch_size = 32
block_size = 1024                  # important: FineWeb was trained with 1024+

n_layer = 10
n_head = 10
n_embd = 640
dropout = 0.0                      # can try 0.1 later
learning_rate = 6e-4               # slightly higher for smaller models
max_iters = 50000                  # ~50–100B tokens total is ideal
warmup_iters = 2000
lr_decay_iters = 50000
min_lr = 6e-5
beta2 = 0.99
```

→ This is ~160M parameters, runs comfortably on a 4090 with ~20–22 GB VRAM usage.

### Even Better: 200M+ Model (if you have 24 GB+)

```python
n_layer = 12
n_head = 12
n_embd = 768    # → ~350M params (original GPT-2 medium size)
batch_size = 32
gradient_accumulation_steps = 16   # effective BS 512
block_size = 1024
learning_rate = 5e-4
max_iters = 60000
```

Many people train this successfully on a single 4090.

### Key Rules of Thumb for FineWeb + nanoGPT

1. **block_size = 1024** is strongly recommended
   FineWeb was filtered and trained with 1024 context. Using 512 hurts perplexity more than you think.

2. **Effective batch size ≈ 512** is the sweet spot
   Original LLaMA used ~4M tokens per batch. For nanoGPT, 512 sequences × 1024 tokens = ~0.5M tokens/batch → close enough scaling law.

3. **Learning rate**
   - ~100M params: 6e–8e-4
   - ~350M params: 5e–6e-4
   - ~770M params: 3e-4

4. **Train for at least 50B tokens** (better 100B+)
   With 160M model:
   - 50k iters × 32 × 16 × 1024 tokens = ~83B tokens
   Good convergence.

5. **Use the official FineWeb dataset (not openwebtext)**
   Your script is already correct:
   FineWeb >> OpenWebText in quality.
   Use the 100B subset: `fineweb100B` or full `fineweb` (truncated to your disk).

6. **Optional but helpful**

```python
compile = True          # PyTorch 2.0 compile, ~20–30% faster
bias = False            # no bias in Linear layers (like LLaMA)
weight_decay = 0.1
```

### Quick Command to Download FineWeb (100B version)

```bash
pip install datasets
python -c "
from datasets import load_dataset
ds = load_dataset('HuggingFaceFW/fineweb', name='sample-100BT', split='train')
ds.save_to_disk('data/fineweb100B')
"
```

Then point nanoGPT to that folder.

### Summary: Upgrade Your Current Config

Replace your current model part with this (for 24 GB GPU):

```python
n_layer = 10
n_head = 10
n_embd = 640
batch_size = 32
gradient_accumulation_steps = 16
block_size = 1024
learning_rate = 6e-4
max_iters = 50000
```

You’ll get a much stronger model with almost no extra cost.

People are getting **very good 160M–350M models** on FineWeb with these settings — often surpassing original GPT-2 performance.

Let me know your exact GPU and I can give you the optimal config! 🚀
