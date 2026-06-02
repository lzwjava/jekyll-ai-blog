---
audio: false
generated: true
image: false
lang: en
layout: post
title: Gemma4 Flash Attention Fix
translated: false
type: note
---

## Comprehensive Review: Gemma4 Troubleshooting on RTX 4070

### System Profile

| Component | Detail |
|-----------|--------|
| **OS** | Ubuntu, Linux 6.8.0-107-generic x86_64 |
| **GPU** | NVIDIA RTX 4070 (12GB VRAM), CUDA 13.0, Driver 580.126.20 |
| **RAM** | 62GB total, ~57GB available |
| **CPU** | 32 cores |
| **llama.cpp** | Commit `94ca829b6`, built with `GGML_CUDA=ON`, `GGML_CUDA_FA=ON`, Release `-O3` |

### Models Available

| Model | Size | Status |
|-------|------|--------|
| `gemma-4-26B-A4B-it-UD-IQ2_M.gguf` | 9.3GB | Tested, working |
| `gemma-4-26B-A4B-it-UD-IQ3_S.gguf` | 11GB | Untested — likely too large for 12GB VRAM with KV cache |
| `DeepSeek-R1-Distill-Llama-8B-Q4_K_M.gguf` | — | Previously used |
| `Mistral-Small-24B-Instruct-2501-Q2_K.gguf` | — | Was running before this session |

### Root Cause Analysis

**The crash:** Two CUDA errors captured in `llama.log`, both with identical backtrace:

```
ggml_cuda_error → ggml_backend_cuda_buffer_set_tensor → ggml_backend_sched_graph_compute_async
  → llama_context::graph_compute → process_ubatch → decode → llama_decode
```

**The cause:** Flash Attention CUDA kernels failing on gemma4's architecture. Gemma4 is a **MoE (Mixture of Experts)** model with:

- **Mixed SWA/non-SWA layers** — 25 SWA layers + 5 non-SWA layers
- **Different V embedding sizes across layers** — llama.cpp explicitly warns: `"the V embeddings have different sizes across layers and FA is not enabled - padding V cache to 2048"`

The FA kernels don't properly handle this heterogeneous layer structure, causing an out-of-bounds CUDA buffer write during tensor set operations.

### What We Did

1. **Inspected the system** — identified GPU, RAM, build config, model files
2. **Read crash logs** (`llama.log`) — found CUDA buffer overflow in FA path
3. **Read server logs** (`llama-server.log`) — found Mistral was running, with context overflow errors (17-18K tokens vs 16K limit)
4. **Attempted `--no-flash-attn`** — flag renamed in current version, failed
5. **Found correct flag** (`--flash-attn off`) via `--help`
6. **Launched successfully** — model loaded, responded correctly
7. **Fixed binding** — changed from `127.0.0.1` to `0.0.0.0:8081`

### Current Running Configuration

```bash
llama-server \
  -m gemma-4-26B-A4B-it-UD-IQ2_M.gguf \
  --flash-attn off \
  -ngl 99 \
  -c 4096 \
  --host 0.0.0.0 \
  --port 8081
```

### Resource Usage

| Resource | Usage |
|----------|-------|
| VRAM | 11.3GB / 12GB (model 9.5GB + KV 920MB + compute 522MB) |
| RAM | ~1GB mapped to CPU |
| Speed | ~111 tokens/sec generation, ~127 tokens/sec prompt processing |

### Concerns & Recommendations

1. **VRAM is tight** (11.3/12GB). With 4 slots and 4096 context, longer conversations may OOM. Consider:
   - Reducing to `-c 2048` or `--parallel 2` if you hit issues
   - Or offloading a few layers to CPU with `-ngl 28` instead of `99`

2. **IQ2_M is a very aggressive quantization** — expect noticeable quality degradation vs the original 26B model. The IQ3_S (11GB) would be better quality but won't fit with KV cache overhead.

3. **The V-cache padding** (to 2048) wastes some VRAM. This is a known limitation when FA is off — the cache can't use the actual per-layer V sizes and must pad to the max.

4. **Upstream fix** — this is likely a known issue in llama.cpp's CUDA FA kernels for gemma4. Worth watching the repo for PRs mentioning "gemma4 flash attention" — once fixed, re-enabling FA would save VRAM and may improve speed.

5. **The old `llama.sh` script** still points to `DeepSeek-R1-Distill-Llama-8B` on port 8000. You may want to update it if gemma4 becomes your default.
