---
audio: false
generated: true
image: false
lang: en
layout: post
title: Download Q4_K_M fused model
translated: false
type: note
---

Direct answer from that tree:

| File in the repo | Runnable? |
|---|---|
| `Qwen3.8-27B-Uncensored-<QUANT>.gguf` (fused) | **YES** - standalone, MTP head included |
| `Qwen3.8-27B-Uncensored-noMTP-<QUANT>.gguf` | **YES** - standalone, but pair with the draft file for speed |
| `Qwen3.8-27B-Uncensored-draft-<QUANT>.gguf` | **NO** - this is what you have. Draft head only |
| `mmproj-Qwen3.8-27B-Uncensored-F16.gguf` | NO - vision projector, not a model |

So download **one** of the fused files. For your RTX 4070 (12 GB VRAM, ~9.4 GB free) + 62 GB RAM:

| Quant | Size | Verdict |
|---|---|---|
| `IQ2_M` | 10.6 GB | too lossy (PPL 7.86 vs 7.18) |
| `IQ4_XS` | 15.3 GB | good, most VRAM headroom |
| **`Q4_K_M`** | **16.8 GB** | **best pick** - PPL 7.18, ~9 GB GPU + ~8 GB RAM |
| `Q5_K_M` | 19.5 GB | fine, slower |
| `Q6_K` / `Q8_0` | 22-29 GB | mostly CPU, noticeably slower |

Command for the one to get:

```bash
hf download JonathanColetti/Qwen3.8-27B-Uncensored-GGUF \
  Qwen3.8-27B-Uncensored-Q4_K_M.gguf \
  --local-dir /mnt/data/llama.cpp/models
```

Then:

```bash
cd /mnt/data/llama.cpp && ./build/bin/llama-server \
  -m models/Qwen3.8-27B-Uncensored-Q4_K_M.gguf \
  --spec-type draft-mtp --spec-draft-n-max 2 \
  -c 32768 -ngl auto --fit on \
  --host 127.0.0.1 --port 8080
```

Web UI at `http://127.0.0.1:8080`.

Your existing `draft-Q8_0.gguf` becomes unnecessary with the fused file (the MTP head is already inside). It's only needed if you go the `noMTP-*` + explicit `-md` route.

Shall I download Q4_K_M now and launch it?