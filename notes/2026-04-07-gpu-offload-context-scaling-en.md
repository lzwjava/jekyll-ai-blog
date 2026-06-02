---
audio: false
generated: true
image: false
lang: en
layout: post
title: GPU Offload and Context Scaling Results
translated: false
type: note
---

## Comprehensive Summary

### Setup Journey

**Starting point** (from your info):

- llama-server running with `-ngl 20` (20 GPU layers)
- Model: `gemma-4-E4B-it-Q5_K_M.gguf`
- Context: 32k
- VRAM used: ~2,695 MiB with 9GB headroom wasted

---

### Step 1 — GPU Layer Increase

Bumped from ngl 20 → ngl 35 (already done when session started), then pushed to full offload:

| ngl | VRAM used | Layers on GPU | CPU layers |
|---|---|---|---|
| 20 | ~2,695 MiB | 20 / 43 | 23 |
| 35 | ~5,030 MiB | 35 / 43 | 8 |
| **43** | **~5,182 MiB** | **43 / 43** | **0** |

Going from ngl 35 → 43 (full offload) only cost +152 MiB — essentially free. Zero CPU↔GPU data transfer during inference now.

---

### Step 2 — Context Size: 32k → 64k

Restarted with `-c 65536`. KV cache doubled but VRAM impact was modest:

| Context | VRAM (idle) | VRAM (after long prompt) |
|---|---|---|
| 32k | ~5,030 MiB | ~5,182 MiB |
| **64k** | **~6,118 MiB** | **~6,646 MiB** |

Cost of doubling context: **+936 MiB idle**, **+528 MiB** extra during a 60k token inference. Still 5GB+ headroom remaining.

---

### Step 3 — Long Prompt Stress Tests

**First test** (32k ctx era): 12,020 token prompt → success in 6.9s

**64k context tests:**

| Prompt tokens | % of 64k ctx | Completion | Total time | Gen speed |
|---|---|---|---|---|
| 20,025 | 30% | 385 tok | 7.5s | **51.6 tok/s** |
| 40,025 | 61% | 383 tok | 14.1s | **27.1 tok/s** |
| 60,025 | 92% | 444 tok | 20.2s | **22.0 tok/s** |

**Zero crashes across all tests.**

---

### Performance Analysis

**Speed vs context depth:**

```
20k prompt → 51.6 tok/s  (baseline)
40k prompt → 27.1 tok/s  (-47% vs 20k)
60k prompt → 22.0 tok/s  (-57% vs 20k)
```

This is expected — attention computation is **O(n²)** in sequence length, so generation slows as more tokens are in the KV cache. The model doesn't degrade in quality though — responses were coherent at all sizes.

**Prefill throughput** (rough estimate from total time):

- 20k tokens in ~3-4s → ~5,000–6,000 tokens/s prefill
- 60k tokens in ~8-10s → ~6,000–7,500 tokens/s prefill

Prefill is fast because it's parallelized on GPU; generation is the bottleneck.

---

### Final Server Configuration

```bash
llama-server \
  -m gemma-4-E4B-it-Q5_K_M.gguf \
  --flash-attn off \
  -ngl 43 \          # full GPU offload
  -c 65536 \         # 64k context
  --host 0.0.0.0 \
  --port 8081
```

| Resource | Usage | Headroom |
|---|---|---|
| VRAM (12,282 MiB total) | ~6,646 MiB | **~5,600 MiB free** |
| Context | 65,536 tokens | Up to 131,072 (model max) |
| GPU layers | 43/43 | Full offload |

**Potential next steps** if you want more speed:

- Enable `--flash-attn on` (currently off) — could improve throughput at long contexts significantly
- Try `-c 131072` (model's native max) — ~+1.5GB VRAM, still fits
- Increase parallel slots (`-np`) if serving multiple users
