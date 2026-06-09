---
audio: false
generated: true
image: false
lang: zh
layout: post
title: VS Code中的Copilot部分开源
translated: true
type: note
---

问题：VS Code 中的 Copilot 是否开源？

答案：**部分开源。** VS Code 中 GitHub Copilot 的前端和客户端集成是开源的，但实际的 AI 模型和后端服务仍然是**闭源的**。

微软和 GitHub 已将扩展的代码库转为 MIT 许可证下的开源模式，并将代码直接迁移到主流的开源 VS Code 核心仓库中。

以下是具体哪些部分开源、哪些闭源：

### 开源部分

* **用户体验和客户端扩展**：负责 VS Code 中用户界面、聊天窗口、内联编辑界面以及提示管理的客户端代码完全开源。
* **提示工程逻辑**：你可以查看仓库，了解你的上下文是如何收集的、在发送给 AI 之前提示是如何构建的，以及收集了哪些遥测数据。

### 闭源部分

* **AI 模型**：Copilot 使用的实际底层大语言模型（LLM），例如来自 OpenAI、Anthropic 和 Google 的模型，均为专有且闭源。
* **后端服务**：处理 AI 请求并将数据返回给编辑器的云基础设施和专有后端系统完全闭源。
* **订阅模式**：尽管客户端软件是开源的，但使用官方服务仍需一个 GitHub Copilot 账户（不过提供了有限的“Copilot Free”免费层级）。

参考来源：

* [Visual Studio Code FAQ](https://code.visualstudio.com/docs/supporting/FAQ)
* [开源 AI 编辑器：第一个里程碑 - Visual Studio Code](https://code.visualstudio.com/blogs/2025/06/30/openSourceAIEditorFirstMilestone)