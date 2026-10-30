---
audio: false
generated: true
image: false
lang: en
layout: post
title: ROCm llama.cpp Works on gfx900
translated: false
type: note
---

Done — full pipeline works. Here's the summary:

## Result

| Stage | Status |
| ------- | -------- |
| Clone | `~/projects/llama.cpp` @ `eb4e244` |
| Build | HIP/ROCm backend, `gfx900`, `GGML_CUDA_FORCE_MMQ=ON` |
| Model | `models/Qwen2.5-7B-Instruct-Q4_K_M.gguf` (4.36 GiB, 7.62 B params) |
| Inference | ✅ running on **AMD Radeon Pro WX 9100** (`gfx900`), no CPU fallback |

**Benchmark (ROCm, ngl=99):**

```
pp128: 182.86 t/s
tg32:   45.84 t/s
```

**Sample output** — prompt *"Explain in one sentence what a GPU is."*:
> A GPU is a specialized electronic circuit that processes graphics and can also be used for general-purpose computing tasks.

## Key gotcha you'll want to remember

ROCm **7.1 dropped `gfx900` from rocBLAS** — its Tensile kernels only ship for `gfx908/gfx90a`. A normal HIP build crashes at runtime:

```
rocBLAS error: Cannot read .../TensileLibrary.dat: Illegal seek for GPU arch : gfx900
```

Fix: build with `-DGGML_CUDA_FORCE_MMQ=ON` so llama.cpp uses its own MMQ kernels instead of hipBLAS. (You'll also need `libhipblas-dev` installed just to satisfy CMake, even though it's unused at runtime.)

## How to run

```bash
cd ~/projects/llama.cpp
export PATH="$HOME/.local/bin:$PATH"   # for cmake

# one-shot completion
./build/bin/llama-completion -m models/Qwen2.5-7B-Instruct-Q4_K_M.gguf \
    -ngl 99 -p "Your prompt" -n 256

# interactive chat
./build/bin/llama-cli -m models/Qwen2.5-7B-Instruct-Q4_K_M.gguf -ngl 99

# OpenAI-compatible server on :8080
./build/bin/llama-server -m models/Qwen2.5-7B-Instruct-Q4_K_M.gguf -ngl 99 --host 127.0.0.1 --port 8080
```

Everything is on GPU; VRAM used is ~4.4 GiB of the 16 GiB, so you have plenty of headroom for a larger model or long context.
