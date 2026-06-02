---
audio: false
generated: true
image: false
lang: en
layout: post
model: openai/gpt-5
title: GPU Memory vs Compute Utilization Explained
translated: false
type: note
---

Ah, this is a common point of confusion. The GPU memory usage being high (like 90% in your case) **doesn’t mean your GPU is fully utilized**. Memory usage and compute utilization are related but separate metrics. Here’s why you see it:

1. **Model and optimizer take a lot of memory**

   * Your 125M-parameter model + Adam optimizer + gradients + temporary buffers can easily take up **most of the GPU memory**, especially on GPUs with 12 GB like your 4070.
   * This is **memory allocated**, not actively computing.

2. **Small model = low FLOPs usage**

   * Even if almost all memory is used, the actual **compute utilization (MFU)** can remain low because the operations are small. The GPU isn’t doing enough parallel math to saturate all cores.

3. **Memory fragmentation and caching**

   * PyTorch (or CUDA) often **pre-allocates or caches memory** to avoid repeated allocations. So the memory bar looks full even if some of it isn’t actively being used at this instant.

4. **Batch size impact**

   * Larger batch sizes increase both memory usage **and** compute utilization. But if your batch is small, the memory is mostly taken by static model parameters and optimizer states, not actual heavy computation.

So in your case:

* ~90% memory usage = normal for a model + optimizer on a 12 GB GPU.
* ~10% MFU = normal for a small model with small batches — the GPU is waiting on small matrix multiplies rather than crunching huge matrices.

If you want, I can break down **roughly how much memory each part (model, optimizer, gradients, etc.) is taking** for your 125M NanoGPT model. It’s quite instructive.
