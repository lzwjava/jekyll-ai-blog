---
audio: false
generated: true
image: false
lang: en
layout: post
title: Gemma 4B Deployment Success
translated: false
type: note
---

**✅ Gemma 4 26B is stable and running!**

**Results:**
- ✅ Server stays up after multiple inferences
- ✅ Multi-turn conversation works
- ✅ Multi-turn caching works (prompt 44 tokens reused from cache)
- ✅ **Speed:** ~38 tokens/sec generation
- ✅ **Context:** 2048 tokens
- ✅ **GPU layers:** 25/31 on CUDA, 6 on CPU
- ✅ **VRAM:** ~9.5GB / 12GB used (leaving headroom)

**Working config:**
```
-m ./models/gemma-4-26B-A4B-it-UD-IQ3_S.gguf
-ngl 25
-c 2048
--host 0.0.0.0
--port 8081
```

The key was reducing `-ngl` from 31 to 25 — gives ~2GB VRAM headroom for compute buffers, which was causing the OOM crashes.
