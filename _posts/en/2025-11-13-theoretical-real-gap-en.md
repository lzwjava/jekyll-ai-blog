---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: The Gap Between Theoretical and Real Performance
translated: false
type: note
---

The discrepancy arises because **theoretical peak FLOPS** (floating-point operations per second) measures raw arithmetic throughput under ideal conditions—assuming perfect utilization of all execution units, no memory bottlenecks, and infinite bandwidth. In real workloads (especially AI/training/inference), performance is gated by **memory subsystem inefficiencies**, not just compute. The 2010 Fermi GPUs (e.g., GTX 480) were particularly bad at this, inflating the "expected" gap when compared to modern cards like the RTX 4090.

### Key Reasons Fermi Underutilized Its Theoretical FLOPS

1. **Poor Cache Hierarchy and Memory Coalescing**
   - Fermi had only 64 KB L1 cache per SM (shared with registers) and a tiny 768 KB L2 (entire chip).
   - No proper cache coherence; global memory accesses were uncoalesced → **~10–30% effective bandwidth** in real kernels.
   - Modern GPUs (Ampere/Ada) have **massive L1 (192 KB/SM)**, **dedicated texture caches**, and **aggressive prefetching**, achieving 70–90% of theoretical BW.

2. **High Latency, Low Bandwidth ECC DDR5/GDDR5**
   - Fermi: ~170 GB/s GDDR5, **384-bit bus but ECC overhead** → effective ~130 GB/s.
   - RTX 4090: **1 TB/s GDDR6X**, 384-bit but **no ECC tax in consumer mode**, plus **better compression**.
   - Real AI kernels are **memory-bound** (e.g., GEMM with large matrices); FLOPS don't matter if data stalls.

3. **Inefficient Register File and Warp Scheduling**
   - Fermi: 32k 32-bit registers/SM → **max 1536 threads** but only **~50% occupancy** in practice due to register spilling.
   - Ada: 256 KB register file → **2048 threads/SM**, near-100% occupancy.
   - Less divergence, better ILP extraction.

4. **Power/Thermal Throttling**
   - GTX 480: 250 W TDP, **throttled hard under sustained load** (clocks dropped 10–20%).
   - RTX 4090: 450 W but **~3x better perf/W** via 4nm process, DLSS, and dynamic boosting.

### Measured Real-World Gains (AI Workloads)

| Metric | GTX 480 (Fermi, 2010) | RTX 4090 (Ada, 2022) | Speedup |
|--------|------------------------|----------------------|---------|
| FP32 TFLOPS (peak) | 1.35 | 82.6 | **61x** |
| FP16 TFLOPS (peak) | ~0.7 (emulated) | 330 (Tensor) | **>400x** |
| **ResNet-50 Training (img/s)** | ~60 | ~1,050 | **~17x** |
| **GPT-2 Inference (tokens/s)** | ~8 | ~140 | **~17x** |
| **Stable Diffusion (it/s)** | <0.1 | ~1.6 | **>16x** |

*Sources: NVIDIA papers, MLPerf benchmarks, AnandTech.*

### Bottom Line

Theoretical FLOPS assumed Fermi could sustain ~70% utilization—it couldn't (real ~15–25%). Modern architectures close that gap to **~70–90%**, so **effective compute scales closer to Moore's Law + arch improvements** (~10–17x over 12 years), not the 60x+ peak FLOPS suggest. The rest is "paper performance."
