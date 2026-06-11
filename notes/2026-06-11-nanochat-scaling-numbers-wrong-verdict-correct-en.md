---
audio: false
generated: true
image: false
lang: en
layout: post
title: Nanochat Scaling Numbers Wrong Verdict Correct
translated: false
type: note
---

**Question:** Review this nanochat scaling analysis (model sizes, CPU DDP speed estimates, training horizons) — are the numbers right, and is the verdict sound?

**Answer:**

The verdict is correct — CPU DDP for plumbing/learning, GPU for d12+ — but several numbers in the analysis don't survive a first-principles check. Three issues worth fixing before you plan compute around this table.

## 1. The FLOPs/token column mixes 2N and 6N

Training FLOPs per token ≈ **6N** (2N forward, 4N backward). Check the table against that:

```
d4:  6 × 37M  = 222M   (table says 72M  ≈ 2N forward-only)
d8:  6 × 92M  = 552M   (table says 250M ≈ ~3N, neither)
d12: 6 × 186M = 1.1B   (table says 1.7B ≈ 6N of an inflated param count)
```

The column is internally inconsistent by ~3x, so every extrapolation built on it inherits that error.

## 2. The param counts for d12 and d20 are wrong

nanochat: `dim = depth × 64`, vocab 65,536, untied embeddings, standard 12·d²·L transformer body:

```python
def params(depth, vocab=65536):
    d = depth * 64
    return 12 * d*d * depth + 2 * vocab * d

# d4:  36.7M   ✓ matches table (37M) — note: 91% embeddings!
# d8:  92.3M   (table: 80M, close)
# d12: 186M    (table: 286M ✗)
# d20: 561M    (table: 1.0B ✗)
```

The d20 = 561M figure is the sanity anchor — that's exactly Karpathy's $100 speedrun model. The table's 1.0B is off by ~2x, which cascades into the time estimates.

Also note d4 is **91% embedding parameters**. Its loss curves tell you almost nothing about how d12+ will behave — it's mostly learning a lookup table. Fine for validating the DDP plumbing, useless as a scaling data point.

## 3. The speed extrapolation is ~5x too pessimistic for d12

If you're compute-bound, tok/sec scales with 1/FLOPs using *consistent* 6N:

```
d4 → d12 slowdown = 186M / 37M ≈ 5x   →  115/5 ≈ 23 tok/sec
(not 24x → 5 tok/sec)
```

But it doesn't matter, because at 23 tok/sec, one d12 step at 65,536 tokens/step is **47 minutes**. Karpathy's 200k-step horizon is ~18 years of CPU. The conclusion survives; the table just gets there with wrong arithmetic.

One real risk the analysis missed: **Gloo allreduce over your LAN**. d12 gradients = 186M × 4B ≈ 744MB per step. On gigabit ethernet that's ~12s of comm. Negligible against 47-min compute steps, but if you shrink the batch to iterate faster (e.g. 2048 tokens/step), comm becomes the bottleneck and the "compute-bound, FLOPs ∝ time" model breaks entirely. Measure, don't extrapolate:

```python
# drop into the train loop to decompose step time
import time, torch.distributed as dist

t0 = time.perf_counter()
loss = model(x, y); loss.backward()
t1 = time.perf_counter()                  # compute
# DDP allreduce overlaps with backward; force a sync point to isolate it:
dist.barrier(); t2 = time.perf_counter()  # comm + straggler
opt.step(); opt.zero_grad()
print(f"compute {t1-t0:.1f}s  sync {t2-t1:.1f}s")
```

If sync time is significant, use gradient accumulation (more micro-batches per allreduce) — comm cost amortizes linearly.

## What I'd actually do

- **d4 CPU DDP**: stop around step 1000. You've validated Gloo, the data loader, and checkpointing. That was the point.
- **Skip the 3-day d8 CPU grind entirely.** d8 on the 4070 is a few hours. Burning 3 days of two machines to produce what one overnight GPU run produces is negative-value, even for learning — you learn the same things from the GPU run plus you get a usable checkpoint.
- **d12/d20 → MI300X.** The speedrun is ~32 H100-hours for d20; MI300X is roughly H100-class on dense BF16, so ballpark 25–35 hours ≈ **$50–70 at your $2/hr rate**. That's the full d20 with chat fine-tuning for less than the electricity cost of a month of CPU DDP. Single-GPU means no DDP comm at all — set `device_batch_size` to fill the 192GB HBM and use grad accum for the rest.

The d4 loss going 10.40 → 10.39 in 5 steps is expected, by the way — init loss ≈ ln(65536) ≈ 11.09, and the first thing the model learns is unigram statistics, which takes a few hundred steps to flush through. Nothing interesting happens before ~1k steps at this scale.

**References:**

- [nanochat (karpathy/nanochat)](https://github.com/karpathy/nanochat)
