---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Agnes-3.0-Flash 开放权重预览
translated: true
type: note
---

**问题：** Hugging Face 上的 Agnes-3.0-Flash 是什么？

**回答：**

Agnes-3.0-Flash Preview 是 Agnes AI 于 2026 年 9 月发布的一款开放权重多模态 AI 模型。以下是详细介绍：

**它是什么**

这是一个开放权重的多模态预览模型（33B 参数），专为“无需旗舰级硬件即可获得旗舰级推理能力”而构建，支持文本、图像和视频理解，上下文窗口为 262,144 个 token。

**重要说明**

本仓库包含较早的开放权重 **预览检查点**，与更新的 **生产版/API 检查点** 不同。生产版模型使用不同的配置，上下文窗口为 100 万 token——其基准测试结果不应归因于此处发布的预览权重。

**架构亮点**

它使用混合注意力解码器：每 4 层中有 3 层运行门控 Delta 规则（循环），仅 1/4 运行标准全局注意力。这意味着 72 层中只有 18 层持有随上下文长度增长的 KV 缓存——使其在长序列场景下更节省内存。

**关键能力**

| 特性 | 详情 |
|---|---|
| 参数 | 33B |
| 上下文窗口 | 262,144 个 token |
| 模态 | 文本、图像、视频 |
| 推理强度 | 高 / 中 / 低（可调） |
| 工具调用 | 是 |
| 许可证 | Apache 2.0 |

**硬件要求**

bf16 检查点约需 66 GB 磁盘空间，推荐在 1× NVIDIA H200 141 GB 或 H100 80 GB GPU 上运行，主机内存建议 128 GB 或以上。

**基准测试性能**

在 GPQA Diamond（研究生级科学推理基准）上，预览检查点得分为 85.05，与 Qwen3.5-27B（85.8）等模型相当，但落后于 Gemini 3.5 Flash（92.2）等更大或仅 API 的模型。

**参考链接：**
- [Agnes-AI/Agnes-3.0-Flash 在 Hugging Face 上](https://huggingface.co/Agnes-AI/Agnes-3.0-Flash)
- [Agnes AI 官网](https://agnes-ai.com/)