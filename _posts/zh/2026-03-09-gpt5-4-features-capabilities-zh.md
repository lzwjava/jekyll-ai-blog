---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GPT-5.4 功能与能力详解
translated: true
type: note
---

## GPT-5.4：全面介绍

### 概述

GPT-5.4 是 OpenAI 最强大和最高效的用于专业工作的前沿模型，于 2026 年 3 月 5 日发布。它可在 ChatGPT（作为 GPT-5.4 Thinking）、API 和 Codex 中使用。它将 OpenAI 最近在推理、编码和代理工作流方面的最佳进展整合到一个前沿模型中。

它是第一个纳入 GPT-5.3-Codex 前沿编码能力的主体推理模型，OpenAI 将其命名为 GPT-5.4，以反映这一重大能力飞跃，并简化在使用 Codex 时模型的选择。

---

### 模型变体

GPT-5.4 有三个主要变体：

**1. GPT-5.4 (Standard / API)**
通过 API 以 `gpt-5.4` 形式提供，正在逐步在 ChatGPT 和 Codex 中推出。

**2. GPT-5.4 Thinking (ChatGPT)**
在 ChatGPT 中，GPT-5.4 Thinking 现在可以提供其思考的预先计划，因此用户可以在响应过程中调整方向，并在工作中到达更符合其需求的最终输出。此变体可供 ChatGPT 中的 Plus、Team 和 Pro 用户使用，而 Enterprise 和 Edu 客户可以启用早期访问。

**3. GPT-5.4 Pro**
GPT-5.4 Pro 是一个使用更多计算资源进行更深入思考并提供一致更好答案的版本。它仅在 Responses API 中可用，以支持在响应 API 请求之前进行多轮模型交互，以及其他高级 API 功能。GPT-5.4 Pro 通过 API 以 `gpt-5.4-pro` 形式提供，并在 ChatGPT 中供 Pro 和 Enterprise 计划用户使用。

---

### 关键能力

**推理与效率**
GPT-5.4 是 OpenAI 迄今为止最具 token 效率的推理模型，与 GPT-5.2 相比，使用显著更少的 token 来解决问题——这转化为减少的 token 使用量和更快的速度。

**编码**
GPT-5.4 融入了 GPT-5.3-Codex 的行业领先编码能力，提升了模型在工具、软件环境以及涉及电子表格、演示文稿和文档的专业任务中的工作方式。

**原生计算机使用**
在 Codex 和 API 中，GPT-5.4 是第一个发布时具备原生、最先进计算机使用能力的通用模型，使代理能够操作计算机并在应用程序中执行复杂工作流。它在 OSWorld-Verified Computer Use 基准上达到了 75%。

**长上下文窗口**
GPT-5.4 支持最多 100 万 token 的上下文，允许代理在长时段内规划、执行和验证任务。超过 272K 输入 token 的提示按全会话 2 倍输入和 1.5 倍输出来计价。

**工具搜索**
GPT-5.4 通过名为 Tool Search 的新功能改进了模型在大型工具和连接器生态系统中的工作方式，帮助代理更高效地找到并使用正确的工具，而不牺牲智能。

**专业知识工作**
在 GDPval 上——该基准测试代理在 44 种职业中产生规范良好的知识工作的能力——GPT-5.4 达到了新的最先进水平，在 83.0% 的比较中匹配或超过行业专业人士，而 GPT-5.2 为 70.9%。

---

### 幻觉与准确性改进

GPT-5.4 是 OpenAI 迄今为止最事实性的模型。在一组用户标记事实错误的去标识化提示上，GPT-5.4 的单个声明虚假的可能性降低了 33%，其完整响应的任何错误可能性降低了 18%，相对于 GPT-5.2。

---

### 安全功能

OpenAI 发布了关于监控模型推理过程的新安全研究，包括一个开源评估，旨在测试系统是否能隐藏其推理。该研究发现，GPT-5.4 Thinking 隐藏推理的能力较低，公司将其描述为积极的安全信号。

OpenAI 保留了用于 GPT-5.3-Codex 的相同高网络风险分类，并部署了额外保护措施，包括扩展的网络安全系统、监控工具、可信访问控制，以及在 Zero Data Retention 表面上针对更高风险活动的请求阻塞。

---

### 定价 (API)

标准 `gpt-5.4` 模型定价为 **每百万输入 token 2.50 美元** 和 **每百万输出 token 15 美元**。`gpt-5.4-pro` 模型定价为 **每百万输入 token 30 美元** 和 **每百万输出 token 180 美元**。

---

### 模型快照 / 版本

当前快照为 `gpt-5.4-2026-03-05`。快照允许开发者锁定模型的特定版本，从而使性能和行为随时间保持一致。

---

### 旧模型退役

GPT-5.2 Thinking 将在模型选择器中的 Legacy Models 部分继续供付费用户使用三个月，之后将于 2026 年 6 月 5 日退役。

---

### 总结表格

| 特性 | GPT-5.4 | GPT-5.4 Pro |
|---|---|---|
| Context Window | 1.05M tokens | 1.05M tokens |
| Computer Use | Native (first general-purpose) | Native |
| Reasoning Effort | none, low, medium, high, xhigh | medium, high, xhigh |
| API Price (Input) | $2.50 / 1M tokens | $30 / 1M tokens |
| API Price (Output) | $15 / 1M tokens | $180 / 1M tokens |
| ChatGPT Access | Plus, Team, Pro | Pro & Enterprise |

参考资料：

- [Introducing GPT-5.4 | OpenAI](https://openai.com/index/introducing-gpt-5-4/)
- [GPT-5.4 Model | OpenAI API Docs](https://developers.openai.com/api/docs/models/gpt-5.4)
- [GPT-5.4 Pro Model | OpenAI API Docs](https://developers.openai.com/api/docs/models/gpt-5.4-pro)
- [OpenAI launches GPT-5.4 | TechCrunch](https://techcrunch.com/2026/03/05/openai-launches-gpt-5-4-with-pro-and-thinking-versions/)
- [OpenAI announces GPT-5.4 | Neowin](https://www.neowin.net/news/openai-announces-gpt54-its-most-powerful-model-that-excels-at-professional-tasks/)
- [GPT-5.4 safety & release | Help Net Security](https://www.helpnetsecurity.com/2026/03/06/openai-chatgpt-gpt%E2%80%915-4-model-release/)
