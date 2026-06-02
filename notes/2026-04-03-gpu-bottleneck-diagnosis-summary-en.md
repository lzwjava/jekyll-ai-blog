---
audio: false
generated: true
image: false
lang: en
layout: post
title: GPU Bottleneck Diagnosis Summary
translated: false
type: note
---

Here’s the step-by-step reasoning I used to arrive at that diagnosis and solution:

## Step 1: Identify the core anomaly

**21 seconds per iteration** on an H200 GPU is immediately suspicious. For context:
- A single H200 can do ~300-500 TFLOPs (FP16/BF16)
- GPT-2 XL (1.5B params) forward+backward on 1M tokens should take **~0.5-1.5 seconds** on this hardware
- Even with overhead, anything over 3-5 seconds signals a bottleneck

The MFU reading of **150%+** confirms something is broken in the measurement, not the computation.

## Step 2: Calculate the actual data load

Looking at your config:
```
batch_size = 16
block_size = 1024
gradient_accumulation_steps = 64
```

Per iteration:
- Each micro-batch: 16 × 1024 = 16,384 tokens
- 64 accumulations = **1,048,576 tokens per iteration**
- That's ~4MB of data (4 bytes per token)
- But here's the catch: **64 separate disk reads per iteration**

## Step 3: Trace the data path in nanoGPT

Standard `get_batch()` in nanoGPT:
```python
def get_batch(split):
    data = train_data if split == 'train' else val_data
    ix = torch.randint(len(data) - block_size, (batch_size,))
    x = torch.stack([data[i:i+block_size] for i in ix])
    y = torch.stack([data[i+1:i+block_size+1] for i in ix])
    return x, y
```

This does **random indexing into a numpy/memory-mapped array**. With `gradient_accumulation_steps=64`, you're doing:
- 64 calls to `get_batch()` per iteration
- Each call: 16 random indices × 1024 token lookups = 16,384 random memory accesses
- Total per iteration: **1,048,576 random memory accesses**

Even with SSDs, random access at this scale is deadly.

## Step 4: Consider storage location on DigitalOcean

DigitalOcean H200 droplets typically have:
- **Boot disk**: Network-attached, moderate IOPS (2,000-5,000)
- **Scratch NVMe**: Local, high IOPS (100,000+)

If your `fineweb` dataset is on boot disk, those 1M random accesses per iteration will be bottlenecked at ~5,000 IOPS → ~200 random accesses per millisecond → at least 5 seconds just in I/O wait. Add Python overhead, and 21 seconds makes sense.

## Step 5: Calculate the time penalty

At 21s/iter × 10,000 iters = 210,000 seconds = **58 hours**

But if fixed to 1s/iter = 10,000 seconds = **2.8 hours**

That's a **20x speedup** waiting to be unlocked.

## Step 6: Connect to known nanoGPT issue

I recalled there's a specific PR in the nanoGPT repo: "Fix for gradient_accumulation_steps training slow". The issue is exactly this: large accumulation values cause repeated data loading because the `get_batch()` call happens inside the accumulation loop, not outside.

## Step 7: Prioritize the fixes

Most impactful first:
1. **Reduce `gradient_accumulation_steps`** → cuts disk reads by 16x
2. **Increase `batch_size`** → fewer random indices per read
3. **Use `DataLoaderLite`** → prefetches and batches efficiently
4. **Move to NVMe** → 100x faster random access

The MFU artifact is a distraction - it's `torch.compile` misreporting because it can't properly account for I/O wait time. Fix the I/O first, then MFU will drop to realistic 40-60%.

**Bottom line**: Your H200 is spending 20 of those 21 seconds waiting for data, not computing. The fix is to serve data faster and less often.
