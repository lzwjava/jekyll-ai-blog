---
audio: false
generated: true
image: false
lang: en
layout: post
title: "GTX 1060: A Decade-Old GPU"
translated: false
type: note
---

**Question:** What is the GTX 1060 GPU?

**Answer:**

The NVIDIA GeForce GTX 1060 is a mid-range consumer GPU from July 2016, built on the Pascal architecture (GP106 die, 16nm TSMC). It was one of the most popular gaming cards ever — it topped the Steam hardware survey for years.

Key specs (6GB variant):

| Spec | Value |
|------|-------|
| Architecture | Pascal (GP106) |
| CUDA cores | 1280 |
| VRAM | 6 GB GDDR5 (there's also a cut-down 3GB variant with 1152 cores) |
| Memory bandwidth | 192 GB/s (192-bit bus) |
| FP32 | ~4.4 TFLOPS |
| TDP | 120 W |
| Compute capability | 6.1 |

From an ML perspective — the lens that matters for you:

- **No Tensor Cores.** Those arrived with Volta/Turing. So no hardware-accelerated mixed precision; FP16 on Pascal consumer cards runs at roughly FP32 speed (FP16 throughput was deliberately crippled on GP106/GP104).
- **6 GB VRAM** is tight but workable for toy training. You could run nanoGPT's Shakespeare char-level model or small GPT-2 (124M) with small batch sizes and gradient accumulation. GPT-2 760M like you trained on the MI300X — not a chance without aggressive offloading.
- **Compute capability 6.1** means modern stacks are dropping it: recent PyTorch builds still work, but FlashAttention requires sm_80+ (Ampere), and Triton kernels increasingly assume Ampere+. It's on the deprecation path in CUDA 12.x tooling.
- Rough comparison to your RTX 4070: the 4070 has ~7x the FP32 throughput (29 TFLOPS), Tensor Cores with FP16/BF16/FP8 support, 12 GB, and ~504 GB/s bandwidth. A 1060 is basically a decade behind for training workloads.

Quick check if you encounter one:

```bash
nvidia-smi --query-gpu=name,memory.total,compute_cap --format=csv
python -c "import torch; print(torch.cuda.get_device_capability())"  # (6, 1)
```

Bottom line: fine for old games and inference of small quantized models (a 3B model at Q4 fits in 6 GB via llama.cpp), but not worth buying in 2026 for ML — used market ~$60-80, and even a used RTX 3060 12GB is a far better value for local inference.
