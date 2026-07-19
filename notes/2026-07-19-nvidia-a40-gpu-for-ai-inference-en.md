---
audio: false
generated: true
image: false
lang: en
layout: post
title: NVIDIA A40 GPU for AI Inference
translated: false
type: note
---

Question: What is the NVIDIA A40 GPU?

Answer: Ampere-architecture data center GPU (2020), positioned as a "prosumer/visual computing" card but commonly used for AI inference/fine-tuning since it's cheap-ish and has decent VRAM.

Key specs:
- Architecture: Ampere (GA102, same die family as RTX 3090)
- CUDA cores: 10,752
- Tensor cores: 336 third-generation Tensor Cores
- RT cores: 84 second-generation RT cores
- Memory: 48GB GDDR6 ECC memory
- FP32: double-rate vs prior gen — double-speed processing for single-precision floating point (FP32) operations
- Interconnect: NVLink to scale from 48GB to 96GB across two GPUs
- Bus: PCIe Gen4, passive cooling (server card, needs chassis airflow)
- No NVSwitch, no SXM — it's a PCIe-only card, unlike A100/H100

Where it fits for your use case:
- vs A100 (40/80GB HBM2e): A40 has way less memory bandwidth (~696 GB/s GDDR6 vs A100's ~1.5-2TB/s HBM2e), so it's much worse for large-batch training/inference throughput. Memory bandwidth is usually the bottleneck for LLM inference, not raw FLOPs.
- vs 3090 (24GB GDDR6X): A40 basically = 3090 die + double VRAM + ECC + passive cooling + NVLink, at a big price premium — you're paying for VRAM and reliability, not compute.
- Good for: fitting a 30B-ish model in bf16 for inference on a single card, or QLoRA fine-tuning where VRAM capacity matters more than bandwidth.
- Bad for: training throughput at scale — you'd get much better $/token on A100/H100 or even 4090 clusters if VRAM isn't the constraint.

Note: Lenovo's product guide already lists it as withdrawn from marketing — the NVIDIA A40 GPU is withdrawn from marketing — so it's EOL/cloud-inventory territory now, not something you'd buy new. Check current cloud pricing (RunPod/Lambda/Vast) before committing rather than buying hardware.

References:
- [NVIDIA A40 Data Center GPU](https://www.nvidia.com/en-us/data-center/a40/)
- [ThinkSystem NVIDIA A40 Product Guide](https://lenovopress.lenovo.com/lp1773-thinksystem-nvidia-a40-48gb-pcie-gen4-passive-gpu)
- [NVIDIA A40 R7E31A Specs](https://epoka.com/blogs/news/nvidia-a40-r7e31a-48gb-pcie-gpu-specs-performance-ai-workloads)
