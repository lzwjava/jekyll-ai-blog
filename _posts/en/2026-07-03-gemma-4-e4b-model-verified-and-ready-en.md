---
audio: false
generated: true
image: false
lang: en
layout: post
title: Gemma 4 E4B Model Verified and Ready
translated: false
type: note
---

It works! Here's the complete verification:

**Model loaded and generated text**: "I am a language model, trained by Google."

**Architecture**: Gemma 4 E4B (7.52B params, Q3_K quant, 3.76 GiB file)

**Gemma 4 E4B key specs from the GGUF metadata**:
- 42 layers, 2560 embed dim, 10240 FF dim
- 8 attention heads, 2 KV heads (GQA=4)
- 131K context length (both global + sliding window attention at 512)
- BPE tokenizer, 262k vocab
- Shared KV layers (18 shared across layers — Gemma 4's layer-tied KV design)
- Layer Input weights («per_layer_token_embd», per-layer input gating/projection — Gemma 4's "Gated Delta Net" architecture)

**Performance on RTX 4070 12GB**:
- Prompt eval: 291 t/s
- Generation: 91 t/s
- VRAM used: 2343 MiB model + 14 MiB KV + overhead → ~3.2 GiB total, plenty of room

The file is at `/mnt/data/models/gemma-4-E4B-it-Q3_K_M.gguf` and ready to use. Want me to start the `llama-server` so you can chat with it or configure it in Hermes?