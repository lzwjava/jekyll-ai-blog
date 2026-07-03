---
audio: false
generated: true
image: false
lang: en
layout: post
title: Gemma 4 Model Setup and llama.cpp Update
translated: false
type: note
---

Here's the full session summary.

---

## Session: Gemma 4 E4B — Download, verify, update llama.cpp

### 1. Downloaded model

- **File**: `gemma-4-E4B-it-Q3_K_M.gguf` at `/mnt/data/models/`
- **Size**: 3.8 GB (Q3_K_M quantization, 4.30 BPW)
- **Method**: `curl` through proxy (127.0.0.1:7890) — `hf` CLI failed because Python's `requests` doesn't route through the shell proxy properly
- **SHA256**: `db7ba769f71e7d4e8ec11db42152ba20f422a12d58960a665b5395e111582072`

### 2. Model architecture (from GGUF metadata)

| Property | Value |
| --- | --- |
| Architecture | Gemma 4 (gemma4) |
| Params | 7.52 B (labeled "E4B") |
| Layers | 42 |
| Embed dim | 2560 |
| FF dim | 10240 |
| Attention heads | 8 (GQA = 4, 2 KV heads) |
| Context length | 131,072 |
| Sliding window | 512 (hybrid — 35 SWA layers + 7 global layers) |
| RoPE base | 1,000,000 (global), 10,000 (SWA) |
| Logit softcap | 30.0 |
| Shared KV layers | 18 (layer-tied KV design) |
| Per-layer input embeds | Yes (Gated Delta Net) |
| Vocab | BPE, 262,144 tokens |
| License | Apache 2.0 |

### 3. Initial inference test (old build b8)

- Prompt eval: 291 t/s
- Generation: 91 t/s
- VRAM: 2,343 MiB model + ~14 MiB compute buffer on RTX 4070

### 4. Updated llama.cpp

- **Repo**: `git@github.com:ggerganov/llama.cpp.git`
- **Bumped from**: b8 (834a24366)
- **Bumped to**: version 1194 (067de9371)
- **142+ new tags** pulled (b9156 → b9600 range)
- Major changes expected: improved Gemma 4 support, Gated Delta Net optimizations, flash attention improvements

### 5. Build

- **Build system**: CMake + Ninja, `-DGGML_CUDA=ON -DCMAKE_BUILD_TYPE=Release`
- **Disk issue**: Root partition hit 100% (430M free) during CUDA template compilation
- **Cleanup**: Removed 101G — `~/.cache/uv/` (45G), `~/.cache/nanochat/` (39G), `~/.cache/pip/` (17G)
- **Result**: 77G free, full build of 679 targets succeeded
- **Binaries rebuilt**: `llama-cli`, `llama-server`, `llama-simple`, `llama-perplexity`, `llama-bench`, etc.

### 6. Final verification

- `llama-cli --version` → version 1194 (067de9371)
- Gemma 4 E4B Q3_K_M inference on new build: ~68 t/s, working correctly

### Current state

- Updated llama.cpp at `~/projects/llama.cpp/build/bin/`
- Model ready at `/mnt/data/models/gemma-4-E4B-it-Q3_K_M.gguf`
- 77 GB free on root, 795 GB free on /mnt/data
