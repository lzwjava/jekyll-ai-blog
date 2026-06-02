---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: GitHub Copilot扩展更新摘要
translated: true
type: note
---

### GitHub Copilot VS Code 扩展（版本 1.388.0）

GitHub Copilot 扩展 1.388.0 版本于 2025 年 10 月 24 日发布。这似乎是一个侧重于稳定性和兼容性改进的小幅更新，特别是针对最新 VS Code 版本（1.105）。市场或 GitHub 博客中未公开详细的具体发布说明，但用户报告表明修复了诸如内联生成期间不需要的代码插入和中止建议时的额外标签补全等问题。它与最近的 Copilot 功能无缝集成，包括增强的代理模式和模型选择。

#### 过去 6 个月的主要更新（2025 年 5 月至 10 月）
GitHub Copilot 的主要增强功能通常与每月 VS Code 发布同时宣布。以下是此期间扩展及相关功能的重要更新摘要：

- **2025 年 10 月（VS Code 1.105 / 扩展 ~1.388）**：
  - OpenAI Codex 集成现已在 VS Code Insiders 中提供给 Copilot Pro+ 订阅者，支持在编辑器中直接进行高级代码合成。
  - 新的“任务控制”界面，用于跨会话分配、引导和跟踪 Copilot 编码代理任务。
  - 代理会话视图扩展，支持 GitHub Copilot CLI 以管理本地和基于云的代理。

- **2025 年 9 月（VS Code 1.104 / 扩展 ~1.38x）**：
  - 实验性 GitHub Copilot-SWE 模型向 VS Code Insiders 推出，该模型针对代码编辑、重构和小型转换进行了优化。它以任务为中心，可在任何聊天模式下工作；建议使用详细提示以获得最佳效果。
  - 改进了终端错误的内联聊天，提供更好的解释和修复。

- **2025 年 8 月（VS Code 1.103 / 扩展 ~1.37x）**：
  - 增强了提交消息建议，具有多行上下文感知能力，并与 @workspace 集成以生成整个项目结构。
  - 轻量级内联聊天升级，无需打开完整视图即可进行更快的交互。

- **2025 年 7 月（VS Code 1.102 / 扩展 ~1.36x）**：
  - 通过单一提示更好地协调多文件编辑，分析项目结构以实现一致的更改。
  - 弃用了旧模型（部分 Claude、OpenAI 和 Gemini 变体），转而使用更新、更快的选项，如 GPT-4.1。

- **2025 年 6 月（VS Code 1.101 / 扩展 ~1.35x）**：
  - 引入了提示和指令文件，用于通过可重用的指南和组织知识自定义 Copilot 的行为。
  - 扩展了 GitHub Pull Requests 集成：直接从 VS Code 视图将 PR/问题分配给 Copilot，并新增“Copilot on My Behalf”查询以进行跟踪。

- **2025 年 5 月（VS Code 1.100 / 扩展 ~1.34x）**：
  - 代理模式增加了模型上下文协议（MCP）支持，允许为第三方模型使用自定义 API 密钥。
  - 由 OpenAI GPT-4.1 和 Anthropic Claude Sonnet 驱动的更快的代理编辑，尤其适用于大文件。
  - 仓库搜索改进，用于语义代码发现和全代码库范围的建议。

这些更新强调了代理工作流、模型性能以及与 VS Code 生态系统的无缝集成。有关完整的扩展历史，请查看 VS Code 市场。重大公告通常与 VS Code 的月度发布周期相关联。

[GitHub Copilot in VS Code gets upgraded](https://github.blog/changelog/2025-10-28-github-copilot-in-visual-studio-code-gets-upgraded/)
[Copilot-SWE model rolling out to Visual Studio Code Insiders](https://github.blog/changelog/2025-09-22-copilot-swe-model-rolling-out-to-visual-studio-code-insiders/)
[GitHub Copilot in VS Code April release (v1.100)](https://github.blog/changelog/2025-05-08-github-copilot-in-vs-code-april-release-v1-100/)
[GitHub Copilot in VS Code March release (v1.99)](https://github.blog/changelog/2025-04-03-github-copilot-in-vs-code-march-release-v1-99/)
[September 2025 (version 1.105) - Visual Studio Code](https://code.visualstudio.com/updates)
[GitHub Copilot Marketplace Page](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot)
