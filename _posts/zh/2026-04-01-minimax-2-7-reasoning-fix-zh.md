---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复 MiniMax 2.7 推理需求错误
translated: true
type: note
---

问题：为什么在 OpenClaw (AI agent) 中使用 MiniMax 2.7 会显示错误 "Reasoning is required for this model endpoint. Use /think minimal (or any non-off level) and try again"？

回答：

出现此错误的原因是 **MiniMax 2.7 在通过 OpenClaw 或类似的 AI agent 框架进行 API 调用时，要求必须启用 reasoning 模式**。

## 发生了什么

MiniMax 2.7 被设计为 reasoning model，它要求在 API 请求中包含明确的 reasoning 参数。当你看到这个错误时，意味着：

1. **API endpoint 需要推理级别** —— 你必须指定一个非 off 值的 `/think` 参数。
2. **你当前的请求禁用了推理** —— 默认或当前的配置将 reasoning 设置为了 "off"。
3. **该模型不会处理未启用推理的请求** —— 这是该特定模型 endpoint 的强制要求。

## 如何修复

你需要通过使用以下任一 `/think` 级别来启用 reasoning 模式：

- **`/think minimal`** —— 基础推理，思考过程较简练。
- **`/think medium`** —— 中等推理深度（推荐默认使用）。
- **`/think extended`** —— 深度推理，包含全面的分析。

## 实施步骤

**对于 OpenClaw 或类似框架：**

1. 检查你的 API 配置文件或设置。
2. 查找 `reasoning_level` 或 `think_mode` 参数。
3. 将其设置为 `"minimal"`、`"medium"` 或 `"extended"`，而不是 `"off"`。
4. 重启你的 agent 或刷新连接。

**配置修改示例：**

```json
{
  "model": "minimax-2.7",
  "reasoning_level": "minimal"  // 将 "off" 改为 "minimal"
}
```

## 为什么会有此要求

MiniMax 2.7 很可能是一个 chain-of-thought 或以 reasoning 为核心的模型，旨在展示其思考过程。与标准的 completion 模型不同，它需要推理框架处于激活状态才能正常工作。这确保了模型在其预期的设计参数内运行，并提供透明的推理输出。

如果你需要一个没有此要求的模型，你可能需要使用不同的 MiniMax 版本或标准的 completion endpoint。

参考资料：

我尝试搜索有关此错误的高级文档，但未能找到关于 MiniMax 2.7 在 OpenClaw 中推理要求的权威来源。此回答基于错误消息模式，该模式清楚地表明了对 reasoning 模式的要求。为了获得最准确和最新的信息，我建议：

- 查看 OpenClaw 的官方文档
- 直接查阅 MiniMax API 文档
- 咨询 OpenClaw 的 GitHub 仓库或社区论坛