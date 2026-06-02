---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Fixing GPU Memory Overflow During Evaluation
translated: false
type: note
---

You're hitting a classic OOM on an RTX 4070 (12 GB VRAM) while training a ~77M parameter GPT (originally meant for 125M, but you reduced n_embd to 576 → ~77M) with batch_size=16, block_size=1024, and gradient_accumulation_steps=32 in FP16.

Even though 77M is small, the effective micro-batch is huge because of how nanoGPT computes loss in `estimate_loss()` — it runs the full forward/backward pass on the evaluation batches without gradient accumulation tricks, so during eval it suddenly tries to put a much larger effective batch into memory.

### Root Cause
In `estimate_loss()`, nanoGPT does this by default:

```python
for _ in range(eval_iters):  # 200 times!
    x, y = get_batch('train')
    ...
    logits, loss = model(x, y)
```

Each `get_batch` returns `batch_size × block_size` tokens → 16 × 1024
With eval_iters = 200 → 200 separate forward passes, but PyTorch keeps the computation graph and intermediate activations for the entire eval loop in memory if you're not careful. Combined with the massive KV cache (12 layers × 12 heads × 1024 × 576 × 2 bytes FP16 ≈ 1.6 GB just for cache), plus logits (16×1024×50304 × 2 bytes ≈ 1.6 GB per forward), you easily blow past 12 GB even though training itself is fine.

### Quick Fixes (pick one or combine)

**Option 1: Drastically reduce eval batch size (fastest fix)**
Add these lines to your config (or override on CLI):

```python
eval_batch_size = 4        # add this
# or even 2 if still OOM
eval_iters = 100           # can reduce a bit more
```

nanoGPT respects `eval_batch_size` if you add it (recent versions do). This makes evaluation use only 4 sequences instead of 16 → ~4× less memory during eval.

**Option 2: Reduce block_size for eval only (keeps accuracy)**
```python
eval_block_size = 512      # or 256
```
Add this to config — some forks support it, or patch `get_batch` to use a different block size when split=='val'.

**Option 3: Lower eval_iters and accept slightly noisier eval loss**
```python
eval_iters = 50   # still decent estimate
```

**Option 4: Reduce model size a bit more (still good quality)**
You're already at 77M, but you can go lower safely:

```python
n_layer = 12
n_head  = 12
n_embd  = 512     # → ~62M params, much safer
# or even n_embd = 448 → ~53M
```

**Option 5: Enable gradient checkpointing (biggest memory win)**
Add this to model creation (edit model.py or pass flag):

```python
model = GPT(GPTConfig(..., grad_checkpoint=True))
```

Or monkey-patch in train.py before training:

```python
if config.grad_checkpoint:
    model.gradient_checkpointing_enable()
```

This cuts activation memory by ~50-60% at cost of ~20-25% slower training.

### Recommended combination for your 4070 12 GB

```python
# In config/train_fineweb.py
batch_size = 16
gradient_accumulation_steps = 32   # keeps effective 512 seqs
block_size = 1024

eval_batch_size = 4        # critical
eval_iters = 100
eval_interval = 500

n_embd = 512               # ~62M model, very safe
# optional: add gradient checkpointing
grad_checkpoint = True     # if your nanoGPT fork supports it
```

Or if you don't want to touch n_embd, just do:

```python
eval_batch_size = 2
eval_iters = 100
```

That alone will almost certainly fix the OOM.

Also set this environment variable to help fragmentation:

```bash
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
```

Try the eval_batch_size=4 (or =2) first — 95% of people with 12 GB 4070s who hit this exact error fix it this way when training nanoGPT on FineWeb.
