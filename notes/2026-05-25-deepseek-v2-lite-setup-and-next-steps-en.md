---
audio: false
generated: true
image: false
lang: en
layout: post
title: DeepSeek-V2-Lite Setup and Next Steps
translated: false
type: note
---

Here's your note from yesterday. Here's the summary:

```
================================================================
  DeepSeek-V2-Lite-Chat on RTX 4070 — Setup Complete
================================================================

WHAT WAS DONE (May 24):
  - Downloaded DeepSeek-V2-Lite-Chat (16B total, 2.4B activated/token)
  - Installed bitsandbytes (4-bit NF4 quant) + accelerate
  - Fixed missing Python.h (symlinked python3.12 headers as 3.11)
  - Wrote inference script at /mnt/data/deepseek-v4-inference/run_lite.py
  - Successfully ran test — model loads in ~2.5 min, uses 9.5 GB VRAM

MODEL LOCATION: /mnt/data/models/DeepSeek-V2-Lite-Chat/ (30GB on disk)
SCRIPT:         /mnt/data/deepseek-v4-inference/run_lite.py
VRAM:           9.5 GB / 11.6 GB (82%)
QUANTIZATION:   4-bit NF4 with double quant

HOW TO USE (on 192.168.1.36):
  Interactive:  python3.11 /mnt/data/deepseek-v4-inference/run_lite.py
  One-shot:     python3.11 /mnt/data/deepseek-v4-inference/run_lite.py -p "your prompt"
  Longer:       python3.11 /mnt/data/deepseek-v4-inference/run_lite.py -p "prompt" -n 1024
================================================================
```

The MoE forward pass note from the same day (`2026-05-24-moe-layer-forward-pass-explained-en.md`) also documents DeepSeek V3's architecture — shared expert + 256 routed experts, top-8 selection, auxiliary-loss-free load balancing.

What do you want to do next? Some options:

1. SSH into 192.168.1.36 and run interactive chat to explore the model
2. Build on this — try different quantization, benchmark speed, or experiment with MoE routing
3. Study the MoE architecture deeper (the forward pass note has shape annotations)
