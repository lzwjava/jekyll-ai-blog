---
audio: false
generated: true
image: false
lang: zh
layout: post
title: NVIDIA显卡中的Ti
translated: true
type: note
---

Question: NVIDIA 显卡型号如 RTX 5060 Ti 中的“Ti”是什么意思？

Answer:

“Ti” = Titanium。它是 NVIDIA 用于表示同一基础芯片中经过更高筛选、功能更完整的版本的后缀，位于普通版与更高一级型号之间。

具体来说，在同一颗 GPU 芯片（例如这里的 GB206）内：
- 非 Ti 版（RTX 5060）：启用的 CUDA 核心数更少，频率更低，通常显存更少，TDP 更低
- Ti 版（RTX 5060 Ti）：同一芯片上解锁更多核心，频率更高，通常显存更多/位宽更大，TDP 更高

本代示例：
- RTX 5060 8GB：3840 CUDA 核心，145W TDP
- RTX 5060 Ti 16GB：4608 CUDA 核心，180W TDP，相同 128-bit 位宽但满配 GDDR7 容量

这纯粹是一种市场细分标签——没有固定规则（并不总是“同一芯片，更好的筛选”；有时完全是不同的芯片，例如 RTX 4070 与 4070 Ti 是不同的 GPU）。历史上可追溯到 GeForce 2 Ti（2000 年）。除了“产品线中更好的 SKU”之外，没有架构层面的含义，不像“Super”（中期更新）或“Founders Edition”（NVIDIA 公版设计）。

针对你的情况：型号命名本身并不能告诉你关于带宽/显存取舍的推理相关信息——始终要查看实际规格表（位宽、GB/s、显存容量），而不是依赖层级名称。