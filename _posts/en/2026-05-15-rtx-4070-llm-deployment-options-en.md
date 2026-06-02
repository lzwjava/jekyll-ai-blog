---
audio: false
generated: true
image: false
lang: en
layout: post
title: RTX 4070 LLM Deployment Options
translated: false
type: note
---

Confirmed: **RTX 4070, 12 GB VRAM, ~12.1 GB free**, CUDA 13.0, driver 580. Since you're in `llama.cpp`, here are realistic options served via `llama-server` (GGUF) — budgeting ~1–2 GB for KV cache + context.

## Best fits (full GPU offload, fast)

| Model                            | Quant            | VRAM      | Notes                                     |
| -------------------------------- | ---------------- | --------- | ----------------------------------------- |
| **Qwen2.5-14B-Instruct**         | Q4_K_M           | ~9 GB     | Best general 14B; strong reasoning/coding |
| **Qwen2.5-Coder-14B-Instruct**   | Q4_K_M           | ~9 GB     | Top open coder under 32B                  |
| **Phi-4 (14B)**                  | Q4_K_M           | ~9 GB     | Microsoft, very strong reasoning for size |
| **Mistral-Small-2501 (24B)**     | IQ3_XXS / Q3_K_S | ~10–11 GB | Tight but works at short ctx              |
| **Gemma-2-9B-it**                | Q5_K_M           | ~7 GB     | Leaves lots of room for context           |
| **Llama-3.1-8B-Instruct**        | Q6_K             | ~7 GB     | Solid all-rounder                         |
| **Qwen2.5-7B-Instruct**          | Q6_K / Q8_0      | ~6 / 8 GB | High quality at Q8                        |
| **DeepSeek-R1-Distill-Qwen-14B** | Q4_K_M           | ~9 GB     | Reasoning-tuned                           |

## Sweet spot recommendation
**Qwen2.5-14B-Instruct Q4_K_M** (or the Coder variant) — fits fully on GPU with ~16–32k context, ~40–60 tok/s on a 4070.

## Push-the-limit (partial offload, slower)
- **Mistral-Small-24B Q4_K_M** (~14 GB) — offload ~30 of 40 layers, expect ~10–20 tok/s
- **Qwen2.5-32B Q3_K_M** (~14 GB) — same trick, quality drops noticeably at Q3

## Quick serve command
```bash
./llama-server -m qwen2.5-14b-instruct-q4_k_m.gguf \
  -ngl 99 -c 16384 --host 0.0.0.0 --port 8080 -fa
```
`-ngl 99` = all layers on GPU; `-fa` = flash attention (saves KV memory); drop `-c` to 8192 if you want headroom for larger quants.

Want me to download one and benchmark it?
