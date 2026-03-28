---
audio: false
generated: true
image: false
lang: en
layout: post
title: Choosing ECS Instances for Model Training
translated: false
type: note
---

**Question:** How do I choose the right ECS instance type detail (such as `ecs.vgn7i`) and its sub-sizes for model training on Alibaba Cloud?

**Answer:**

## Understanding the ECS Instance Type Naming Convention

Each instance type name follows the format `ecs.<Instance family>.<Instance size>`. The `<Instance size>` part represents the number of vCPUs: `small` = 1 vCPU, `large` = 2 vCPUs, `xlarge` = 4 vCPUs, and `<n>xlarge` = n × 4 vCPUs. For example, `2xlarge` = 8 vCPUs, `8xlarge` = 32 vCPUs.

---

## What is `ecs.vgn7i`?

`vgn7i` uses the latest Intel Ice Lake processors and NVIDIA A30 GPUs based on the NVIDIA Ampere architecture. If you want exclusive CPU resources, choose the `vgn7i-vws` instance family. This family includes an NVIDIA GRID vWS license and provides certified graphics acceleration for CAD software, while also serving as a lightweight GPU-accelerated instance for small-scale AI inference.

**Key point:** `vgn7i` provides **virtual GPUs (vGPU)**, meaning the GPU is sliced and shared — not a dedicated full GPU. Each GPU can be sliced into multiple partitions, and each partition is allocated as a vGPU to an instance. For example, `NVIDIA A10 * 1/6` means one GPU is sliced into six partitions, and each instance gets one partition.

---

## GPU Instance Families Compared — Which to Choose for Training?

| Instance Family | GPU | Full GPU? | Best For |
|---|---|---|---|
| `ecs.vgn7i` | NVIDIA A30 (sliced) | ❌ vGPU (shared) | Small inference, CAD, remote desktop |
| `ecs.gn7i` | NVIDIA A10 | ✅ Full GPU | Medium model training, inference |
| `ecs.gn7` | NVIDIA A100 | ✅ Full GPU | Large model training |
| `ecs.gn8` (Bare Metal) | NVIDIA H100/H800 | ✅ Full GPU × 8 | LLM training (70B+ parameters) |

The gn8 bare metal family is designed specifically for AI model training and ultra-large models. Each instance has eight GPUs, with each GPU equipped with 96 GB of HBM3 memory delivering up to 4 TB/s memory bandwidth, which greatly accelerates model training and inference.

---

## How to Choose the Right Sub-Size (e.g., `xlarge`, `4xlarge`, `8xlarge`)

Follow this decision process:

### Step 1 — Decide your GPU count need
- **1 vGPU / small experiments** → `ecs.vgn7i-[size].xlarge` (4 vCPU)
- **1 full GPU / medium training** → `ecs.gn7i-c8g1.2xlarge`
- **Multi-GPU / large training** → `ecs.gn7-c13g1.13xlarge` or bare metal `ecs.ebmgn8`

### Step 2 — Match vCPU and memory to your data pipeline
The instance size (xlarge, 2xlarge, etc.) controls vCPU and RAM, not just GPU count. More vCPUs help with:
- Data preprocessing
- Multi-worker DataLoader (PyTorch/TF)
- Serving multiple GPU streams

### Step 3 — Consider your budget
- `vgn7i` series → cheapest (shared/sliced GPU), suitable for inference and light fine-tuning
- `gn7i` / `gn7` → mid-range, good for full model training
- `gn8` bare metal → most expensive, for production-scale LLM training

### Step 4 — Check regional availability
Instance types available for purchase vary by region. You can visit the Instance Types Available for Each Region page to check availability, or use the ECS Price Calculator to estimate costs.

---

## Quick Recommendation Summary

| Your Task | Recommended Instance |
|---|---|
| Fine-tuning small models (< 1B params) | `ecs.gn7i-c8g1.2xlarge` (1× A10 GPU) |
| Training medium models (1B–7B params) | `ecs.gn7i-c16g1.4xlarge` or `gn7` |
| Training large models (7B–70B params) | `ecs.gn7-c13g1.13xlarge` (8× A100) |
| LLM training (70B+ params) | `ecs.ebmgn8` bare metal (8× H100) |
| Light inference / CAD / remote GPU | `ecs.vgn7i-*` (vGPU, cheapest) |

**Bottom line:** `ecs.vgn7i` is **not ideal for serious model training** because it uses virtual/shared GPUs. For actual training, pick from the `gn7i`, `gn7`, or `gn8` families instead, and choose the sub-size based on how many vCPUs your data pipeline needs.

**References:**

- [Alibaba Cloud vGPU Instance Families (vgn7i)](https://www.alibabacloud.com/help/en/egs/vgpu-accelerated-instance-families)
- [GPU Compute-Optimized Instance Families (gn series)](https://www.alibabacloud.com/help/en/egs/gpu-accelerated-compute-optimized-instance-families)
- [ECS Instance Naming and Classification](https://www.alibabacloud.com/help/en/ecs/user-guide/instance-specification-naming-and-classification)
- [ECS Instance Families Overview](https://www.alibabacloud.com/help/en/ecs/user-guide/overview-of-instance-families)