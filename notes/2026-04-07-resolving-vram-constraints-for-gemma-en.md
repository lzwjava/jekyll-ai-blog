---
audio: false
generated: true
image: false
lang: en
layout: post
title: Resolving VRAM Constraints for Gemma
translated: false
type: note
---

Here's the full summary:

---

**What we did:**
1. Downloaded `gemma-4-26B-A4B-it-UD-IQ3_S.gguf` (10.4GB) from HuggingFace via proxychains
2. Rebuilt llama.cpp from source (latest commit `b8-94ca829b6`)
3. Started llama-server with the Gemma 4 26B model

**Key findings:**
- The old build had the **SWA (Sliding Window Attention) bool/uint32 bug** — fixed by rebuilding
- **VRAM was the real constraint** — with 31 GPU layers, there was zero headroom for compute buffers → OOM crashes
- Solution: **`-ngl 25`** (offload 25 of 31 layers to GPU, leave 6 on CPU) + **`-c 2048`** context
- This freed ~2GB VRAM for compute, making inference stable

**Running config:**
```
-m ./models/gemma-4-26B-A4B-it-UD-IQ3_S.gguf
-ngl 25
-c 2048
--host 0.0.0.0
--port 8081
--path ./tools/server/public
```

**Performance:**
- ~38 tokens/sec generation speed
- 2048 token context
- VRAM: ~9.5GB / 12GB used

**Firewall issue:**
- Port 8081 was blocked by UFW → added rule `sudo ufw allow 8081/tcp`

**Current status:**
- ✅ Llama-server: running on port 8081 with built-in web UI
- ✅ OpenWebUI: also running on port 11435