---
audio: false
generated: true
image: false
lang: zh
layout: post
title: NVIDIA H200 GPU 规格与特性
translated: true
type: note
---

Question: What are the key specifications and features of the NVIDIA H200 GPU?

Answer: **NVIDIA H200** 是基于相同 **Hopper architecture** 构建的 H100 显存增强进化版。虽然它与其前代产品共享相同的核心计算引擎，但 H200 对其内存子系统进行了重大升级，使其成为第一款使用 **HBM3e** (High Bandwidth Memory 3e) 的 GPU。

### ## Key Technical Specifications

H200 的主要区别在于其显存容量和带宽的大幅提升，这直接解决了 Large Language Model (LLM) 推理和训练中的“内存墙”问题。

| Feature | NVIDIA H100 (SXM) | NVIDIA H200 (SXM) | Improvement |
| :--- | :--- | :--- | :--- |
| **Architecture** | Hopper (4nm) | Hopper (4nm) | - |
| **GPU Memory** | 80 GB HBM3 | **141 GB HBM3e** | **+76%** |
| **Memory Bandwidth** | 3.35 TB/s | **4.8 TB/s** | **+43%** |
| **FP8 Tensor Core** | 3,958 TFLOPS* | 3,958 TFLOPS* | Identical |
| **FP64 (Non-Tensor)** | 34 TFLOPS | 34 TFLOPS | Identical |
| **TDP (Power)** | 700W | 700W | Identical |
| **Interconnect** | NVLink 4.0 (900 GB/s) | NVLink 4.0 (900 GB/s) | Identical |

*\*Performance figures include sparsity.*

---

### ## Core Features & Innovations

* **HBM3e Memory:** 通过将 VRAM 增加至接近 H100 的两倍，H200 允许更大的模型（如 Llama 3 70B 甚至某些 175B 配置）容纳在更少的 GPU 中。这减少了对复杂模型并行化和 GPU 间通信的需求。
* **Transformer Engine:** 利用第 4 代 Tensor Cores 和智能软件动态管理精度（在 FP8 和 FP16 之间切换）。这在不牺牲准确性的情况下优化了基于 transformer 模型的吞吐量。
* **NVLink & NVSwitch:** 支持 900 GB/s 的双向带宽，实现在 8-GPU (HGX) 甚至大规模 SuperPOD 集群之间的无缝扩展。
* **Second-Generation MIG:** 允许将 GPU 划分为多达 **7 个独立实例**。由于 H200 拥有更大的内存，每个实例现在拥有约 **18 GB** 的专用 VRAM，使其在处理多租户企业工作负载时能力更强。

### ## Performance Impact

H200 专为在内存带宽是瓶颈的 **inference-heavy** 环境中表现出色而设计：

1. **LLM Inference:** 与 H100 相比，它在 Llama 2 70B 等模型上的性能提升高达 **1.9 倍**。
2. **Scientific Computing (HPC):** 对于内存密集型仿真（如 MILC 或天气建模），增加的带宽使其相比传统双路 CPU 系统实现了 **110 倍的加速**。
3. **TCO Efficiency:** 由于 H200 可以更高效地处理更大的 Batch Size 和更长的 Context Window，尽管初始硬件成本较高，但通常会降低生成每个 token 的总拥有成本 (TCO)。

---

Would you like me to compare the H200 specifically against the newer Blackwell B200 architecture?
