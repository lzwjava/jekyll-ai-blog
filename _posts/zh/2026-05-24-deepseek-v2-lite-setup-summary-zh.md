---
audio: false
generated: true
image: false
lang: zh
layout: post
title: DeepSeek-V2-Lite 设置摘要
translated: true
type: note
---

全部完成。以下是摘要：

```
=== DeepSeek-V2-Lite-Chat 设置完成 ===

模型：DeepSeek-V2-Lite-Chat（160亿参数，通过MoE每个token激活24亿参数）
  - 与V4相同的MLA架构，规模缩小
  - 4位NF4量化，采用双重量化

显存：已使用9.5 GB（可用11.6 GB）——适配您的RTX 4070
模型路径：/mnt/data/models/DeepSeek-V2-Lite-Chat/
脚本：/mnt/data/deepseek-v4-inference/run_lite.py

使用方法：
  python3.11 /mnt/data/deepseek-v4-inference/run_lite.py              # 交互式对话
  python3.11 /mnt/data/deepseek-v4-inference/run_lite.py -p "提示"  # 单次提示
  python3.11 /mnt/data/deepseek-v4-inference/run_lite.py -p "提示" -n 1024  # 更多token

已安装依赖：
  - bitsandbytes 0.49.2
  - accelerate 1.13.0
  - python3.11 头文件从3.12符号链接（用于triton）

模型大小：磁盘约30GB（bf16），显存约9.5GB（4位NF4）
```

想要尝试交互模式吗？
