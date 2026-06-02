---
audio: false
generated: true
image: false
lang: en
layout: post
title: Remote LLM Proxy Configuration Guide
translated: false
type: note
---

## What Was Set Up

**Problem:** Tree of Thought uses a custom API format `{model, system_prompt, input}` — llama.cpp expects standard OpenAI `{messages:[...]}`.

**Solution:** A 3-piece chain:

```
ToT (local:8000) → SSH tunnel :1234 → remote proxy :8088 → llama-server :8080
```

**Files on remote (192.168.1.36):**
- `~/tot_proxy.py` — translates ToT format → OpenAI format, listens on :8088
- llama-server running with `DeepSeek-R1-0528-Qwen3-8B-Q4_K_M.gguf` on :8080
- Logs: `~/llama8b.log`, `~/tot_proxy.log`

---

## To Change the Model

SSH in and restart llama-server with a different `.gguf`:

```bash
ssh lzw@192.168.1.36
pkill llama-server
nohup /home/lzw/projects/llama.cpp/build/bin/llama-server \
  -m /home/lzw/projects/llama.cpp/models/DeepSeek-R1-Distill-Qwen-32B-Q2_K.gguf \
  --host 0.0.0.0 --port 8080 -ngl 99 \
  > ~/llama8b.log 2>&1 &
```

Available models on remote:
- `deepseek-r1-distill-qwen-1.5b-q4_0.gguf` — tiny/fast
- `DeepSeek-R1-0528-Qwen3-8B-Q4_K_M.gguf` — **current, recommended**
- `DeepSeek-R1-Distill-Qwen-32B-Q2_K.gguf` — large, may fit in 12GB

---

## To Restart Everything After Reboot

```bash
# On remote
ssh lzw@192.168.1.36
nohup /home/lzw/projects/llama.cpp/build/bin/llama-server \
  -m /home/lzw/projects/llama.cpp/models/DeepSeek-R1-0528-Qwen3-8B-Q4_K_M.gguf \
  --host 0.0.0.0 --port 8080 -ngl 99 > ~/llama8b.log 2>&1 &
nohup python3 ~/tot_proxy.py > ~/tot_proxy.log 2>&1 &

# On local Mac (new terminal)
ssh -f -N -L 1234:localhost:8088 lzw@192.168.1.36
```

Frontend stays at `http://localhost:1234/api/v1/chat`, all model fields set to `local`.
