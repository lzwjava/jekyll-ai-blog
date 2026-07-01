---
audio: false
generated: true
image: false
lang: en
layout: post
title: AMD MI300X GPU Server Profile
translated: false
type: note
---

Here's the complete picture of **165.245.137.138** end-to-end:

---

## System Overview

| Item | Detail |
| --- | --- |
| **OS** | Ubuntu 24.04, kernel 6.8.0-106-generic |
| **CPU** | Intel Xeon Platinum 8568Y+ (20 cores) |
| **RAM** | 235 GB (241,610 MiB total) |
| **Disk** | 697 GB (611 GB free) |

---

## GPU — AMD Instinct MI300X VF

| Attribute | Value |
| --- | --- |
| PCIe | 5.0 x16 @ 32 GT/s |
| HBM3 | 256 GB physical / **196,288 MiB visible** (~192 GB usable) |
| GFX arch | gfx942 |
| ROCm | **7.2.0** at `/opt/rocm-7.2.0` |
| Driver | amdgpu in-kernel v6.16.13 |
| `rocm-smi` | Detected, RAS all ENABLED |

VRAM headroom after loading Qwen3.5-122B (37 GB GGUF): **~190 GB free** — you could run multiple models or a much bigger one concurrently.

---

## Build Artifacts (`/root/llama.cpp/`)

### llama-cli (`build/bin/llama-cli`)

For one-shot terminal inference. Already smoke-tested with Qwen2.5-0.5B.

### llama-server (`build/bin/llama-server`)

**Currently running** on port 8080, PID 292080.

| Detail | Value |
| --- | --- |
| Model loaded | `models/Qwen3.5-122B-A10B-UD-IQ1_M.gguf` (37 GB) |
| File renamed | Removed `?download=true` suffix |
| Context | 32,768 tokens × 4 slots |
| Prompt caching | 8192 MiB RAM cache enabled |
| API | OpenAI-compatible chat completions |
| Warmup | Completed at startup |
| Chat template | Qwen3.5 with thinking/reasoning support |

### Performance confirmed

| Scenario | Throughput |
| --- | --- |
| Qwen2.5-0.5B (smoke test) | Prompt: 748 t/s, Gen: 484 t/s |
| **Qwen3.5-122B-A10B-IQ1_M (live)** | **Prompt: 77 t/s, Gen: 91 t/s** |

91 t/s on a 122B-parameter model. That's strong — the MoE sparse activation (only ~10B active per token) keeps it fast.

---

## What you can do right now

**1. Hit the API from anywhere:**

```bash
curl http://165.245.137.138:8080/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "Qwen3.5-122B-A10B-UD-IQ1_M",
    "messages": [{"role": "user", "content": "你的问题"}],
    "max_tokens": 500
  }'
```

**2. Run inference directly on the server** (no HTTP overhead):

```bash
cd /root/llama.cpp
export ROCM_PATH=/opt/rocm-7.2.0
export HIP_PATH=$ROCM_PATH
export PATH=$ROCM_PATH/bin:$PATH
./build/bin/llama-cli -m models/Qwen3.5-122B-A10B-UD-IQ1_M.gguf \
  -ngl 99 -p "你的问题" -n 500
```

**3. What else fits in VRAM?** With ~190 GB free, you could run:

| Model | Quant | Est. VRAM | Fits? |
| --- | --- | --- | --- |
| DeepSeek-V2 236B | IQ2_XXS | ~90 GB | Easy |
| DeepSeek-V3 671B | IQ1_S | ~140 GB | Yes |
| Llama 3.1 405B | Q2_K | ~120 GB | Yes |
| Qwen 3.5 235B | IQ2_XXS | ~95 GB | Easy |

**4. Server lifecycle**

- Restart: `ssh root@165.245.137.138 "bash /root/run_server.sh"`
- Logs: `ssh root@165.245.137.138 "tail -f /tmp/llama-server.log"`
- Kill: `ssh root@165.245.137.138 "kill 292080"`
- The script is at `/root/run_server.sh` on the server

---

Want me to download and load a bigger model next, or help you integrate this API endpoint into something on your local machine?
