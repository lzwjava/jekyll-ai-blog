---
audio: false
generated: true
image: false
lang: en
layout: post
title: Memory Bottleneck in Large Language Models
translated: false
type: note
---

**Question:** Why is memory (and unified memory) so critical for LLM training and inference?

**Answer:**

The fundamental reason is **compute-to-memory bandwidth mismatch**. Modern GPUs/accelerators have vastly more compute than memory bandwidth, so the bottleneck during LLM training/inference is almost always memory movement, not math.

## The Core Problem

A GPU like RTX 4070 or MI300X can perform ~teraFLOPS of compute, but memory bandwidth is limited:

| Device | Peak Compute | Memory BW | Compute:BW Ratio |
|--------|--------------|-----------|------------------|
| RTX 4070 | ~29 TF32-TFLOPS | 432 GB/s | ~67 |
| MI300X | ~360 TFLOPS (FP8) | 5.3 TB/s | ~68 |

To keep the GPU busy, you need to move data in and out of memory **fast enough to feed the compute units**.

If you have 67 bytes of data per FLOP, and compute takes 1 nanosecond per FLOP, you need 67 bytes * 1 ns = 67 ns of memory latency tolerance. GDDR6 can't sustain that. **HBM (High Bandwidth Memory) exists specifically to solve this**: HBM3 on MI300X gives you 5.3 TB/s vs GDDR6's ~400 GB/s—**10x more bandwidth**.

## Training: Activation Memory Explodes

During forward pass, you must keep all intermediate activations in memory for the backward pass. For a transformer:

```
Activation memory = batch_size × seq_len × hidden_dim × num_layers × bytes_per_param

Example (13B model, bsz=1, seq=4096):
= 1 × 4096 × 5120 × 40 × 2 bytes (fp16)
≈ 1.6 GB just for activations, per layer
× 40 layers ≈ 64 GB
```

This is **linear in sequence length**. Longer context = more memory needed. This is why:

- Flash Attention minimizes this by fusing kernels (no intermediate storage)
- Gradient checkpointing trades compute for memory (recompute activations, don't store them)
- You need HBM or large VRAM just to fit standard training

## Inference: KV Cache Dominates

During inference, you cache key/value vectors to avoid recomputing attention:

```
KV cache size = batch_size × seq_len × hidden_dim × 2 × num_layers × bytes

For 13B model, bsz=32, seq=4096:
= 32 × 4096 × 5120 × 2 × 40 × 2 bytes (fp16)
≈ 52 GB
```

This scales **quadratically** with sequence length and batch size. If you want to serve 128 concurrent users with 8K context, you need massive memory. This is why:

- Quantization (int8/fp8) reduces KV cache size by 50-75%
- MQA (Multi-Query Attention) reduces KV cache by num_heads factor
- You're memory-bound, not compute-bound, during inference

## Why Unified Memory Matters

NVIDIA's Unified Memory Architecture (UVA) allows CPU and GPU to access the same virtual address space, with automatic paging between them. This sounds great but has a critical flaw:

**Paging is slow.** If activations spill to system RAM, you're moving data over PCIe (16 GB/s on PCIe 4.0) instead of HBM (5.3 TB/s). You lose 300x bandwidth.

However, unified memory is useful for:

- **Grad accumulation workflows** where you move data explicitly with fine control
- **CPU-GPU heterogeneous compute** (rare in LLM training)
- **Dynamic memory management** where you don't know sizes ahead of time

For pure LLM training, you're better off with **explicit memory management** (allocate on GPU, keep it there) than relying on unified memory's automatic paging.

## Practical For Your Situation

**MI300X (192 GB HBM3):** You can train larger models in full precision and fit larger batches because of the huge bandwidth and capacity. This is why it's so strong for 760M GPT-2 training—you have headroom.

**RTX 4070 (12 GB VRAM):** You're constrained. For serious work, you need:

- Mixed precision (fp16/tf32)
- Gradient checkpointing
- Smaller batch sizes or sequence lengths
- Quantization (QLoRA for fine-tuning)

**Optimization priorities:**

1. **Minimize data movement** (fused kernels, Flash Attention)
2. **Use the fastest memory available** (HBM > GDDR6 > system RAM)
3. **Right data types** (fp8/int8 KV cache for inference, fp16 for training)
4. **Batch size tuning** (maximize GPU utilization without exceeding memory)

The unified memory rabbit hole: modern inference engines (vLLM, TensorRT) manage this explicitly instead of relying on automatic paging—they know the memory access patterns and prefetch strategically.
