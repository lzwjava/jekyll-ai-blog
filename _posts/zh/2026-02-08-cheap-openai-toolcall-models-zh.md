---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-haiku
title: 支持工具调用的低成本 OpenAI 模型
translated: true
type: note
---

我将搜寻更经济实惠且仍支持 tool calling 的 OpenAI 模型选项。这是一个非常棒的问题！以下是支持 tool calling 的最佳低成本 OpenAI 模型：

## 支持 Tool Calling 的最经济选择

**GPT-4o Mini** — 价格为每百万 input tokens 15 美分，每百万 output tokens 60 美分，比 GPT-3.5 Turbo 便宜 60% 以上。它在 function calling 方面表现强劲，使开发者能够构建获取数据或与外部系统交互的应用程序。这是最具性价比的选择之一。

**GPT-4.1 Mini** — 擅长指令遵循和 tool calling，具有 1M token 的 context window，且在没有 reasoning step 的情况下具有低延迟（low latency）。它的能力比 GPT-4o Mini 更强，同时保持了成本效益。

**GPT-5.1 Codex Mini** — GPT-5.1-Codex 的一个更小、更经济、功能稍弱的版本，专门为需要 tool calling 支持且对预算敏感的 Codex 用户设计。

**o3-Mini** — 价格为每百万 input tokens 1.10 美元——低于 GPT-4.1 的 2.00 美元费率，使其成为最经济的 reasoning 选项。

## 适用于您的 config.toml

对于优先考虑成本效率且包含 tool calling 的自定义 provider 设置，我建议：
1. **GPT-4o Mini** 用于通用任务
2. **GPT-4.1 Mini** 如果您需要更好的指令遵循能力
3. **o3-Mini** 用于预算紧张且需要重度 reasoning 的任务

您的主要使用场景是什么？这是否有助于缩小最佳选择范围？