---
audio: false
generated: true
image: false
lang: en
layout: post
title: DeepSeek-V2-Lite Setup Summary
translated: false
type: note
---

All done. Here's the summary:

```
=== DeepSeek-V2-Lite-Chat Setup Complete ===

MODEL: DeepSeek-V2-Lite-Chat (16B params, 2.4B activated/token via MoE)
  - Same MLA architecture as V4, scaled down
  - 4-bit NF4 quantization with double quant

VRAM: 9.5 GB used (of 11.6 GB available) — fits your RTX 4070
MODEL PATH: /mnt/data/models/DeepSeek-V2-Lite-Chat/
SCRIPT: /mnt/data/deepseek-v4-inference/run_lite.py

USAGE:
  python3.11 /mnt/data/deepseek-v4-inference/run_lite.py              # interactive chat
  python3.11 /mnt/data/deepseek-v4-inference/run_lite.py -p "prompt"  # single prompt
  python3.11 /mnt/data/deepseek-v4-inference/run_lite.py -p "prompt" -n 1024  # more tokens

DEPS INSTALLED:
  - bitsandbytes 0.49.2
  - accelerate 1.13.0
  - python3.11 headers symlinked from 3.12 (for triton)

MODEL SIZE: ~30GB on disk (bf16), ~9.5GB in VRAM (4-bit NF4)
```

Want to try it in interactive mode?