---
audio: false
generated: true
image: false
lang: en
layout: post
title: Qwen3.5-397B Model Technical and Cost Overview
translated: false
type: note
---

Question: What are the training details, architecture, and estimated costs for Qwen3.5-397B-A17B?

Answer: Released in February 2026, **Qwen3.5-397B-A17B** is a flagship native vision-language model from Alibaba's Qwen team. It is notable for its massive scale combined with high inference efficiency due to its sparse architecture.

### **1. Model Architecture**

The model uses a **Hybrid Mixture-of-Experts (MoE)** architecture combined with a **Gated DeltaNet** (a form of linear attention), which allows it to handle extremely long contexts more efficiently than standard Transformers.

* **Total Parameters:** 397 Billion
* **Active Parameters:** 17 Billion (per token)
* **Layers:** 60
* **Hidden Dimension:** 4,096
* **Experts:** 512 total experts (10 routed + 1 shared expert activated per token).
* **Context Window:** 262,144 tokens (native), extensible up to **1.01 million tokens** via YaRN RoPE scaling.
* **Tokenizer:** 248,320 vocabulary size, supporting 201 languages.

### **2. Training Details**

While Alibaba does not disclose the specific datasets, the training involved several advanced techniques:

* **Data Scale:** Trillions of multimodal tokens covering text, images, and video.
* **Multi-Token Prediction (MTP):** Trained with multi-step prediction to improve long-horizon reasoning and planning.
* **Early Fusion:** A unified multimodal backbone where vision and language tokens are processed in the same latent space from the start.
* **Post-Training:** Extensive Reinforcement Learning (RL) was used to enhance "Thinking Mode" (internal reasoning) and agentic capabilities.

### **3. Hardware & Estimated Costs**

The model is optimized for **NVIDIA GPU-accelerated systems** (H100/H200/B200 clusters).

* **Card Requirements:** Due to its 397B total parameters, even with 4-bit quantization (~200GB+ VRAM), it typically requires a multi-GPU setup (e.g., **8x H100 80GB** or **4x B200**) just for inference. Training such a model would require thousands of interconnected GPUs.
* **API Costs (per 1M tokens):** * **Input:** ~$0.39 - $0.60
  * **Output:** ~$2.34 - $3.60
* **Estimated Compute Cost/Hour:** To rent an 8x H100 node (capable of serving this model at high throughput), market rates in 2026 hover around **$20 - $35 per hour** depending on the provider (e.g., Together AI, Lambda, or Alibaba Cloud).

References:

* [Qwen3.5-397B-A17B Model Card on NVIDIA NIM](https://build.nvidia.com/qwen/qwen3.5-397b-a17b/modelcard)
* [Qwen/Qwen3.5-397B-A17B on Hugging Face](https://huggingface.co/Qwen/Qwen3.5-397B-A17B)
* [Artificial Analysis: Qwen3.5-397B-A17B Performance & Specs](https://artificialanalysis.ai/articles/qwen3-5-397b-a17b-everything-you-need-to-know)
