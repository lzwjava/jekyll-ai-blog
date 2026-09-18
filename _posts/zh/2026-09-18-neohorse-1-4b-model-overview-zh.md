---
audio: false
generated: true
image: false
lang: zh
layout: post
title: NeoHorse-1-4B 模型概述
translated: true
type: note
---

**问题：** Hugging Face 上的 NeoHorse-1-4B 模型是什么？

**答案：**

NeoHorse-1-4B 是由 **TokenRhythm** 开发的一个约 40 亿参数的因果语言模型，于 2026 年 9 月发布。以下是关于它的概要：

**来源与基础模型**
它基于 **Qwen3.5-4B**（阿里云）进行后训练，并由 TokenRhythm 微调。本次发布仅包含语言模型权重，不包含视觉权重。重新打包更改了配置和张量键名，但未改变微调后的张量值。

**核心目标：递归自我改进（RSI）**
NeoHorse-1-4B 是迈向**递归自我改进（RSI）**的初始原型。路由框架将任务分配给异构模型池，记录工具交互和结果，评估能力需求，并使用能力级别的反馈来塑造下一轮训练混合。更新后的模型可以重新进入框架，形成原型评估–选择–更新的闭环。

**能力**
它专为以下任务设计：
基于文本的 **agent harnesses**、**tool use**、**coding** 和 **instruction following**。

**关键规格**

| 属性 | 值 |
|---|---|
| 参数 | ~4B |
| 上下文长度 | 262,144 tokens（可扩展至约 1M） |
| 格式 | Safetensors / BF16 |
| 许可证 | Apache 2.0 |

**性能**
它在十个基准测试上取得了 **64.87 宏平均分**，而基础模型 Qwen3.5-4B 为 58.94，提升了 **+5.93 分**。在 4B 类别的五个对比模型中，它总体排名最佳。

**参考链接：**
- [TokenRhythm/NeoHorse-1-4B on Hugging Face](https://huggingface.co/TokenRhythm/NeoHorse-1-4B)
- [技术报告 (arXiv:2609.08183)](https://arxiv.org/abs/2609.08183)
- [GitHub 仓库](https://github.com/TokenRhythm/NeoHorse)