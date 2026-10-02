---
audio: false
generated: true
image: false
lang: en
layout: post
title: Qwen2.5-7B Running on Remote Server
translated: false
type: note
---

✅ **Done!** The Qwen2.5-7B model is now running on the remote server `lzw@192.168.1.34`.

Here's a summary of what was done:

| Step | Action |
| ------ | -------- |
| 🔍 | Identified running `llama-server.service` (transient) on `192.168.1.34` using **Qwen3.8-27B-UD-IQ1_M.gguf** (6.3G) |
| ⏹️ | Stopped the old service via `systemctl --user kill llama-server.service` |
| ✅ | Verified `Qwen2.5-7B-Instruct-Q4_K_M.gguf` (4.4G) was **already present** in the models directory |
| ▶️ | Started new service: `systemd-run --user --unit=llama-server /home/lzw/projects/llama-b11344/llama-server -m .../Qwen2.5-7B-Instruct-Q4_K_M.gguf --port 8080 --host 0.0.0.0 -ngl 99 -c 4096` |
| 🧪 | **Tested** — API responds correctly: `{"choices":[{"finish_reason":"stop","index":0,"message":{"role":"assistant","content":"Hello!"}}]}` |

**Model running**: `Qwen2.5-7B-Instruct-Q4_K_M.gguf` on port **8080**, with all 99 layers offloaded to GPU, 4096 context size. Inference is fast: ~11 t/s prompt processing, ~19.8 t/s text generation.
