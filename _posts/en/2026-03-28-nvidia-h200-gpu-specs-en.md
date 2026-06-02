---
audio: false
generated: true
image: false
lang: en
layout: post
title: NVIDIA H200 GPU Specifications and Features
translated: false
type: note
---

Question: What are the key specifications and features of the NVIDIA H200 GPU?

Answer: The **NVIDIA H200** is the memory-enhanced evolution of the H100, built on the same **Hopper architecture**. While it shares the same core compute engine as its predecessor, the H200 introduces significant upgrades to its memory subsystem, making it the first GPU to utilize **HBM3e** (High Bandwidth Memory 3e).

### ## Key Technical Specifications
The H200 is primarily differentiated by its massive jump in memory capacity and bandwidth, which directly addresses the "memory wall" in Large Language Model (LLM) inference and training.

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
* **HBM3e Memory:** By nearly doubling the VRAM compared to the H100, the H200 allows larger models (like Llama 3 70B or even certain 175B configurations) to fit within fewer GPUs. This reduces the need for complex model parallelism and inter-GPU communication.
* **Transformer Engine:** Utilizes 4th Gen Tensor Cores and intelligent software to dynamically manage precision (switching between FP8 and FP16). This optimizes throughput for transformer-based models without sacrificing accuracy.
* **NVLink & NVSwitch:** Supports 900 GB/s of bidirectional bandwidth, enabling seamless scaling across 8-GPU (HGX) or even massive SuperPOD clusters.
* **Second-Generation MIG:** Allows the GPU to be partitioned into up to **7 isolated instances**. With the H200's larger memory, each instance now has roughly **18 GB** of dedicated VRAM, making it much more capable for multi-tenant enterprise workloads.



### ## Performance Impact
The H200 is specifically designed to excel in **inference-heavy** environments where memory bandwidth is the bottleneck:
1.  **LLM Inference:** It delivers up to **1.9x faster** performance on models like Llama 2 70B compared to the H100.
2.  **Scientific Computing (HPC):** For memory-intensive simulations (like MILC or weather modeling), the increased bandwidth translates to a **110x speedup** over traditional dual-socket CPU systems.
3.  **TCO Efficiency:** Because the H200 can handle larger batches and longer context windows more efficiently, it often results in a lower Total Cost of Ownership (TCO) per token generated, despite the higher initial hardware cost.

---

Would you like me to compare the H200 specifically against the newer Blackwell B200 architecture?
