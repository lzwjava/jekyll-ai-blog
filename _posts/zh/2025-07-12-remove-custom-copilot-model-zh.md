---
audio: false
generated: true
lang: zh
layout: post
title: GitHub Copilot移除自定义模型功能
translated: true
type: note
---

要在 Visual Studio Code (VS Code) 的 GitHub Copilot 扩展中移除模型，请注意：内置模型（如默认的 GitHub Copilot 模型）无法移除，因为它们是扩展的组成部分。但如果你指的是通过第三方提供商（例如 Anthropic、OpenAI、Google Gemini 或其他）使用自己的 API 密钥添加的自定义模型，则可以通过删除关联的 API 密钥和提供商详细信息来有效移除它。此功能目前处于预览阶段，可能尚未面向 Copilot Business 或 Enterprise 用户开放。

根据官方文档，操作步骤如下：

1. 在 VS Code 中打开 Chat 视图（如果尚未打开，可使用命令面板，快捷键为 `Ctrl+Shift+P` 或 macOS 上的 `Cmd+Shift+P`，然后搜索“Copilot: Open Chat”）。
2. 在 Chat 视图中，点击模型选择下拉菜单（位于输入框旁边）并选择 **管理模型**。或者，打开命令面板并运行 **GitHub Copilot: Manage Models** 命令。
3. 在管理模型界面中，将鼠标悬停在要移除模型对应的提供商上，点击齿轮图标以编辑其详细信息。
4. 从字段中删除 API 密钥（以及适用的任何端点 URL），然后保存更改。这应该会使该模型从选择器中移除。

如果遇到问题（例如，API 密钥字段未正确更新或清除，某些情况下这已被报告为错误），请先尝试以下解决方法：

- 在 Chat 视图的模型选择器中选择一个不同的模型，以取消选择你正在尝试移除的模型。
- 返回管理模型，编辑提供商，然后删除 API 密钥。

前提条件和注意事项：

- 这仅适用于聊天功能；不会影响代码补全或其他工具。
- 确保你的 Copilot 订阅允许访问多个模型（例如，个人版、专业版或为组织启用的预览功能）。
- 如果模型仍然存在或遇到错误，请重启 VS Code 或检查扩展更新。

如果这与你所说的“移除模型”不符（例如，如果你试图禁用整个扩展或隐藏 Copilot 功能），请进一步说明以获得更具体的步骤。
