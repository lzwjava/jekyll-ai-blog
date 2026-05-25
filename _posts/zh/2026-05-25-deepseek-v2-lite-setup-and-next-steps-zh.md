---
audio: false
generated: true
image: false
lang: zh
layout: post
title: DeepSeek-V2-Lite 设置与后续步骤
translated: true
type: note
---

以下是您昨天的笔记。以下是摘要：

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

同一天的 MoE 前向传播笔记（`2026-05-24-moe-layer-forward-pass-explained-en.md`）也记录了 DeepSeek V3 的架构——共享专家 + 256 个路由专家、top-8 选择、无辅助损失的负载均衡。

接下来您想做什么？以下是一些选项：

1. SSH 进入 192.168.1.36 并运行交互式聊天以探索模型
2. 在此基础上进一步尝试——使用不同的量化方式、测试速度或实验 MoE 路由
3. 更深入地研究 MoE 架构（前向传播笔记中带有形状标注）