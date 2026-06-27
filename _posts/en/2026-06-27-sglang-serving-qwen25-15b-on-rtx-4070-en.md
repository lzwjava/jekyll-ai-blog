---
audio: false
generated: true
image: false
lang: en
layout: post
title: sglang Serving Qwen2.5-1.5B on RTX 4070
translated: false
type: note
---

Done. sglang is running and serving Qwen2.5-1.5B-Instruct successfully on the RTX 4070.

Here's the summary:

WHAT WAS SET UP:
  Fresh venv: ~/sglang-env
  torch: 2.7.1+cu126 (CUDA 12.6 runtime)
  triton: 3.3.1 (not the segfaulting 3.5/3.6)
  sglang: 0.4.10.post2
  sgl-kernel: 0.2.8
  flashinfer: 0.2.9rc2

KEY DETAILS:
  - Driver 580.x is backward-compatible with cu126 (no driver change needed)
  - The cu124 wheel max was torch 2.6.0, but sglang 0.4.x hard-pins torch==2.7.1
  - Used cu126 wheels instead — same driver compatibility, torch 2.7.1 available
  - triton 3.3.1 (bundled with torch 2.7.1) does NOT segfault on Ada/sm_89
  - CUDA graph capture completed in 0.52s — no crashes
  - Server responding at http://0.0.0.0:30000 with OpenAI-compatible API

LAUNCH SCRIPT: /tmp/start-sglang.sh
  Sets proxy (127.0.0.1:7890) and PATH, then runs sglang on port 30000

TO RESTART LATER:
  ssh lzw@192.168.1.36 "nohup /tmp/start-sglang.sh > /tmp/sglang-server.log 2>&1 &"
