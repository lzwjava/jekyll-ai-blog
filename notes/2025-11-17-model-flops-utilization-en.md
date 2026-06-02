---
audio: false
generated: true
image: false
lang: en
layout: post
model: openai/gpt-5
title: Understanding Model FLOPs Utilization
translated: false
type: note
---

In NanoGPT, **MFU** stands for **Model FLOPs Utilization**.

It tells you **how much of your GPU’s theoretical compute (FLOPs) the model is actually using during training**.
Think of it as a rough “GPU efficiency” indicator.

Here’s what it means in practice:

**• 0–20% MFU:**
Typical for small models, small batch sizes, or when the GPU is under-utilized.

**• 30–50% MFU:**
Quite good for a modest model on consumer GPUs.

**• 50–70% MFU:**
Very strong utilization — usually large batch sizes, well-tuned kernels.

**• 80%+ MFU:**
Near the limit; only happens for large models with optimized kernels (FlashAttention, fused ops, bf16, etc.).

Your number:

```
mfu 10.69%
```

This is normal for a 125M-parameter model on a 4070. Small models don’t fully utilize the GPU because:

* The matmuls are too small to saturate the SMs
* Batch size is small
* Some overhead (dataloader, Python) dominates
* The GPU is built for huge matrix multiplications, not tiny ones

If you want to push MFU higher, you can try:

* Increasing **batch size** (max tokens per batch)
* Increasing **model size**
* Using **FlashAttention**
* Using **CUDA graph capture** (already used in newer configs)

But for small models, MFU ~10–20% is expected and totally fine.

If you want, I can help you read your config and show exactly how your MFU relates to your batch size and parameter count.
