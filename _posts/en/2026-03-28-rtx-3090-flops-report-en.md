---
audio: false
generated: true
image: false
lang: en
layout: post
title: RTX 3090 Theoretical FLOPS Performance Report
translated: false
type: note
---

Question: How's the FLOPS performance of the RTX 3090 in this server hardware report?

Answer:

The RTX 3090 in your server has the following theoretical peak FLOPS performance based on its GA102 GPU architecture:

- **FP32 (Single Precision)**: Approximately 35.6 TFLOPS
- **FP16 (Half Precision)**: Approximately 142 TFLOPS (using Tensor Cores)

These numbers represent the raw theoretical maximum compute performance of the card. In real-world usage, actual achieved FLOPS will be lower depending on the workload, cooling, power limits, and software optimization.

### Quick Breakdown

- **FP32 FLOPS (~35.6 TFLOPS)**: This is the standard single-precision floating-point performance. It's solid for general-purpose computing, gaming, and many scientific simulations, though it's not the absolute highest compared to modern datacenter GPUs like the A100 or H100.
- **FP16 / Tensor Core FLOPS (~142 TFLOPS)**: This is where the RTX 3090 really shines for machine learning inference and training. The Tensor Cores provide a massive boost for half-precision and mixed-precision workloads (common in AI models). This makes it particularly strong for running large language models or computer vision tasks at high throughput.

### Context for Your Setup

Your server has a capable Intel Xeon Platinum 8369B CPU with full AVX-512 support (including VNNI), which pairs well with the GPU for hybrid CPU+GPU workloads. With 91 GiB of system RAM (nearly all free), memory isn't a bottleneck right now.

The main blocker right now is the missing NVIDIA driver. Until the driver is installed and `nvidia-smi` works, you won't be able to utilize the GPU's FLOPS at all — CUDA applications simply won't see the hardware.

**Recommendation**:
Yes, installing the NVIDIA driver is the next step. Once installed, you can run benchmarks like `nvidia-smi` to confirm the GPU is healthy, then test real performance with tools like TensorFlow/PyTorch benchmarks or CUDA samples to see sustained FLOPS in practice.

If you want, I can provide commands to install the latest compatible NVIDIA driver for your Linux setup (assuming it's a common distro like Ubuntu or CentOS on the Alibaba ECS instance).

References:

- NVIDIA GeForce RTX 3090 official specifications (theoretical TFLOPS values)
