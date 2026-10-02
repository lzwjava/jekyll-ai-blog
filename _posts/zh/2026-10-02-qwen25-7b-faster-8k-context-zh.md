---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Qwen2.5-7B：更快，8K上下文
translated: true
type: note
---

完成！✅ **Qwen2.5-7B** 现已运行，**上下文长度为 8192**，位于 `lzw@192.168.1.34:8080`。

| 设置 | 之前 | 之后 |
| --------- | -------- | ------- |
| **模型** | Qwen3.8-27B-UD-IQ1_M (6.3G) | **Qwen2.5-7B-Instruct-Q4_K_M** (4.4G) |
| **上下文** | 4096 | **8192** |
| **GPU 内存** | ~2.4G | **~4.9G**（仍可适配 11.5G Tesla M40） |
| **推理速度** | ~8.4 t/s | **~17.2 t/s**（快 2 倍） |

较小的 7B 模型采用更高精度的量化（Q4_K_M 对比 IQ1_M），运行速度显著提升，同时上下文窗口扩大了一倍。一切正常！
