---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Karpathys nanoGPT and nanochat
translated: false
type: note
---

### Overview
nanoGPT and nanochat are both open-source projects created by Andrej Karpathy, designed to make large language model (LLM) training accessible and educational. nanoGPT (released in 2023) focuses on the fundamentals of training GPT-style models from scratch, while nanochat (released in October 2025) builds on it as a more comprehensive "full-stack" pipeline for creating a ChatGPT-like chatbot. The key differences lie in scope, training stages, codebase complexity, and end-to-end usability—nanochat essentially evolves nanoGPT into a complete production-like system for conversational AI.

### Key Differences in Training Code
The training code in nanochat is an extension and refinement of nanoGPT's approach, but it incorporates additional stages, optimizations, and integrations tailored for chat applications. Here's a breakdown:

| Aspect                  | nanoGPT                                                                 | nanochat                                                                 |
|-------------------------|-------------------------------------------------------------------------|--------------------------------------------------------------------------|
| **Primary Focus**      | Pre-training a Transformer-based GPT model on raw text data (e.g., OpenWebText or Shakespeare). Teaches core concepts like tokenization, model architecture, and basic training loops. | Full pipeline: Pre-training + mid-training (conversations/multiple-choice) + supervised fine-tuning (SFT) + optional reinforcement learning (RLHF via GRPO) + evaluation + inference. Builds a deployable chatbot. |
| **Training Stages**    | - Single-stage pre-training.<br>- Basic evaluation (e.g., perplexity). | - **Pre-train**: Similar to nanoGPT but on FineWeb dataset.<br>- **Mid-train**: On SmolTalk (user-assistant dialogues), multiple-choice Q&A, and tool-use data.<br>- **SFT**: Fine-tune for chat alignment, evaluated on benchmarks like MMLU, ARC-E/C, GSM8K (math), HumanEval (code).<br>- **RL**: Optional RLHF on GSM8K for preference alignment.<br>- Automated report card generation with metrics (e.g., CORE score). |
| **Codebase Size & Structure** | ~600 lines total (e.g., `train.py` ~300 lines, `model.py` ~300 lines). Minimal, hackable PyTorch; prioritizes simplicity over completeness. Deprecated in favor of nanochat. | ~8,000 lines of clean, modular PyTorch code. Includes Rust-based tokenizer, efficient inference engine (KV cache, prefill/decode), tool integration (e.g., Python sandbox), and web UI. More cohesive but still forkable. |
| **Optimizer & Hyperparams** | Standard AdamW; learning rates tuned for medium-sized models (e.g., GPT-2 124M params). | Muon + AdamW hybrid (inspired by modded-nanoGPT); adaptive learning rates (e.g., lower for smaller datasets to avoid overfitting). Scales via `--depth` flag for model size. |
| **Data Handling**      | Raw text corpora; basic BPE tokenizer training. | Enhanced: Train custom tokenizer (vocab size ~65K); uses Hugging Face datasets (FineWeb for pre-train, SmolTalk for conversations). Supports synthetic data for personality infusion. |
| **Training Time & Cost** | ~4 days on 8xA100 for GPT-2 equivalent (~$500+). Focuses on educational runs. | ~4 hours on 8xH100 for a basic 560M-param model (~$100); ~12 hours surpasses GPT-2; scales to ~$1,000 for stronger models (e.g., 40% MMLU after 24 hours). |
| **Inference & Deployment** | Basic text generation; no built-in chat or UI. | Optimized engine with KV cache; CLI chat; ChatGPT-style web UI; tool use (e.g., code execution). Models are "naive/silly" but amusing for small scales. |
| **Educational Goal**   | Build the "guts" of a language model (brain). Great for beginners experimenting with architectures. | Build a full ChatGPT clone (from brain to interface). Capstone for advanced courses like LLM101n; potential research benchmark. |

### When to Use Each
- **Choose nanoGPT** if you're new to LLMs and want a lightweight intro to pre-training (e.g., tweaking architectures or datasets). It's simpler but limited to non-conversational models.
- **Choose nanochat** for end-to-end chatbot development. It outperforms nanoGPT on chat tasks (e.g., 58% improvement in some RLHF tests) and includes everything needed to go from data to a working UI in one repo.

Both emphasize hackability—e.g., nanochat allows easy scaling (change model depth) or customization (add synthetic data for personality). nanochat even gives the model self-awareness (e.g., it knows its own size and limitations).

For hands-on exploration:
- [nanoGPT GitHub](https://github.com/karpathy/nanoGPT)
- [nanochat GitHub](https://github.com/karpathy/nanochat)

If you're running these, start with nanochat's `speedrun.sh` script on a cloud GPU like Lambda Labs for the full experience.
