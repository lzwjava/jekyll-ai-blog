---
audio: false
generated: true
image: false
lang: zh
layout: post
title: DeepSeek成本对比：Flash与Pro
translated: true
type: note
---

**问题：** DeepSeek V4 Flash 在 OpenRouter 上是否比 DeepSeek V4 Pro 便宜约4倍？

**答案：**

并非精确的4倍——实际上是**约3.1倍便宜**，接近但并非正好4倍。具体细分如下：

| 模型 | 输入（$/百万 tokens） | 输出（$/百万 tokens） | 激活参数量 |
| --- | --- | --- | --- |
| DeepSeek V4 Pro | $0.435 | $0.870 | 49B |
| DeepSeek V4 Flash | $0.140 | $0.280 | 13B |
| **比例** | **3.1x** | **3.1x** | **3.8x** |

因此，输入和输出的比例一致为**3.1倍**。你的大致印象没错——“约4倍”是一个合理的心理模型，但精确数值约为3倍。

**你需要在以下方面权衡：**

- Flash：总计284B / **激活13B** — 快速、便宜，适合编码助手和 agent 循环
- Pro：总计1.6T / **激活49B** — 推理能力更强，在复杂数学/代码上表现更好，支持1M上下文及混合注意力

对于你的使用场景——日常AI助手、CLI agent、代码迭代——Flash 是可靠的默认选择。将 Pro 保留给那些确实需要额外推理余量的任务（复杂多文件重构、困难算法问题、长上下文分析）。你很可能只需将80%的流量路由到 Flash，就能将每天8美元的费用降至约2.50美元。

**参考链接：**

- [OpenRouter 上的 DeepSeek V4 Pro](https://openrouter.ai/deepseek/deepseek-v4-pro)
- [OpenRouter 上的 DeepSeek V4 Flash](https://openrouter.ai/deepseek/deepseek-v4-flash)
