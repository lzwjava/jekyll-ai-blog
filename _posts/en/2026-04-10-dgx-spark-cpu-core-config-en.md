---
audio: false
generated: true
image: false
lang: en
layout: post
title: DGX Spark CPU Core Configuration
translated: false
type: note
---

Question: What is the new NVIDIA DGX OS from last month, and in the context of NVIDIA's DGX Spark or similar systems, do the numbers for "10 Cortex" and "10 Cortex in CPU" have to match? What do they respectively mean?

Answer: 

NVIDIA DGX OS is a customized Linux distribution (based on Ubuntu) designed specifically for NVIDIA DGX systems. It comes pre-installed with optimized drivers, the full NVIDIA AI software stack (including CUDA, cuDNN, TensorRT, and more), diagnostic tools, and platform-specific tweaks for stable, high-performance AI, machine learning, and analytics workloads. Recent releases, such as DGX OS 7.x versions, support the latest hardware like the DGX Spark. It is essentially a tuned version of Ubuntu Linux with NVIDIA enhancements baked in for better compatibility and performance on their Grace Blackwell-based platforms.

The "10 Cortex" and "10 Cortex in CPU" you mentioned refer to the CPU configuration in the **NVIDIA DGX Spark** (also known as the GB10 Grace Blackwell Superchip system), a compact desktop AI supercomputer released around early 2025–2026. This is not a generic "10 Cortex" but specifically:

- **10 Cortex-X925 cores**: These are high-performance (big) Arm Cortex-X925 CPU cores. They are designed for maximum single-threaded and multi-threaded performance, handling demanding tasks like AI data preprocessing, orchestration, tokenization, model fine-tuning, and heavy computational workloads. They run at higher clock speeds and deliver the "heavy lifting" in the system.

- **10 Cortex-A725 cores**: These are high-efficiency (little) Arm Cortex-A725 CPU cores. They focus on power efficiency and lighter background or parallel tasks, helping with overall system orchestration, smaller workloads, and reducing power consumption while the big cores handle intensive jobs.

Together, they form a **20-core Armv9 hybrid (big.LITTLE) CPU** in the Grace part of the GB10 Superchip. The CPU shares 128 GB of unified LPDDR5x memory with the integrated Blackwell GPU. This big.LITTLE design is common in modern Arm-based processors (like those in smartphones or high-end SoCs) to balance performance and efficiency.

The numbers **do not have to be identical** in general Arm big.LITTLE designs — many configurations use uneven splits (e.g., 8 big + 4 little). However, in the specific DGX Spark / GB10 design, NVIDIA chose a balanced **10 + 10** split for optimal AI workloads on a desktop-scale system. This provides strong performance without excessive power draw or heat in a compact form factor.

In short:
- The two "10"s refer to the count of each type of core in this particular 20-core Arm CPU.
- Cortex-X925 = performance-focused cores.
- Cortex-A725 = efficiency-focused cores.

This setup pairs with a powerful Blackwell GPU (up to 1 petaFLOP AI performance at FP4), making the DGX Spark suitable for local AI development, running large models (up to ~200B parameters), inference, and robotics/computer vision tasks.

If you're seeing this in system specs, logs, or `lscpu`/`cat /proc/cpuinfo` output on a DGX Spark running DGX OS, that's exactly what it describes.

References:  
- https://docs.nvidia.com/dgx/dgx-spark/hardware.html  
- https://www.nvidia.com/en-us/products/workstations/dgx-spark/  
- https://newsroom.arm.com/blog/arm-nvidia-dgx-spark-high-performance-ai