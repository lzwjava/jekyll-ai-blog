---
audio: false
generated: true
image: false
lang: en
layout: post
title: Llama.cpp Inference Engine Overview
translated: false
type: note
---

I have enough now. Here's the picture.

## What this code is

**llama.cpp** is a production LLM **inference engine** written in C/C++. It loads quantized GGUF model weights and runs them efficiently on CPU/GPU (CUDA, Metal, Vulkan, HIP, SYCL, WebGPU, etc.) with no Python runtime. It's the reference implementation behind Ollama, LM Studio, llamafile, and many other tools.

It's **not** a training framework. It cannot backprop. It's the C++ analogue of HuggingFace `transformers` for serving, plus a tensor library underneath.

Code is layered cleanly:

| Layer             | What it is                                                                           | Files                                   |
| ----------------- | ------------------------------------------------------------------------------------ | --------------------------------------- |
| `ggml/`           | Tensor library: ops + multi-backend executor (CPU/CUDA/Metal/…)                      | `ggml/src/ggml*.{c,cpp}`                |
| `src/`            | The "transformer engine": model loader, KV cache, graph builders, sampler, tokenizer | `src/llama-*.{cpp,h}`                   |
| `src/models/`     | 129 per-architecture files defining each model's forward graph                       | `gpt2.cpp`, `llama.cpp`, `qwen3.cpp`, … |
| `tools/`          | Executables: `cli`, `server`, `quantize`, `perplexity`, `bench`                      | `tools/cli/cli.cpp`                     |
| `include/llama.h` | Public C API (~1570 lines)                                                           |                                         |

## Compared to nanoGPT

nanoGPT is **353 lines, one file, training + inference, PyTorch, GPT-2 only.** llama.cpp is ~20k lines in the core alone, inference-only, supports ~130 architectures, ~10 backends, and ~20 quant formats.

The interesting comparison is what they *share*. Look at nanoGPT's `Block.forward` (`/mnt/data/nanoGPT/model.py:116`):

```python
x = x + self.attn(self.ln_1(x))
x = x + self.mlp(self.ln_2(x))
```

And llama.cpp's GPT-2 graph in `src/models/gpt2.cpp:82-124` — same structure, just written as ggml tensor ops:

```cpp
cur = build_norm(inpL, attn_norm, attn_norm_b, LLM_NORM, il);          // ln_1
auto [Q,K,V] = build_qkv(...);                                          // c_attn split
cur = build_attn(inp_attn, wo, wo_b, ..., Q, K, V, ..., 1/sqrt(d), il);// attn + c_proj
ffn_inp = ggml_add(ctx0, cur, inpL);                                    // residual
cur = build_norm(ffn_inp, ffn_norm, ffn_norm_b, LLM_NORM, il);          // ln_2
cur = build_ffn(cur, ffn_up, ffn_up_b, ..., ffn_down, ..., LLM_FFN_GELU, ...); // MLP
cur = ggml_add(ctx0, cur, ffn_inp);                                     // residual
```

**Same algorithm.** GPT-2 in 147 lines vs nanoGPT's whole file in 353 — llama.cpp's is shorter because tokenizer/sampler/KV cache live elsewhere, and the bias-having LayerNorm + learned positional embedding + tied lm_head are all parameterized into `build_norm` / `build_inp_pos` / the loader.

## Key differences from nanoGPT's GPT to llama.cpp's Llama (`src/models/llama.cpp`)

This is also where you see what makes a "modern" model vs GPT-2:

| GPT-2 (nanoGPT)                         | Llama (llama.cpp)                                                   |
| --------------------------------------- | ------------------------------------------------------------------- |
| `LayerNorm` with optional bias          | `RMSNorm`, no bias                                                  |
| Learned positional embeddings (`wpe`)   | **RoPE** (rotary, applied to Q and K inside attention)              |
| `n_head_kv == n_head` (multi-head)      | **GQA**: `n_head_kv` can be smaller (grouped-query attention)       |
| MLP: `up → GELU → down` (sequential)    | MLP: `SiLU(gate) * up → down` (**SwiGLU**, parallel)                |
| Single dense MLP                        | Optionally **MoE**: gate picks top-k of N experts (`build_moe_ffn`) |
| `c_attn` produces Q,K,V from one matmul | Q,K,V from one or split matmuls, then RoPE rotated                  |

You can see all four (RMSNorm, RoPE, GQA, SwiGLU) in `src/models/llama.cpp:130-217` — that's basically the diff between "GPT-2 in 2019" and "Llama-3 in 2024."

## Core inference loop logic

nanoGPT does this in `generate()` (model.py:328) — pure Python, recomputes the whole forward pass each token. llama.cpp's equivalent is split across these pieces:

1. **Model load** (`llama-model-loader.cpp` → `src/models/<arch>.cpp::load_arch_tensors`) — mmap GGUF, register tensors per layer.
2. **Graph build** (`src/models/<arch>.cpp::graph` ctor) — once per batch, build a ggml compute DAG. This is the "model.py forward" equivalent, but it builds a graph instead of running ops directly.
3. **Backend execute** (`ggml-backend.cpp`) — schedule the DAG onto CPU/CUDA/Metal kernels.
4. **KV cache** (`llama-kv-cache.cpp`, 2502 lines) — *the* speedup over nanoGPT. nanoGPT recomputes K,V for the entire prefix every token (O(T²) work per step). llama.cpp stores K,V per layer and only computes K,V for the new tokens, attending against the cached past. That's the whole reason production engines exist.
5. **Sampler** (`llama-sampler.cpp`) — same idea as nanoGPT's `temperature / top_k / multinomial` block at model.py:339-348, but as a chainable pipeline: temperature → top-k → top-p → min-p → typical → mirostat → grammar → softmax → sample. Each is a small struct with `apply()`.
6. **Token loop** (`tools/cli/cli.cpp`) — feed prompt batch → decode → sample → append → decode 1 token → repeat. Same shape as nanoGPT's `for _ in range(max_new_tokens)` loop, just wrapped in batching + streaming + chat templating.

## TL;DR

nanoGPT teaches you what the math is. llama.cpp is what you ship when you actually need it to run fast on someone's laptop: same transformer math underneath, but with (a) a portable tensor IR (ggml) instead of PyTorch, (b) a KV cache so generation is O(T) not O(T²), (c) integer quantization for fitting big models in small RAM, (d) one file per architecture so adding a new model is mostly writing its forward graph using shared `build_norm` / `build_qkv` / `build_attn` / `build_ffn` primitives.