---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Gemini与DeepSeek Flash对比
translated: true
type: note
---

问题：比较 Gemini 3.5 Flash 与 DeepSeek V4 Flash

答案：以下是 Google Gemini 3.5 Flash 与 DeepSeek V4 Flash 在核心技术能力、处理性能和成本效率方面的对比。

### 关键指标对比

| 特性 / 指标 | Google Gemini 3.5 Flash | DeepSeek V4 Flash |
| --- | --- | --- |
| **上下文窗口** | 1.05M tokens | 1.05M tokens |
| **输入价格（每百万 tokens）** | $1.50 | ~$0.0983 |
| **输出价格（每百万 tokens）** | $9.00 | ~$0.1966 |
| **输入模态** | 多模态（文本、音频、视频、图像） | 仅文本 |
| **模型可用性** | 专有（Google API / AI Studio） | 开源（权重可用） |
| **最大输出 tokens** | 66K | 131K |
| **中位延迟（p50）** | ~1.28s | ~3.44s |
| **吞吐量（p50）** | ~39.0 tokens/s | ~38.0 tokens/s |

---

### 核心结构与功能差异

* **智能与基准评估：** Gemini 3.5 Flash 在整体基准测试中领先明显，在 Artificial Analysis 的智能指数上得分为 **55**，而 DeepSeek V4 Flash 为 **46**。Gemini 在核心编程能力和广泛的多步骤代理执行方面也优于 DeepSeek V4 Flash。
* **成本差异：** DeepSeek V4 Flash 提供了极高的成本效益。其输入价格大约是 Gemini 3.5 Flash 的 1/15，输出价格则接近 1/45。评估运营成本的开发者通常发现，DeepSeek 以极低的预算提供了不错的推理能力。
* **多模态能力：** Gemini 3.5 Flash 保留了 Google 原生的多模态处理优势，允许用户在其大上下文窗口内无缝解析视频、图像和音频。DeepSeek V4 Flash 则专注于纯文本数据集和代码结构。
* **输出限制与处理延迟：** DeepSeek V4 Flash 的最大输出 tokens 是 Gemini 3.5 Flash 的两倍（131K vs 66K），这对于生成长文本或复杂代码架构非常有利。然而，Gemini 3.5 Flash 的初始延迟更低（~1.28s vs ~3.44s），使其开始响应的速度明显更快。