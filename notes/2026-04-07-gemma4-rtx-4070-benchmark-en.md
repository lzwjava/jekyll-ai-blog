---
audio: false
generated: true
image: false
lang: en
layout: post
title: Gemma4 RTX 4070 Benchmarking Review
translated: false
type: note
---

## Comprehensive Review: Gemma4 on RTX 4070 — Full Troubleshooting & Benchmarking

### System Profile

| Component | Detail |
|-----------|--------|
| **OS** | Ubuntu, Linux 6.8.0-107-generic x86_64 |
| **GPU** | NVIDIA RTX 4070 (12GB VRAM), CUDA 13.0, Driver 580.126.20 |
| **RAM** | 62GB total, ~57GB available |
| **CPU** | 32 cores |
| **llama.cpp** | Commit `94ca829b6`, built with `GGML_CUDA=ON`, `GGML_CUDA_FA=ON`, Release `-O3` |
| **Model** | `gemma-4-26B-A4B-it-UD-IQ2_M.gguf` (9.3GB) |

---

### Root Cause: CUDA Flash Attention Crash

**Symptom:** Repeated CUDA errors in `ggml_backend_cuda_buffer_set_tensor` during `llama_decode`.

**Cause:** Gemma4 has a heterogeneous architecture:
- **25 SWA (Sliding Window Attention) layers** + **5 non-SWA layers**
- **Different V embedding sizes across layers**
- The Flash Attention CUDA kernels don't handle this mixed layout correctly, causing out-of-bounds buffer writes

**Fix:** `--flash-attn off` — forces the fallback path that pads V-cache to 2048, which works correctly.

---

### Benchmarking Results

All configs tested with `--flash-attn off`, model fully loaded (IQ2_M 9.3GB).

| Config | Context | `-ngl` | Layers on GPU/CPU | VRAM Used | Prompt Speed | Gen Speed | Max Tested Prompt |
|--------|---------|--------|-------------------|-----------|-------------|-----------|-------------------|
| **Full GPU** | 4,096 | 99 | 31/0 | 11.3GB | 127 tok/s | **92 tok/s** | 27 tokens |
| **Full GPU** | 8,192 | 99 | 31/0 | 11.5GB | 1,718 tok/s | **92 tok/s** | 5,906 tokens |
| **Hybrid** | 16,384 | 26 | 26/5 | 10.2GB | 1,286 tok/s | **32 tok/s** | 13,436 tokens |
| **Hybrid** | 32,768 | 20 | 20/11 | 9.2GB | 793 tok/s | **15 tok/s** | 26,828 tokens |

**Failed configs:**
| Config | Reason |
|--------|--------|
| 32K + ngl 99 | OOM at startup — compute buffer allocation failed |
| 16K + ngl 99 | OOM during inference — `MUL_MAT` CUDA OOM |

---

### Key Observations

1. **Generation speed degrades linearly with CPU offload** — each layer moved to CPU costs ~7 tok/s. The 32K config is 6x slower than 8K because 11/31 layers run on CPU.

2. **Prompt processing stays fast** — even at 32K with heavy CPU offload, prompt ingestion is 793 tok/s because it's batched and benefits from parallelism.

3. **V-cache padding tax** — without FA, the V-cache pads every layer's V embeddings to 2048 dims regardless of actual size. This wastes VRAM:
   - Non-SWA KV (5 layers): 320MB at 8K, 960MB at 32K
   - SWA KV (25 layers): 800-900MB (capped by sliding window size)

4. **VRAM budget breakdown at 32K / ngl 20:**
   - Model (20 GPU layers): ~6.1GB
   - Non-SWA KV cache: ~960MB
   - SWA KV cache: ~900MB
   - Compute buffers: ~1.0GB
   - Total: ~9.0GB — leaves 3GB headroom

5. **IQ2_M quality** — this is an aggressive 2-bit quantization. The model produces reasoning traces (`reasoning_content`) but actual `content` responses were empty in most tests, suggesting the model spends its token budget on chain-of-thought. May need `--override-kv` or prompt tuning.

---

### Recommendations

| Priority | Action |
|----------|--------|
| **Use now** | 8K/ngl 99 if you need speed (92 tok/s), 32K/ngl 20 if you need long context (15 tok/s) |
| **Quality** | Consider the IQ3_S quant (11GB) with 4K context + ngl 99 — better quality, still fits in VRAM |
| **Watch upstream** | Monitor llama.cpp PRs for gemma4 FA fixes — re-enabling FA would save ~200-400MB on V-cache padding, potentially allowing 16K at full GPU speed |
| **Production** | Update `/home/lzw/llama.sh` to reflect whichever config you settle on |
| **Prompt format** | The server auto-detected `peg-gemma4` chat format with thinking enabled — if you want direct answers without reasoning traces, pass `"thinking": false` or adjust the system prompt |

---

### Current State

Server running at `http://192.168.1.36:8081` with **32K context, ngl 20, flash-attn off**. Stable, tested up to 26,828 tokens.