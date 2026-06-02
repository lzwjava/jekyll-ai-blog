---
audio: false
generated: true
image: false
lang: en
layout: post
title: Gemma 4 12GB VRAM Server Crashes
translated: false
type: note
---

Here's the full summary:

---

**Model Download ✅**

- Downloaded `gemma-4-26B-A4B-it-UD-IQ3_S.gguf` (10.4GB) from HuggingFace via proxychains
- File location: `/home/lzw/projects/llama.cpp/models/`

**Running on:**

- **GPU:** RTX 4070 (12GB VRAM)
- **VRAM usage:** ~10.7GB (31/31 layers offloaded)
- **Context:** 512 tokens (max due to VRAM constraints)
- **Quantization:** IQ3 (4-bit with quality optimization)
- **llama.cpp build:** b1-25eec6f32

**Issue:**
The server crashes after each inference — it exits cleanly after processing one request. This appears to be a memory management or SWA (Sliding Window Attention) bug in this version of llama.cpp with Gemma 4's architecture. With only 512 tokens context, it works for simple prompts but hits OOM or a crash on longer outputs.

**Status:**
Server is currently down. You'd need to restart it before each use, or we could try:

1. A different GGUF variant (e.g., Q4_K_M instead of IQ3_S)
2. Patching/updating llama.cpp to a newer build
3. Reducing `-ngl` layers to free up more VRAM for compute buffers

**API:** `http://localhost:8081` — works with OpenAI-compatible `/v1/chat/completions` endpoint.
