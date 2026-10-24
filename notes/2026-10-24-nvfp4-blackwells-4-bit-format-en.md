---
audio: false
generated: true
image: false
lang: en
layout: post
title: "NVFP4: Blackwell's 4-bit Format"
translated: false
type: note
---

**Question:** What is NVFP4 — an introduction?

**Answer:**

## What is NVFP4?

NVFP4 is an innovative 4-bit floating point format introduced with the NVIDIA Blackwell GPU architecture. It is designed specifically to maximize AI inference efficiency while preserving model accuracy.

---

### The Bit Layout

The base FP4 E2M1 format consists of 1 bit for the sign, 2 bits for the exponent, and 1 bit for the mantissa. This gives only 15 representable values — far fewer than FP8 or BF16 — making scaling strategies critical.

---

### The Key Innovation: Two-Level Scaling

Raw FP4 alone is too coarse to be useful. NVFP4 solves this with a two-tier scaling system:

1. **Block scale (FP8):** One FP8 (E8M0) scaling factor is shared for every 16 FP4 E2M1 values.
2. **Tensor scale (FP32):** An optional outer FP32 scale across multiple blocks enables two-level scaling on activations.

This gives 256 distinct scale values across the FP8 dynamic range, letting NVFP4 represent values that fall between MXFP4's power-of-2 grid points.

---

### How It Differs from MXFP4

MXFP4 is the multi-vendor consortium standard (OCP MX family). NVFP4 is NVIDIA's choice for Blackwell that the consortium did not adopt. The key difference: NVFP4 uses smaller blocks (16 elements) vs MXFP4's 32 elements, enabling finer-grained quantization. If you publish a model checkpoint quantized to NVFP4, AMD MI300 hardware will need to repack it to MXFP4 for native execution.

---

### Hardware Performance

Blackwell's NVFP4 Tensor Cores run at 2× the throughput of FP8 on the same hardware — and FP8 was already 2× BF16. So NVFP4 → FP8 → BF16 is a 4× → 2× → 1× throughput stair on B100/B200.

In production inference: peak throughput on Blackwell shows NVFP4 running at 3.0× relative to FP8.

Fifth-generation Tensor Cores provide native NVFP4 support with hardware-accelerated scaling, achieving 20 PetaFLOPS of FP4 performance.

---

### Accuracy

FP4 encodes each value in just sixteen levels. Until recently that was usable only for storage; with NVIDIA's NVFP4 format and Blackwell hardware, it now supports the full lifecycle of large models — training, inference, and even long-video generation — at close to 16-bit accuracy.

For example, on the MMLU benchmark, accuracy barely changes: MMLU drops only from 90.8% to 90.7% when quantizing from FP8 to FP4.

---

### Software Ecosystem

TensorRT Model Optimizer provides comprehensive FP4 quantization workflows, while frameworks like vLLM add early NVFP4 support. Pre-quantized checkpoints for models like DeepSeek-R1, Llama 3.1, and FLUX are also available on Hugging Face.

---

### Summary Table

| Feature | FP4 (E2M1) | MXFP4 | NVFP4 |
|---|---|---|---|
| Bit width | 4 | 4 | 4 |
| Block size | None | 32 | 16 |
| Block scale | None | FP8 (E8M0) | FP8 (E4M3) |
| Tensor scale | Optional | None | Optional FP32 |
| Accuracy | Lower | Medium | Higher |
| Hardware | Generic | Multi-vendor | Blackwell-native |

**References:**
- [Introducing NVFP4 for Efficient and Accurate Low-precision Inference (Edge AI & Vision)](https://www.edge-ai-vision.com/2025/07/introducing-nvfp4-for-efficient-and-accurate-low-precision-inference/)
- [NVFP4 Concept Reference — ZeroEntropy](https://www.zeroentropy.dev/concepts/nvfp4/)
- [The Impact of NVFP4 For LLM Inference — Nota AI](https://blog.nota.ai/insights/nvidia-blackwell-nvfp4)
- [Pushing Intelligence to 4-bit — NVIDIA Research](https://research.nvidia.com/labs/eai/blogs/pushing-intelligence-to-4-bit/)
- [Getting started with NVFP4 inference on NVIDIA DGX B200 — Macnica](https://www.macnica.co.jp/en/business/semiconductor/articles/nvidia/148013/)
