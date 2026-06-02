---
audio: false
generated: true
image: false
lang: en
layout: post
title: Alibaba Instance GPU FLOPS Details
translated: false
type: note
---

Question: What is the FLOPS of Alibaba Cloud ECS instance ecs.gn7t-c16g1.4xlarge?

Answer:

The Alibaba Cloud **ecs.gn7t-c16g1.4xlarge** is a GPU-accelerated instance with the following key specifications:

- **vCPUs**: 16
- **Memory (RAM)**: 94 GiB (approximately 96 GB)
- **GPU**: 1 × NVIDIA G39 with 24 GB VRAM
- **Network bandwidth**: Up to 8 Gbps (depending on region and configuration)

**FLOPS performance** for this instance is not directly published by Alibaba Cloud in their standard documentation or instance family tables. The "G39" appears to be an internal or region-specific NVIDIA GPU designation used by Alibaba (likely a variant or rebranded/customized card based on Turing/Ampere/Ada architecture families, similar to how other gn7-series use A10 or A30 GPUs).

Without an official FLOPS rating from Alibaba or NVIDIA for the exact "G39" model, a precise number cannot be confirmed. Comparable GPUs in Alibaba's gn7 series (such as A10) typically deliver:

- **FP32 (single-precision)**: Around 30–60 TFLOPS per GPU
- **FP16/Tensor (mixed-precision)**: Significantly higher, often 100+ TFLOPS with Tensor Cores

For the most accurate and up-to-date FLOPS details, check:

- The official Alibaba Cloud ECS console or instance type selector in your region.
- Alibaba Cloud documentation for the gn7t family.
- Contact Alibaba Cloud support for the specific GPU compute performance metrics.

If you have access to the instance, you can run benchmarks like NVIDIA's `nvidia-smi` combined with tools such as `cuda-samples` or MLPerf to measure real-world TFLOPS.

References:

- <https://pcr.cloud-mercato.com/providers/alibaba/flavors/ecs.gn7t-c16g1.4xlarge>
- <https://sparecores.com/server/alicloud/ecs.gn7t-c16g1.4xlarge>
- <https://www.alibabacloud.com/help/en/ecs/user-guide/gpu-accelerated-compute-optimized-and-vgpu-accelerated-instance-families-1>
