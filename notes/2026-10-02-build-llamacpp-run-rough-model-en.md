---
audio: false
generated: true
image: false
lang: en
layout: post
title: Build llama.cpp, Run Rough Model
translated: false
type: note
---

The remote machine has llama.cpp source but **it's not compiled** — no `build` directory or binary. The old llama-server (PID 7946) must have been from a different source.

You need to build it first:

```bash
ssh lzw@192.168.1.34
cd ~/projects/llama.cpp
cmake -B build
cmake --build build --config Release -j $(nproc)
```

That'll take a few minutes to compile. After it finishes, run:

```bash
./build/bin/llama-server -m models/Qwen3.8-27B-UD-IQ1_M.gguf --port 8080 --host 0.0.0.0
```

Given your Tesla M40 has **11.5GB VRAM** and this model is **6.3GB** (Qwen 3.8 27B at IQ1_M), it should fit. Though IQ1_M is an extremely low-bit quantization — quality may be very rough.
