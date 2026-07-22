---
audio: false
generated: true
image: false
lang: en
layout: post
title: "DeepSpeed: Extreme Scale DL Training"
translated: false
type: note
---

## DeepSpeed — Microsoft's DL Training Optimization Library

You're in the DeepSpeed repo (by Microsoft/DeepSpeedAI). It's the system that trained **MT-530B** and **BLOOM** — at the time, the world's largest language models.

**Core mission**: Extreme speed and scale for deep learning training on PyTorch.

**Key innovations**:

- **ZeRO** (Zero Redundancy Optimizer) — shards optimizer states, gradients, and parameters across GPUs instead of replicating them. The current branch has ZeRO-3 with SDMA (System DMA) offload for AMD GPUs.
- **ZeRO-Infinity** — offload to CPU/NVMe, enabling training beyond GPU memory capacity
- **3D-Parallelism** — data parallel + pipeline parallel + tensor parallel
- **DeepSpeed-MoE** — Mixture of Experts training support
- **Ulysses Sequence Parallelism** — long-context LLM training
- **DeepCompile** — compiler optimization for distributed training
- **ZenFlow** — stall-free offloading engine
- **SuperOffload** — ASLPOS 2026 Honorable Mention, offloading on superchips

**Why you'd use it**: When you need to train a model that doesn't fit on a single GPU. DeepSpeed handles the distributed systems complexity so you write standard PyTorch forward/backward and let it manage sharding, communication, and memory.

**Recent stuff** (2026): Muon optimizer support, SDMA for ZeRO-3 collectives, SuperOffload for superchips, DeepSpeed Core API with PyTorch-style backward.

You're on branch `master`, clean, with two recent ZeRO fixes committed. The project uses `setup.py`/`setup.cfg` + `pre-commit` (yapf+flake8). If you're looking at this repo, you're probably interested in how large-scale distributed training works under the hood — ZeRO's gradient bucketing, pipeline scheduling, or communication overlap.
