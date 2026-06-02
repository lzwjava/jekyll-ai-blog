---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Karpathy's nanoGPT and nanochat Explained
translated: false
type: note
---

### Overview

Both **nanoGPT** and **nanochat** are open-source projects created by Andrej Karpathy (former OpenAI/Tesla AI lead) to teach the internals of large language models (LLMs) through minimal, from-scratch implementations in PyTorch. They are educational tools rather than production-ready systems, emphasizing simplicity and readability over optimizations.

- **nanoGPT** (released in 2023): A lightweight framework for training GPT-like transformer models on raw text data, focusing solely on the pretraining phase.
- **nanochat** (released in October 2025): An expanded, full-stack evolution of nanoGPT, enabling end-to-end training, fine-tuning, inference, and deployment of a ChatGPT-style conversational AI.

### Key Differences

Here's a side-by-side comparison:

| Aspect              | nanoGPT                                                                 | nanochat                                                                 |
|---------------------|-------------------------------------------------------------------------|--------------------------------------------------------------------------|
| **Primary Focus**   | Pretraining a GPT model on unstructured text (e.g., Shakespeare dataset). | Full pipeline: Pretraining + fine-tuning for chat + inference in a web UI. |
| **Scope**           | Minimal transformer implementation (~400 lines of core code). No chat interface. | ~8,000 lines total, including RLHF-like fine-tuning, sampling, and a Streamlit-based chat demo. |
| **Training**        | Causal language modeling on next-token prediction.                      | Extends to supervised fine-tuning (SFT) and preference optimization (e.g., DPO) for dialogue. |
| **Inference**       | Basic text generation.                                                  | Interactive chat mode with system/user/assistant prompts, temperature sampling, and safety filters. |
| **Hardware/Cost**   | Trainable on a single GPU (e.g., 125M params in hours).                 | Similar efficiency; claims "best ChatGPT $100 can buy" via cheap cloud GPUs. |
| **Inspirations**    | Teaches transformer basics.                                             | Builds on nanoGPT + modded-nanoGPT (gamified version); aims for a complete "ChatGPT clone." |
| **Use Case**        | Learning LLM pretraining.                                               | Building/deploying a basic conversational AI from scratch.               |
| **GitHub Stars**    | ~30k+ (as of 2025).                                                     | Newly released; rapid growth to 10k+ in days.                            |

In essence, nanoGPT is like building the "brain" of a GPT model, while nanochat adds the "mouth" (chat interface) and "ears" (dialogue handling), making it a more complete tutorial for modern LLM apps. If you're diving in, start with nanoGPT for fundamentals, then nanochat for chat-specific extensions.

### References

- [nanochat GitHub Repo](https://github.com/karpathy/nanochat)
- [Karpathy's Announcement on X](https://x.com/karpathy/status/1977755427569111362)
- [Forbes Article on nanochat](https://www.forbes.com/sites/lanceeliot/2025/10/15/make-your-own-chatgpt-clone-for-just-100-via-newly-released-nanochat-but-theres-a-catch/)
- [Medium Post: From nanoGPT to NanoChat](https://medium.com/@sebuzdugan/nanochat-build-your-own-chatgpt-clone-in-8-000-lines-of-code-e07a70cc435e)
