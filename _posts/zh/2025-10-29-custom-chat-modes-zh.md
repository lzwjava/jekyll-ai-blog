---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: GitHub Copilot自定义聊天模式
translated: true
type: note
---

### 什么是 chatmode.md？

在 Visual Studio Code（VS Code）的 GitHub Copilot 扩展中，`chatmode.md` 文件用于定义**自定义聊天模式**。这些模式允许你配置 Copilot Chat，使其采用特定角色或行为，以用于规划、安全审查或代码实现等任务。每种模式可以指定指令、可用工具（例如搜索、获取或 GitHub 仓库访问权限），甚至使用的 AI 模型。截至 VS Code 1.101，此功能处于预览阶段，有助于根据你的工作流程定制响应，以保持一致性。

自定义模式以 Markdown 文件形式存储，扩展名为 `.chatmode.md`，可以位于工作区（供团队共享）或用户配置文件中（供个人重复使用）。

### 为什么使用自定义聊天模式？
- **定制响应**：强制执行指南，例如生成计划而不编辑代码。
- **工具控制**：在规划时限制工具为只读，或在实现时启用编辑功能。
- **效率提升**：为常见角色（如架构师、审查员）重复使用设置。

### 如何创建 chatmode.md 文件

1. 在 VS Code 中打开**聊天视图**：
   - 点击标题栏中的 Copilot Chat 图标，或使用 `Ctrl+Alt+I`（Windows/Linux）或 `Cmd+Option+I`（macOS）。

2. 在聊天视图中，点击**配置聊天 > 模式**，然后选择**创建新的自定义聊天模式文件**。或者，打开命令面板（`Ctrl+Shift+P` / `Cmd+Shift+P`）并运行**Chat: New Mode File**。

3. 选择保存位置：
   - **工作区**：默认保存到 `.github/chatmodes/` 目录（可与团队共享）。可通过 `chat.modeFilesLocations` 设置自定义文件夹。
   - **用户配置文件**：保存到你的配置文件文件夹，以便跨设备同步。

4. 为文件命名（例如 `planning.chatmode.md`）并在 VS Code 中编辑。

要管理现有模式，请使用**配置聊天 > 模式**或**Chat: Configure Chat Modes**命令。

### 文件结构与语法

`.chatmode.md` 文件使用 Markdown 格式，并可选择包含 YAML 前言用于元数据。以下是基本结构：

- **YAML 前言**（用 `---` 行包围，可选）：
  - `description`：在聊天输入框占位符和下拉悬停提示中显示的简短文本。
  - `tools`：工具名称数组（例如 `['fetch', 'search']`）。可使用内置工具（如 `githubRepo`）或扩展工具；通过**配置工具**进行设置。
  - `model`：AI 模型（例如 `"Claude Sonnet 4"`）。默认为你选择的模型。

- **正文**：用于 AI 的 Markdown 指令，包括提示、指南或指向外部文件的链接。

工具优先级：提示文件 > 引用的模式 > 默认模式工具。

### chatmode.md 文件示例

以下示例创建一个“规划”模式，用于生成实现计划而不进行代码更改：

```
---
description: 为新功能或重构现有代码生成实现计划。
tools: ['fetch', 'githubRepo', 'search', 'usages']
model: Claude Sonnet 4
---
# 规划模式指令

你处于规划模式。你的任务是为新功能或重构现有代码生成实现计划。不要进行任何代码编辑——仅生成计划。

计划包含一个 Markdown 文档，包含以下部分：

* **概述**：功能或重构的简要描述。
* **需求**：需求列表。
* **实现步骤**：详细的实现步骤。
* **测试**：用于验证的测试列表。
```

保存文件后，它将出现在聊天模式下拉菜单中。

### 如何使用自定义聊天模式

1. 打开**聊天视图**（如上所述）。

2. 在聊天视图顶部的下拉菜单中（模式选择器旁边），选择你的自定义模式（例如“规划”）。

3. 模式的 `description` 将作为占位文本显示在输入框中。输入你的提示（例如“规划用户认证功能”）。

4. Copilot 将按照模式的指令和工具进行响应。你可以随时通过下拉菜单切换模式——内置模式（提问、编辑、代理）仍然可用。

更多示例请查看 [Awesome Copilot 仓库](https://github.com/github/awesome-copilot/tree/main)中的社区贡献。

### 参考资料
- [VS Code 中的自定义聊天模式](https://code.visualstudio.com/docs/copilot/customization/custom-chat-modes)
- [在 VS Code 中开始使用聊天功能](https://code.visualstudio.com/docs/copilot/chat/copilot-chat)
