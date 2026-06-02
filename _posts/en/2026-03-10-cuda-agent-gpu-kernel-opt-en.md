---
audio: false
generated: true
image: false
lang: en
layout: post
title: CUDA Agent Optimizes GPU Kernels Better
translated: false
type: note
---

**Question:** What does CUDA Agent do, according to the paper from ByteDance?

**Answer:**

## CUDA Agent — Overview

CUDA Agent is a large-scale agentic reinforcement learning system developed by ByteDance Seed (in collaboration with Tsinghua University) that develops robust CUDA kernel optimization ability through scalable data synthesis, a skill-augmented execution environment, and stable long-horizon RL training.

---

## Core Problem It Solves

GPU kernel optimization is fundamental to modern deep learning but remains a highly specialized task requiring deep hardware expertise. Despite strong performance in general programming, large language models (LLMs) remain uncompetitive with compiler-based systems such as `torch.compile` for CUDA kernel generation. Existing CUDA code generation approaches either rely on training-free refinement or fine-tune models within fixed multi-turn execution-feedback loops, but both paradigms fail to fundamentally improve the model's intrinsic CUDA optimization ability.

---

## Three Core Components

### 1. Scalable Data Synthesis

Training tasks are built with a three-stage pipeline: seed problem crawling, LLM-based combinatorial synthesis, and execution-driven filtering. Seed operators are mined from `torch` and `transformers`, each represented as a Python class with initialization and forward methods. Combinatorial synthesis samples up to 5 torch operators and composes them sequentially into fused tasks. The final curated dataset contains 6,000 training samples (CUDA-Agent-Ops-6K), designed for scalable RL training with broad task diversity and reduced contamination risk.

### 2. Skill-Augmented Agent Environment

The agent loop follows a ReAct-style workflow with coding tools and a CUDA skill specification (SKILL.md), enabling iterative coding, compile-debug cycles, and profiler-guided optimization. The standard workflow is: profile native PyTorch, implement CUDA kernels/bindings, compile in GPU sandbox, then iterate. The target requirement is to pass correctness checks and exceed a 5% speedup over `torch.compile`.

The agent is given tools including BashTool, GlobTool, MultiEditTool, and TodoWriteTool, and runs in a four-stage loop: analyze performance of the native PyTorch implementation, implement custom CUDA operators by rewriting the model, compile and evaluate in a GPU sandbox environment, and repeat until achieving a 5% speedup over the `torch.compile` baseline.

### 3. Stable Long-Horizon RL Training

Training is staged to stabilize long-horizon RL for CUDA coding. It first runs single-turn PPO warm-up, then initializes both actor and critic before full multi-turn agentic RL. Actor initialization uses Rejection Fine-Tuning (RFT) on sampled trajectories with positive outcomes. RFT filtering removes inefficient loops and invalid tool-call patterns to reduce policy collapse risk. With this multi-stage design, training remains stable for long-context settings (up to 128k context, 150 training turns, and up to 200 turns during evaluation), enabling sustained reward growth.

---

## The Base Model

CUDA Agent is a fine-tuned version of ByteDance's Seed 1.6 LLM, a Mixture-of-Experts (MoE) model with 23B active parameters and 230B total parameters. Fine-tuning took place on a cluster of 128 NVIDIA H20 GPUs.

---

## Key Results

CUDA Agent achieves state-of-the-art results on KernelBench, delivering 100%, 100%, and 92% faster rate over `torch.compile` on Level-1, Level-2, and Level-3 splits, with an overall pass rate of 98.8% and an overall 2.11x speedup vs. `torch.compile`.

The 40-point gap over Claude Opus 4.5 and Gemini 3 Pro on complex kernels suggests that general-purpose coding ability is necessary but insufficient for GPU optimization — you need domain-specific RL on hardware-grounded rewards.

---

## Why It Matters

The key move is obvious in hindsight: if you want a model to generate fast code, reward it for creating fast code — not correct code, not code that looks like good code, but code that the profiler says is fast. The 2.11x speedup over `torch.compile` matters because `torch.compile` is the default optimization path for most PyTorch users. If an RL-trained agent can consistently beat the compiler on the same hardware, it opens a path toward AI-produced kernels replacing hand-tuned operator libraries in production.

---

**References:**

- [CUDA Agent Official Project Page](https://cuda-agent.github.io/)
- [HuggingFace Paper Page](https://huggingface.co/papers/2602.24286)
- [Awesome Agents — ByteDance CUDA Agent Breakdown](https://awesomeagents.ai/news/cuda-agent-bytedance-kernel-generation/)
- [Import AI Newsletter Coverage](https://importai.substack.com/p/import-ai-448-ai-r-and-d-bytedances)
