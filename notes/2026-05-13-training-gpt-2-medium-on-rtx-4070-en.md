---
audio: false
generated: true
image: false
lang: en
layout: post
title: Training GPT-2 Medium on RTX 4070
translated: false
type: note
---

**Question:** How do I train GPT-2 Medium on a local RTX 4070?

---

**Answer:**

## First: Know Your Hardware Constraint

The RTX 4070 has **12GB of GDDR6X VRAM**, which is the critical bottleneck. GPT-2 Medium has 345M parameters. In FP32 that alone takes ~1.4GB, but during training you also need memory for optimizer states, gradients, and activations — this can multiply VRAM usage by 4–6x, pushing toward 8–10GB. It is **tight but doable** on 12GB with the right settings.

---

## Step-by-Step: Training GPT-2 Medium with nanoGPT on RTX 4070

### Step 1 — Install Prerequisites

```bash
# Create a conda environment
conda create -n nanogpt python=3.10 -y
conda activate nanogpt

# Install PyTorch with CUDA 12.x support
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# Install nanoGPT dependencies
pip install numpy transformers datasets tiktoken wandb tqdm
```

Then clone nanoGPT:

```bash
git clone https://github.com/karpathy/nanoGPT
cd nanoGPT
```

---

### Step 2 — Prepare Your Dataset

For the standard Shakespeare toy dataset (fastest to test):

```bash
python data/shakespeare_char/prepare.py
```

For a more serious dataset (OpenWebText, ~54GB download):

```bash
python data/openwebtext/prepare.py
```

---

### Step 3 — Create a Config for GPT-2 Medium on 12GB VRAM

Create a file `config/train_gpt2_medium_4070.py`:

```python
# GPT-2 Medium config tuned for RTX 4070 (12GB VRAM)
out_dir = 'out-gpt2-medium'
eval_interval = 500
eval_iters = 100
log_interval = 10

# Critical memory-saving settings
batch_size = 4              # Reduce from default 12
block_size = 512            # Reduce from 1024 to save memory
gradient_accumulation_steps = 32  # Compensates for small batch size

# GPT-2 Medium architecture
n_layer = 24
n_head = 16
n_embd = 1024
dropout = 0.0

# Key memory optimizations
compile = True              # torch.compile speeds up training
dtype = 'bfloat16'         # Half precision — saves ~50% VRAM

# Gradient checkpointing (add inside model if needed)
# Trades compute for memory — essential for 12GB cards

learning_rate = 3e-4
max_iters = 100000
lr_decay_iters = 100000
min_lr = 3e-5
beta2 = 0.95
warmup_iters = 2000
```

---

### Step 4 — Launch Training

```bash
python train.py config/train_gpt2_medium_4070.py
```

Monitor VRAM usage in a second terminal:

```bash
watch -n 1 nvidia-smi
```

---

### Step 5 — If You Get Out-of-Memory (OOM) Errors

Apply these fixes in order, from easiest to most involved:

**Fix 1 — Reduce batch size further:**
```python
batch_size = 2
gradient_accumulation_steps = 64  # Keep effective batch = 128 tokens
```

**Fix 2 — Enable gradient checkpointing** (in `model.py`, inside the Block class):
```python
# In the forward pass, wrap with:
from torch.utils.checkpoint import checkpoint
x = checkpoint(self.attn, x)
```

This trades compute time for memory — roughly 30–40% more computation but saves significant VRAM.

**Fix 3 — Reduce block size:**
```python
block_size = 256  # Cuts quadratic attention memory in half vs 512
```

**Fix 4 — Use `bfloat16` (make sure it's set):**
```python
dtype = 'bfloat16'
```

Using mixed precision (AMP) cuts memory and speeds up training; enabling gradient checkpointing for deep models reduces activation memory at the cost of extra compute. Reducing batch size to fit the model and accumulating gradients across steps simulates larger effective batch sizes.

---

### Step 6 — Alternative: Fine-tune Pretrained GPT-2 Medium (Much Easier)

Instead of training from scratch, load OpenAI's pretrained weights and fine-tune on your own data. This is faster, cheaper, and produces better results:

```bash
python train.py \
  --init_from=gpt2-medium \
  --data_dir=data/shakespeare_char \
  --max_iters=5000 \
  --learning_rate=3e-5 \
  --dtype=bfloat16 \
  --batch_size=4 \
  --block_size=512
```

This downloads the pretrained GPT-2 Medium weights and adapts them to your dataset — achievable in **hours** rather than weeks.

---

## Realistic Expectations on RTX 4070

| Task | Feasibility | Estimated Time |
|---|---|---|
| Fine-tune GPT-2 Medium on Shakespeare | ✅ Easy | 1–3 hours |
| Train GPT-2 Medium from scratch (small dataset) | ✅ With tweaks | Days |
| Train GPT-2 Medium on full OpenWebText | ⚠️ Very slow | Weeks–months |
| Train GPT-2 Large (774M) | ❌ OOM without heavy tricks | N/A |

For LLM work, VRAM capacity trumps architectural improvements — 12GB of VRAM offers flexibility for running 7B models at higher precision or experimenting with smaller training tasks. GPT-2 Medium training is right at the edge of what 12GB can comfortably handle.

---

## Summary

Your RTX 4070 (12GB) **can** train GPT-2 Medium, but you must use `bfloat16`, small batch sizes (2–4), gradient accumulation, and optionally gradient checkpointing. The sweet spot is **fine-tuning** the pretrained GPT-2 Medium on your own dataset — this takes hours not weeks, and the result is far better than training from scratch at this scale.

---

**References:**

- [nanoGPT GitHub — Andrej Karpathy](https://github.com/karpathy/nanoGPT)
- [RTX 4070 Specs — GroovyComputers](https://groovycomputers.ca/blogs/resources/rtx-4070-specs)
- [12GB GPU Deep Learning Guide — Quora](https://www.quora.com/Is-12GB-RAM-GeForce-RTX-4080-a-good-graphics-card-to-use-for-medium-sized-deep-learning-models)
- [Best GPU for Local LLM 2026 — NutStudio](https://nutstudio.imyfone.com/llm-tips/best-gpu-for-local-llm/)
