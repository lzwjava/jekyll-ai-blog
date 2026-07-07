---
audio: false
generated: true
image: false
lang: en
layout: post
title: Model Capacity on 16GB VRAM
translated: false
type: note
---

Now I have the full picture. Let me summarize what's on this pod:

## Hardware: RunPod RTX 2000 Ada — 16 GB VRAM

### Model capacity with SGLang

| Precision | Max params | Example models | VRAM used |
| ----------- | ----------- | ---------------- | ----------- |
| **FP16/BF16** | **7-8B** | LLaMA-3-8B, Mistral-7B, Qwen2.5-7B | ~16GB (tight on long context) |
| **FP8/INT8** | **13-16B** | Llama-2-13B, DeepSeek-V2-Lite-16B, Qwen2.5-14B | ~8-9GB + room for KV cache |
| **INT4 (AWQ/GPTQ)** | **30-34B** | Qwen2.5-32B, Yi-34B, CodeQwen-32B | ~8GB → lots of headroom |
| **INT4 72B** | **72B (barely)** | Qwen2.5-72B-AWQ | ~14GB → only ~2GB for KV cache = very short context |

### Existing model on disk

Your **SEC-EDGAR-GPT (124M)** is already in HuggingFace format at `/workspace/model/hf-model/` — it's a 628MB safetensors model. This is tiny for SGLang (would use < 1 GB VRAM), so you have plenty of room.

### The question

What model do you want to serve? Options:

1. **Your existing SEC-EDGAR-GPT 124M** — trivial, lots of headroom
2. **A new model** — the GPU can handle up to 7-8B FP16 or 30B-34B INT4. Which one?
