---
audio: false
generated: true
image: false
lang: en
layout: post
title: Gemma-4-26B RTX 4070 Configuration Guide
translated: false
type: note
---

thought;Question: What is the best configuration for Gemma-4-26B-A4B-it-GGUF to run on an RTX 4070 (12GB VRAM) with OpenClaw and llama.cpp, while maintaining a long context size?

Answer: To run **Gemma-4-26B-A4B-it** effectively on an RTX 4070 with 12GB of VRAM for agentic tasks like OpenClaw, you must balance the model's weight size against the VRAM required for a long KV cache. 

### Recommended Quantization
For a 12GB VRAM limit, you should use **IQ3_M** or **IQ3_S** (Importance Quantization) versions.
* **UD-IQ3_M / UD-IQ3_S (~11.2 GB):** These are the highest quants that will fit the weights on your card with minimal room left. However, because OpenClaw requires a significant context buffer, this will likely overflow your VRAM once you start a conversation.
* **UD-IQ2_M (~10.0 GB):** This is the **safest choice** for 12GB. It leaves ~2GB of VRAM for the KV cache (context), which is essential for agentic workflows that involve long system prompts and history.

### Llama.cpp Configuration for Long Context
To maximize your 12GB VRAM, use the following `llama.cpp` flags:
1.  **Flash Attention:** Use `--flash-attn` to significantly reduce VRAM usage during long context processing.
2.  **KV Cache Quantization:** Use `--cache-type-k q8_0 --cache-type-v q8_0` (or even `q4_0`) to compress the context memory, allowing for much longer context (e.g., 32k or 64k) within the remaining 2GB of VRAM.
3.  **Partial Offloading:** If the model weights slightly exceed 12GB, set `-ngl` (number of GPU layers) to offload most, but not all, layers to the GPU. For this 26B MoE model, offloading about **40-45 layers** usually fits 12GB while keeping the "active" experts mostly on-GPU for speed.

### OpenClaw Integration
Since OpenClaw is an agent that often sends large amounts of context (tools, past thoughts, and environment state), ensure your server is started with a high context limit:
```bash
./llama-server -m gemma-4-26B-A4B-it-UD-IQ2_M.gguf -c 32768 --flash-attn --cache-type-k q4_0 -ngl 99
```
*Note: If you experience "Out of Memory" (OOM) errors, reduce `-ngl` until it stabilizes.*



References:
- [Unsloth Gemma-4-26B-A4B-it-GGUF Hub](https://huggingface.co/unsloth/gemma-4-26B-A4B-it-GGUF)
- [Gemma 4 Fine-tuning and Inference Guide](https://unsloth.ai/docs/models/gemma-4/train)
- [LocalLLaMA: VRAM Requirements for Gemma 4](https://www.reddit.com/r/LocalLLaMA/comments/1scw979/gemma_4_for_16_gb_vram/)