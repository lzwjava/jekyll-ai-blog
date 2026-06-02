---
audio: false
generated: true
image: false
lang: en
layout: post
title: Training GPT-3 on One MI300X
translated: false
type: note
---

**Question:** How long would it take to train GPT-3 6.7B on a single MI300X?

**Answer:**

## The Math from First Principles

GPT-3 6.7B was trained on **300B tokens** (from the paper).

```
FLOPs per token ≈ 6 × N
where N = number of parameters

6 × 6.7B = 40.2 GFLOPs per token
300B tokens × 40.2 GFLOPs = 1.206 × 10^22 FLOPs total
```

## MI300X Real Performance

```
MI300X peak bf16:     ~1,300 TFLOPS (theoretical)
Realistic MFU:        30-45% for training
Effective throughput: ~400-600 TFLOPS
```

Let's use **40% MFU = 520 TFLOPS**:

```
1.206 × 10^22 FLOPs / 520 × 10^12 FLOPs/sec
= 23,192,307 seconds
= 268 days
```

## By MFU Scenario

| MFU | Effective TFLOPS | Days | Cost @ $2/hr |
|-----|-----------------|------|--------------|
| 20% | 260 TFLOPS | 537 days | ~$25,776 |
| 30% | 390 TFLOPS | 358 days | ~$17,184 |
| 40% | 520 TFLOPS | 268 days | ~$12,864 |
| 50% | 650 TFLOPS | 215 days | ~$10,320 |

## Reality Check — What OpenAI Actually Used

```
GPT-3 175B: 3.14 × 10^23 FLOPs, 10,000 V100s, ~14 days
GPT-3 6.7B: proportionally ~1/26th of that compute

On 10,000 V100s: ~13 hours for 6.7B
On 1 MI300X:     ~268 days
```

So you're **alone doing what took OpenAI a cluster of 10,000 GPUs.**

## Practical Options

### Option A: Reduce Tokens (Most Practical)

```
Chinchilla optimal for 6.7B = ~134B tokens (20× params)
vs GPT-3's 300B tokens

134B tokens on MI300X @ 40% MFU:
= 1.206e22 × (134/300) / 520e12
= 120 days, ~$5,760
```

Still long. Go smaller:

```
10B tokens:  ~9 days,  ~$432   ← proof of concept
30B tokens:  ~27 days, ~$1,296 ← meaningful run
100B tokens: ~89 days, ~$4,272 ← serious run
```

### Option B: Smaller Model, Same Architecture

| Model | Params | 100B tokens | Cost |
|-------|--------|-------------|------|
| GPT-3 Small | 125M | ~2 days | ~$96 |
| GPT-3 Medium | 350M | ~5 days | ~$240 |
| GPT-3 XL | 1.3B | ~18 days | ~$864 |
| GPT-3 6.7B | 6.7B | ~89 days | ~$4,272 |

### Option C: Multiple MI300X Droplets

DigitalOcean doesn't support multi-GPU droplets easily, but AMD Dev Cloud might have multi-GPU nodes — **8× MI300X would cut time to ~34 days for full 300B token run.**

## My Recommendation for You

```
Phase 1: GPT-3 Small (125M), 10B tokens
         ~4 hours, ~$8
         Goal: validate pipeline, data, checkpointing

Phase 2: GPT-3 XL (1.3B), 30B tokens
         ~5 days, ~$240
         Goal: confirm loss curves, MFU, wandb tracking

Phase 3: GPT-3 6.7B, 30B tokens
         ~27 days, ~$1,296
         Goal: serious training run, publishable loss
```

**Don't jump straight to 6.7B + 300B tokens.** Karpathy's own advice: run small experiments first, confirm everything is working, then scale. A bug at day 25 of a 27-day run is a $1,200 mistake.

## Bottom Line

```
Full GPT-3 6.7B (300B tokens) on 1× MI300X:
  ~268 days, ~$12,864  ← not practical alone

Practical target:
  GPT-3 1.3B, 30B tokens
  ~5 days, ~$240       ← this is your sweet spot
```

The goal isn't to replicate OpenAI's run. It's to **learn the full pipeline at meaningful scale** — and 1.3B at 30B tokens does that at a price you can actually pay.
