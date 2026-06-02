---
audio: false
generated: true
image: false
lang: en
layout: post
title: "MiniMind: A Minimalist LLM Educational Project"
translated: false
type: note
---

Question: What is MiniMind (jingyaogong/minimind)?

Answer: **MiniMind** is an open-source educational project designed to demystify the "black box" of Large Language Models (LLMs). It provides a complete, from-scratch implementation of a minimalist language model—small enough to be trained on a single consumer GPU (like an NVIDIA RTX 3090) in about 2 hours for approximately $0.50 (3 CNY).

The project is structured as a "tutorial-first" repository, focusing on clarity and reproducibility rather than massive scale.

### 1. Key Philosophy: "The Greatest Path is the Simplest"

Unlike mainstream frameworks (like Hugging Face `transformers` or `peft`) that wrap complex logic in abstract functions, MiniMind implements core algorithms using **native PyTorch**. This allows users to read and understand every line of code involving:

* **Model Architecture:** A Transformer Decoder-only structure (similar to Llama 3.1).
* **Training Pipelines:** Pre-training, Supervised Fine-Tuning (SFT), and Reinforcement Learning (RLHF/DPO).
* **Efficiency Techniques:** LoRA (Low-Rank Adaptation) and Mixture of Experts (MoE) implemented from the ground up.

### 2. Technical Specifications

The models in the MiniMind series are extremely lightweight, ranging from **26M to 145M parameters** (about 1/7000th the size of GPT-3).

| Feature | Description |
| :--- | :--- |
| **Architecture** | Transformer Decoder-only with RMSNorm, SwiGLU activation, and RoPE (Rotary Position Embeddings). |
| **Variants** | Supports both **Dense** models and **MoE** (Mixture of Experts) models. |
| **Multimodal** | Includes **MiniMind-V**, a version capable of vision-language tasks (image recognition and chat). |
| **Training Hardware** | Optimized for a single GPU (24GB VRAM); supports multi-GPU via DDP and DeepSpeed. |
| **Data Format** | Uses simplified JSONL or Parquet formats to eliminate complex preprocessing steps. |

### 3. Core Components of the Repository

* **Data Preparation:** Scripts for cleaning and deduplicating high-quality datasets.
* **Full-Stage Training:**
    1. **Pre-training:** Learning basic language patterns from scratch.
    2. **SFT:** Instruction tuning to follow user commands.
    3. **DPO/RLHF:** Aligning the model with human preferences for better "politeness" and logic.
    4. **Distillation:** Learning from larger "teacher" models (like DeepSeek-V3 or R1).
* **Inference & Deployment:** Compatible with `llama.cpp`, `vllm`, and `ollama`. It even includes a minimalist Streamlit WebUI for testing.

### 4. Why use MiniMind?

* **For Beginners:** It serves as a practical "Deep Dive" into how LLMs actually work without the complexity of billion-parameter scales.
* **For Researchers:** It provides a "white-box" environment to test new algorithms (like custom loss functions or architectural tweaks) rapidly.
* **For Developers:** It offers a blueprint for migrating models to private, domain-specific datasets (e.g., medical or legal) with minimal cost.

References:

* [MiniMind GitHub Repository](https://github.com/jingyaogong/minimind)
* [MiniMind Project Documentation & Homepage](https://jingyaogong.github.io/minimind/)
* [MiniMind-V (Vision-Language Model) Branch](https://github.com/jingyaogong/minimind-v)
