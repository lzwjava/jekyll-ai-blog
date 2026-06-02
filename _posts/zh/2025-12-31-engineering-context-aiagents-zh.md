---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: AI Agent 的工程背景
translated: true
type: note
---

Question: What is the content of the blog post at <https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus>?

Answer:

# Context Engineering for AI Agents: Lessons from Building Manus

**Author:** Yichao "Peak" Ji
**Date:** July 18, 2025

这篇博客分享了关于 "context engineering"（上下文工程）的实践经验——这是一门精心塑造 Large Language Models (LLMs) 输入上下文的艺术。这些经验源于作者构建 **Manus** 的过程，Manus 是一个能够执行复杂计算机任务的通用自主 AI Agent。

## Introduction

Manus 团队决定利用尖端 LLMs 的 in-context learning 能力来构建他们的 Agent（而不是采取 fine-tuning 开源模型的方式），以便实现快速迭代并受益于持续的模型改进。这种方法要求必须精通 context engineering，这也导致了 Agent 框架在反复试错中经历了四次全面重写（幽默地被称为 "Stochastic Graduate Descent"）。本文概述了在此过程中发现的关键原则。

## Key Lessons

### 1. Design Around the KV-Cache

KV-cache 命中率是生产环境 AI Agent 最关键的指标，因为 Agent 的 input-to-output token 比例非常高（例如 Manus 中达到了 100:1）。重用缓存的 prefix 可以显著降低延迟和成本。

Best practices:

- 保持 prompt prefix 完全稳定（避免使用时间戳等动态元素）。
- 使上下文保持严格的 append-only（仅追加）模式，并使用确定性的 serialization。
- 在不可避免发生变化时，显式标记 cache breakpoints。

### 2. Mask, Don't Remove

在上下文中动态添加或删除 tool 会导致 KV-cache 失效，并可能使模型产生困惑。相反，应保留所有定义的 tool，但使用 logit masking（通过 function calling 中的 prefill 模式）来强制执行或阻止特定操作。使用一致的名称前缀对 tool 进行分组有助于高效管理可用性。

### 3. Use the File System as Context

由于观测数据巨大、性能下降以及成本问题，长上下文窗口对于真实的 Agent 任务来说仍然是不够的。将本地文件系统视为无限的外部 memory：Agent 读写文件，存储 URL 或路径而非完整内容，从而实现上下文的无损“压缩”。

### 4. Manipulate Attention Through Recitation

对于长时间运行的任务，Agent 维护一个 `todo.md` 文件来背诵（recite）当前目标。这使得高层计划始终处于最近的上下文中，从而应对 "lost-in-the-middle" 问题。

### 5. Keep the Wrong Stuff In

不要隐藏或清理错误和失败的操作。在上下文中保留失败记录（包括 stack traces）可以让模型从中学习并避免重复错误，这是真正的 Agent 行为特征。

### 6. Don't Get Few-Shoted

统一的 few-shot 示例可能会导致 Agent 过度模仿模式，从而在重复任务中产生偏移或 hallucination。引入结构化的变体（不同的措辞、serialization、微小的噪声）以维持多样性。

## Conclusion

Context engineering 是 AI Agent 领域一门新兴但至关重要的学科。它决定了速度、稳健性、恢复能力和可扩展性。Manus 的经验强调了深思熟虑的上下文塑造，而非仅仅依赖更大的模型。Agent 的未来将通过“一次一个上下文”地构建出来。

References:

- [Original blog post](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)
