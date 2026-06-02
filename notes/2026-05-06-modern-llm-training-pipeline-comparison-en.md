---
audio: false
generated: true
image: false
lang: en
layout: post
title: Modern LLM Training Pipeline Comparison
translated: false
type: note
---

## llmTrain

This is an **educational end-to-end LLM training pipeline** — train a BPE tokenizer from raw text, then train a ~100M parameter Transformer from scratch. The model ("MiniLLM-0.1B") was published on HuggingFace Hub.

---

## vs. nanoGPT

| Aspect | **nanoGPT** | **llmTrain** |
|---|---|---|
| **Architecture** | Classic GPT-2 (learned positional embeddings, GELU) | Modern: RoPE + SwiGLU + pre-norm |
| **Attention** | Manual attention math | Flash Attention via `scaled_dot_product_attention` |
| **Position encoding** | Learned absolute embeddings | Rotary (RoPE) |
| **Activation** | GELU | SwiGLU (gated linear units) |
| **Tokenizer** | Uses GPT-2 tokenizer (tiktoken) | Trains its own BPE from scratch |
| **Data pipeline** | Memory-mapped files | Pre-tokenized `.pt` tensors + async DataLoader |
| **Compilation** | `torch.compile` | `torch.compile` |
| **Scope** | Full GPT-2 replication + fine-tuning | Training pipeline only (no fine-tuning) |
| **Focus** | Reproduce GPT-2 results | Show full pipeline: data → tokenizer → model |
| **HF integration** | Minimal | Native — saves as `AutoModelForCausalLM` |

**Key difference**: nanoGPT replicates GPT-2's exact architecture and can reproduce published results. llmTrain uses a **more modern architecture** (closer to LLaMA-style) and adds a complete **tokenizer training stage** that nanoGPT skips. It's less focused on benchmarks and more focused on showing the full pipeline end-to-end.
