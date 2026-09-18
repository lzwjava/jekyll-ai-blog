---
audio: false
generated: true
image: false
lang: en
layout: post
title: Edge0-35B-A3B-preview on-device MoE
translated: false
type: note
---

**Question:** What is the model at <https://huggingface.co/Edge0/Edge0-35B-A3B-preview>?

**Answer:**

**Edge0-35B-A3B-preview** is a sparse Mixture-of-Experts (MoE) language model designed specifically for **edge / on-device inference** — its headline feature is running a 35B-parameter model in under **3 GiB of active memory**.

Here's a breakdown of what makes it notable:

**Architecture & Base**
It is built on top of **Qwen3.6-35B-A3B** as the base model, with 40 layers, 256 experts (4 active per token), and a hidden size of 2048.

**Key Innovations**
The model uses three techniques to achieve low memory usage at usable speeds:

1. **SSD Expert Offload** — expert weights are streamed from storage on demand, so RAM only holds the currently active weights rather than the entire model.
2. **Prerouter** — a trained head predicts expert routing one step ahead, so expert loads overlap the forward pass instead of stalling it, delivering up to +59% decode throughput.
3. **Recover-LoRA** — the int4 base is frozen and LoRA adapters are trained via distillation from the FP16 teacher, recovering most quantization loss at 4-bit.

**Performance (on Mac mini M4 Pro)**
Decode speed is 14.9–17.7 tok/s, prefill throughput is 113–140 tok/s, and peak active memory is just **2.9 GiB**.

**Quality**
The int4 + adapter pipeline loses only **3.9 points on average** versus the fp16 base model, scoring 86.6 on AIME 2026, 90.9 on HumanEval, and 79.8 on GPQA-Diamond.

**Limitations**
This is a preview release — agent capabilities (tool use, multi-step planning) are currently weak, and the MLX backend currently targets **Apple Silicon** only.

**References:**

- [Edge0/Edge0-35B-A3B-preview — Hugging Face](https://huggingface.co/Edge0/Edge0-35B-A3B-preview)
- [arXiv Paper: 2609.18063 — The Other Half of the Memory Wall](https://arxiv.org/abs/2609.18063)
- [Edge0-AI GitHub Repository](https://github.com/Edge0-AI/edge0)
