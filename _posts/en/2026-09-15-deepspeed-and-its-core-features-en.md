---
audio: false
generated: true
image: false
lang: en
layout: post
title: DeepSpeed and Its Core Features
translated: false
type: note
---

**Question:** What is DeepSpeed and what are its core features?

**Answer:**

**DeepSpeed** is a deep learning optimization library that makes distributed training and inference easy, efficient, and effective. It was developed by Microsoft and is open-source under the Apache 2.0 license.

**Core Innovations**

DeepSpeed's system innovations include several key technologies:

**ZeRO (Zero Redundancy Optimizer)** — The flagship memory optimization technique. It partitions optimizer states, gradients, and model parameters across GPUs to drastically reduce per-GPU memory usage. There are several variants:
- **ZeRO-Offload** — offloads optimizer states and gradients to CPU memory, enabling billion-scale training on fewer GPUs.
- **ZeRO-Infinity** — extends offloading to NVMe SSDs, breaking the GPU memory wall entirely.
- **ZeRO++** — reduces collective communication overhead for giant model training.

**3D Parallelism** — Combines three forms of parallelism simultaneously:
- Data Parallelism
- Tensor (Model) Parallelism
- Pipeline Parallelism

**Ulysses Sequence Parallelism** — Enables training on extremely long sequences (multi-million tokens).

**DeepSpeed-MoE** — Optimized training and inference for Mixture-of-Experts models.

**Communication Compression** — Techniques like 1-bit Adam and 1-bit LAMB reduce communication overhead during distributed training.

**Inference Optimizations** — DeepSpeed Inference accelerates transformer model serving at scale.

**Key Capabilities**

- Enabled the world's most powerful language models such as **MT-530B** and **BLOOM (176B)**.
- Supports NVIDIA, AMD, Intel Gaudi, Intel XPU, and Huawei Ascend NPU hardware.
- Integrates with popular frameworks: HuggingFace Transformers, Accelerate, PyTorch Lightning, MosaicML, and more.

**Installation**

```bash
pip install deepspeed
ds_report  # Check compatible features on your machine
```

**Recent highlights (2025–2026)**
- **ZenFlow** — Stall-free offloading engine for LLM training.
- **SuperOffload** — Large-scale LLM training on superchips (ASPLOS 2026 Honorable Mention).
- **DeepCompile** — Compiler optimizations for distributed training.
- **AutoTP** — Automatic Tensor Parallel training of HuggingFace models.

---

**References:**
- [DeepSpeed GitHub Repository](https://github.com/deepspeedai/DeepSpeed)
- [DeepSpeed Official Website](https://www.deepspeed.ai/)
- [API Documentation](https://deepspeed.readthedocs.io/en/latest/)
- [Getting Started Tutorial](https://www.deepspeed.ai/getting-started/)
