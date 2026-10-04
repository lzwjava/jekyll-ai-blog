---
audio: false
generated: true
image: false
lang: en
layout: post
title: M40 running llama.cpp server
translated: false
type: note
---

Done — llama.cpp is cloned, built (via prebuilt CUDA 12.8 binary), and **running as a live server on the M40**. 🎉

## What's running

**llama-server** is up on `http://192.168.1.34:8080` (OpenAI-compatible API), serving **Qwen2.5-1.5B-Instruct (Q4_K_M)** fully offloaded to the Tesla M40.

Verified end-to-end:

```
POST /v1/chat/completions
→ "A GPU, or Graphics Processing Unit, is a specialized electronic circuit
   designed to rapidly manipulate and alter memory to accelerate the creation
   of images in a frame buffer intended for output to a display."
```

| Metric | Value |
|--------|-------|
| Health | `{"status":"ok"}` |
| GPU utilization | 96% (peak) |
| Power draw | 174 W (idle 16 W) |
| VRAM used | ~2.1 GB / 11.4 GB |
| Prompt processing | ~219 t/s |
| Generation | ~88 t/s |
| Context window | 32,768 |

## What's where
- Repo: `~/projects/llama.cpp`
- Binaries: `~/projects/llama-b11344/` (CUDA 12.8 prebuilt + bundled libcudart/libcublas)
- Model: `~/models/qwen2.5-1.5b-instruct-q4_k_m.gguf` (1.04 GB)
- Server process: PID 7946, log at `~/server.log`

## Use it from any machine on your LAN
```bash
curl http://192.168.1.34:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"Hello!"}],"max_tokens":100}'
```

Or with the OpenAI SDK: `base_url="http://192.168.1.34:8080/v1"`.

## Notes
- I used the **CUDA 12.8** build deliberately — the CUDA 13.4 build drops Maxwell (sm_52). The kernels JIT down to sm_52 fine.
- This M40 tops out around a 1.5B model for comfortable serving; a 7B Q4 (~4.4GB) would fit in VRAM but decode would drop to ~15–20 t/s given the M40's old FP16 path and 288 GB/s bandwidth.
- To restart later: `cd ~/projects/llama-b11344 && LD_LIBRARY_PATH=$PWD nohup ./llama-server -m ~/models/qwen2.5-1.5b-instruct-q4_k_m.gguf --host 0.0.0.0 --port 8080 -ngl 99 </dev/null > ~/server.log 2>&1 &`

Want me to try a bigger model (e.g., Qwen2.5-3B or Llama-3.2-3B) to see how far the M40 can go?