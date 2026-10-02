---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Qwen2.5-7B: Faster, 8K Context"
translated: false
type: note
---

Done! ✅ **Qwen2.5-7B** is now running with **8192 context size** on `lzw@192.168.1.34:8080`.

| Setting | Before | After |
| --------- | -------- | ------- |
| **Model** | Qwen3.8-27B-UD-IQ1_M (6.3G) | **Qwen2.5-7B-Instruct-Q4_K_M** (4.4G) |
| **Context** | 4096 | **8192** |
| **GPU Mem** | ~2.4G | **~4.9G** (still fits on 11.5G Tesla M40) |
| **Inference** | ~8.4 t/s | **~17.2 t/s** (2x faster) |

The smaller 7B model with higher quality quantization (Q4_K_M vs IQ1_M) runs much faster and with double the context window. All good!
