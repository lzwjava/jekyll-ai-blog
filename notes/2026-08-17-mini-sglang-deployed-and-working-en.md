---
audio: false
generated: true
image: false
lang: en
layout: post
title: Mini-SGLang Deployed and Working
translated: false
type: note
---

Done — Mini-SGLang is up and verified working. ✅

## What happened

The first launch attempt appeared stuck, and it turned out to be a **missing model download**, not a code issue:

1. **Root cause**: `Qwen/Qwen3-0.6B` was only partially cached (tokenizer/config from Aug 3, but the 1.5 GB weights file had never finished downloading — an old 16 MB fragment from a failed attempt).
2. The server was blocked in HuggingFace's **Xet download backend**, which stalled at 87.6% (~1.31/1.5 GB) behind your Clash proxy.
3. **Fix**: I killed the stuck process and restarted with `HF_HUB_DISABLE_XET=1` — meanwhile the download had completed in the background, so the fresh start loaded weights straight from cache (no re-download).

## Current state

| Item | Value |
|---|---|
| Server | `http://localhost:1919` (OpenAI-compatible) |
| Model | `Qwen/Qwen3-0.6B` (bf16) |
| Process | PID 1668187, log at `/tmp/minisgl.log` |
| KV cache | 73,288 tokens (~7.8 GiB), 0.84 GiB free |
| Verified | `/v1/models` + `/v1/chat/completions` both respond correctly |

The model even ran its Qwen3 thinking mode on the test prompt. Note the GPU now shows **11.3 GiB used** (12 GB card) — this model fits, but something like Qwen3-4B would be tight; Qwen2.5-3B-Instruct (also cached) is a comfortable fit.

Useful for later:
```bash
curl http://localhost:1919/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"Qwen/Qwen3-0.6B","messages":[{"role":"user","content":"hi"}]}'
```

One tip: if you launch it again, keep `HF_HUB_DISABLE_XET=1` in the env to avoid the flaky Xet backend. Want me to try a different model, run the benchmark, or wire up a client script?