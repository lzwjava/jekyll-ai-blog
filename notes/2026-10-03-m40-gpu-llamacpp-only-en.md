---
audio: false
generated: true
image: false
lang: en
layout: post
title: "M40 GPU: llama.cpp only"
translated: false
type: note
---

Nope — nanoGPT uses **PyTorch** (+ `torchrun`, `torch.distributed` for DDP), same hard blocker. Can't even get PyTorch installed on CC 5.2.

Here's the consistent **rule of thumb** for this M40:

| Can run | Can't run |
| --------- | ----------- |
| ✅ Anything using **llama.cpp** (inference, fine-tuning, embeddings, server) | ❌ Anything requiring **PyTorch / TensorFlow** |
| ✅ **Whisper.cpp** (audio→text) | ❌ vLLM, DeepSpeed, nanoGPT, HuggingFace `transformers` |
| ✅ Direct **CUDA C/C++** programs | ❌ Any Python ML framework built on top of CUDA abstractions |

The fundamental difference: llama.cpp writes its own raw CUDA kernels, so it can target CC 5.2. Everything else (PyTorch, TF, JAX) compiled out support for Maxwell years ago.
