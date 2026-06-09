---
audio: false
generated: true
image: false
lang: en
layout: post
title: FA2 + FP8 Training Performance
translated: false
type: note
---

Question: Can you explain the performance comparison of FA2 + FP8 in training?

Answer:

This report shows the performance impact of combining **FA2 (FlashAttention 2)** with **FP8 (8-bit floating point precision)** on a model training task, compared to other configurations. Let’s break it down:

---

### Key Metrics Explained

| Metric         | Meaning                                                                                                 |
| -------------- | ------------------------------------------------------------------------------------------------------- |
| **Step Time**  | Time to process one training step (lower is better).                                                    |
| **Throughput** | Number of tokens processed per second (higher is better).                                               |
| **MFU**        | **Multiplicative Fusion Utilization**, measures how efficiently GPU compute is used (higher is better). |
| **Memory**     | GPU memory used during training.                                                                        |

---

### Configurations Compared

1. **bf16 + SDPA (baseline)**

   * Step Time: 7.7s
   * Throughput: 68K tokens/sec
   * MFU: 27.5%
   * Memory: 105 GB

2. **FP8 + SDPA**

   * Step Time: 6.4s
   * Throughput: 82K tokens/sec
   * MFU: 33.1%
   * Memory: 92 GB
   * Using FP8 reduces memory footprint and speeds up training over bf16.

3. **FP8 + FA2 (SSSL)**

   * Step Time: 5.27s
   * Throughput: 99.5K tokens/sec
   * MFU: 36.4%
   * Memory: 92 GB
   * This combines FP8 precision **with FA2**, an optimized attention kernel (SSSL = Single-Shot Softmax + other improvements), giving the fastest speed and highest GPU utilization without increasing memory use.

---

### Speedup Analysis

* Compared to **bf16 baseline**:

  * **1.46× faster**
  * **+8.9% MFU**
  * Estimated training time drops from 62h → ~42.5h

* Compared to **FP8-only**:

  * **1.21× faster**
  * **+3.3% MFU**
  * Estimated training time drops from 52h → ~42.5h

---

### Summary

* **FA2 + FP8 is a game-changer**: it reduces step time, increases throughput, improves GPU efficiency, and keeps memory usage low.
* The biggest gains come from FA2’s optimized attention computation combined with FP8’s lower precision, which still maintains acceptable model accuracy while accelerating training.

---

References:

* [FlashAttention 2 GitHub](https://github.com/Dao-AILab/flash-attention)
* [FP8 Training in Deep Learning](https://arxiv.org/abs/2305.10822)
* [Mixed Precision Training](https://pytorch.org/docs/stable/amp.html)
