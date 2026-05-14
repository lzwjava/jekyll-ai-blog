---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RTX 4070 LLM 部署选项
translated: true
type: note
---

确认：**RTX 4070，12 GB 显存，可用约 12.1 GB**，CUDA 13.0，驱动 580。既然你在使用 `llama.cpp`，以下是通过 `llama-server`（GGUF）提供的实际可选方案——预留约 1–2 GB 用于 KV 缓存 + 上下文。

## 最佳适配（全 GPU 卸载至 GPU，速度快）

| 模型                            | 量化方式            | 显存占用  | 说明                                     |
| -------------------------------- | ----------------- | --------------- | --------- | ----------------------------------------- |
| **Qwen2.5-14B-Instruct**         | Q4_K_M           | ~9 GB     | 最佳通用 14B 中综合最强；推理与编码能力强 |
| **Qwen2.5-Coder-14B-Instruct**   | Q4_K_M           | ~9 GB     | 32B 以下最佳开源编码。
| **Phi-4 (14B)**                  | Q4_K_M           | ~9 GB     | 微软出品，推理能力非常强 |
| **Mistral-Small-2501 (24B)**     | IQ3_XXS / Q3_K_S | ~10–11 GB | 显存吃紧，短上下文可运行         |
| **Gemma-2-9B-it**                | Q5_K_M           | ~7 GB     | 预留更多上下文空间             |
| **Llama-3.1-8B-Instruct**        | Q6_K             | ~7 GB     | 全能型选手 |
| **Qwen2.5-7B-Instruct**          | Q6 / Q8~ GB / 8 GB | 高              |
| **DeepSeek-Instruct (14B)** | Q4_K_M           | ~9 GB     | 推理优化  |

## 推荐
**Qwen2.5Instruct Q4_K_M** -- 完全可在  GPU 上运行，16–32k 上下文，在 4070 上约 40–60 tok/s。

## 极限尝试（部分卸载，速度较慢）
- **Mistral-Small-24B Q4_K_M** （~14 GB） -- 卸载约 30/40 层，预计 10–20 tok/s
- **Qwen2.5-32B Q3_K_M** （~14 GB） -- 同理，Q3 质量下降明显

## 快速启动命令
```bash
./llama-server -m qwen5-155_q4_m.gguf \
  -ngl 99 -c 16384 --host 0.0.0.0 --port 8 -fa
```
层；`-ngl 99` = 所有层在 GPU；`-fa` = 闪存注意力（节省显卡内存）；如需要更大量化空间，可将 `-c` 降至 8192。

需要我下载一个并跑跑看？