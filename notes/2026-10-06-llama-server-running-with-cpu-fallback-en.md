---
audio: false
generated: true
image: false
lang: en
layout: post
title: llama-server running with CPU fallback
translated: false
type: note
---

Done. Here's the summary:

## Previous setup found
From the last pi session (Oct 4), llama.cpp was run as a tmux session named `llama` using the **llama-b11344 CUDA bundle** (not the `~/projects/llama.cpp` source build). The exact command was:

```bash
tmux new-session -d -s llama -x 200 -y 50 \
  'cd ~/projects/llama-b11344 && LD_LIBRARY_PATH=. \
   ./llama-server -m /home/lzw/models/qwen2.5-1.5b-instruct-q4_k_m.gguf \
   -ngl 99 -t 4 --host 0.0.0.0 --port 8080 2>&1 | tee ~/llama-server.log'
```

## Re-ran it — status: ✅ running

- **tmux session**: `llama` (created 23:13)
- **Endpoint**: `http://0.0.0.0:8080` — listening, pid 4670
- **Health**: `{"status":"ok"}`
- **Model**: Qwen2.5-1.5B-Instruct Q4_K_M
- **Inference test**: responded `Hello!`
- **Speed** (CPU): ~131 t/s prompt, ~76 t/s generation

⚠️ Note: `-ngl 99` is passed, but the Tesla M40 (Maxwell sm_52) is **not** supported by the CUDA 12.8 build (which only ships sm_120a kernels), so it silently falls back to CPU. This matches all prior runs. If you want actual GPU offload, you'd need to build llama.cpp from source with CUDA arch targeting sm_52 (the source tree at `~/projects/llama.cpp` is available).

Log: `~/llama-server.log`. Reattach with `tmux a -t llama`.