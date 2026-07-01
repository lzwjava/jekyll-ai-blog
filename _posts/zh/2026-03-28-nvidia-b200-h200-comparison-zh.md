---
audio: false
generated: true
image: false
lang: zh
layout: post
title: NVIDIA B200 与 H200 对比指南
translated: true
type: note
---

Question: B200 vs H200: Memory Performance and Key Differences

Answer: The transition from the **Hopper** (H200) to the **Blackwell** (B200) architecture represents a massive leap in memory bandwidth and raw compute power, specifically designed to handle trillion-parameter models.

### **Core Specifications Comparison**

| Feature | NVIDIA H200 (Hopper) | NVIDIA B200 (Blackwell) | Improvement |
| :--- | :--- | :--- | :--- |
| **Architecture** | Hopper | Blackwell (Dual-Die) | Generational Leap |
| **Memory Capacity** | 141 GB HBM3e | 180 GB - 192 GB HBM3e | ~30% - 36% Increase |
| **Memory Bandwidth** | 4.8 TB/s | 8.0 TB/s | **1.67x Faster** |
| **NVLink Speed** | 900 GB/s (v4) | 1.8 TB/s (v5) | **2x Faster** |
| **TDP (Power)** | 700W | 1000W - 1200W | ~40% - 70% Higher |
| **Transistors** | 80 Billion | 208 Billion | **2.6x Density** |

---

### **Memory Performance & Architecture**

**B200** 不仅仅是一个更大的芯片；它采用了 **dual-die design**，通过高速互连 (10 TB/s) 连接，使其表现得像一个单一的统一 GPU。

* **Bandwidth Breakthrough:** 达到 **8.0 TB/s** 的 B200 旨在防止“memory starvation”，即计算核心因等待数据而处于闲置状态。这对于 Large Language Model (LLM) 的 inference 至关重要，因为 memory bandwidth 通常是主要的瓶颈。
* **HBM3e Utilization:** 两者都使用 HBM3e，但 B200 配备了 8 个 HBM3e 堆栈（每个 24GB）。这允许显著增加 KV (Key-Value) caches，从而直接支持 Llama 3 或 GPT-4 等模型中更长的 **context windows**。
* **Capacity for Trillion-Parameter Models:** 192GB 的容量使更大的模型能够完全保留在 GPU memory 中，减少了通过网络进行较慢的 multi-GPU 通信的需求。

### **Compute & Efficiency**

* **FP4 Support:** B200 引入了 **FP4 (4-bit Floating Point)** 精度。虽然 H200 在 FP8 方面表现出色，但 B200 的 FP4 能力使其在某些工作负载下的 **inference performance** 达到上一代的 **15 倍**。
* **The Power Trade-off:** B200 在功耗方面是一个“怪兽”，在某些配置下功耗高达 **1,200W**。虽然它的 per-token 效率更高，但与 H200 700W 的风冷友好设计相比，它需要更强大的冷却基础设施（通常是 liquid cooling）。

### **Which one to choose?**

* **选择 H200：** 如果你拥有专为 700W 设计的现有 HGX/SXM 基础设施，或者你的模型可以轻松适应 141GB，并且你优先考虑较低的初始 TCO 和功耗。
* **选择 B200：** 如果你正在 training 或 serving 前沿模型（1T+ parameters），需要实时应用中尽可能低的 latency，或者需要在新数据中心最大化性能密度。

你想让我调查特定模型（如 Llama 3 或 DeepSeek）在这两款芯片上的具体 performance benchmarks 吗？
