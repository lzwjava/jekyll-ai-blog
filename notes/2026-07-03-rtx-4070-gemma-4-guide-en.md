---
audio: false
generated: true
image: false
lang: en
layout: post
title: RTX 4070 Gemma 4 Guide
translated: false
type: note
---

**Question:** What about `unsloth/gemma-4-26B-A4B-it-qat-GGUF` — is this a good fit for my RTX 4070 (12 GB) box, and which file should I download?

**Answer:**

Yes — this one is actually a great match for your workstation. Night-and-day difference from GLM-5.2.

**The repo only has one quant, and that's intentional.** The tree contains a single model file, `gemma-4-26B-A4B-it-qat-UD-Q4_K_XL.gguf` at 14.2 GB, plus mmproj vision encoder files. The `qat` suffix means quantization-aware training: Google fine-tuned the weights *with* 4-bit quantization in the loop, so Q4 here recovers near-BF16 quality — same playbook as the Gemma 3 QAT drops. Don't go hunting for Q5/Q6 in other repos; the QAT checkpoint at Q4 is the intended precision and typically beats a post-hoc Q6 of the non-QAT model.

**The memory math:**

```
Weights:        14.2 GB  (26B total × ~4.4 bits/8)
Active/token:    ~4B params → ~2.2 GB touched per forward pass
Your VRAM:       12 GB
Your RAM:        62 GB
```

14.2 GB doesn't fully fit in 12 GB VRAM, but 26B-A4B is a MoE — so you use the same expert-offload trick: attention, embeddings, and shared layers on GPU; routed experts in system RAM. Because only ~4B params activate per token, the CPU side streams very little per step. Expect roughly 25–45 tok/s decode — this is the class of model (like Qwen3-30B-A3B) that feels *fast* on your exact hardware.

**Download and run:**

```bash
# Text-only
huggingface-cli download unsloth/gemma-4-26B-A4B-it-qat-GGUF \
  --include "gemma-4-26B-A4B-it-qat-UD-Q4_K_XL.gguf" --local-dir ~/models

# Optional: vision (it's an image-text-to-text model)
huggingface-cli download unsloth/gemma-4-26B-A4B-it-qat-GGUF \
  --include "mmproj-F16.gguf" --local-dir ~/models

./llama-server \
  -m ~/models/gemma-4-26B-A4B-it-qat-UD-Q4_K_XL.gguf \
  --mmproj ~/models/mmproj-F16.gguf \
  --n-gpu-layers 999 \
  --n-cpu-moe 12 \
  -c 16384 -fa on
```

Tuning `--n-cpu-moe`: start at 12 and decrease until you OOM, then back off by 2. Every expert layer you pull back onto the GPU is free speed. Watch `nvidia-smi` — target ~11.3 GB used, leaving headroom for KV cache. If you want longer context, add `--cache-type-k q8_0 --cache-type-v q8_0` to halve KV memory.

**One caveat on the tooling:** Gemma 4 just landed, so make sure you're on latest llama.cpp master (`git pull && cmake --build build -j`) — new architectures usually need fresh graph support, and MoE offload flags (`--n-cpu-moe`) only apply if the arch is wired up. If `llama-server` errors with `unknown architecture: gemma4`, that's your signal to rebuild.

Grab the mmproj-F16 (1.19 GB) too — a local vision model at this speed is genuinely useful for screenshot-driven agent loops in your CLI tools.

**References:**

- [unsloth/gemma-4-26B-A4B-it-qat-GGUF](https://huggingface.co/unsloth/gemma-4-26B-A4B-it-qat-GGUF/tree/main)