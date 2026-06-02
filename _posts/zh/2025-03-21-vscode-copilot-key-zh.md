---
audio: false
generated: true
lang: zh
layout: post
title: Visual Studio Code Copilot 插件
translated: true
type: note
---

不，Visual Studio Code（VSCode）的 Copilot 插件无法使用自定义 API 密钥，例如您的 Gemini 密钥。GitHub Copilot 由 GitHub（微软旗下）开发，是一款基于 AI 的代码补全工具，深度集成于 GitHub 的基础设施及其特定的 AI 模型（最初基于 OpenAI 的 Codex）。它需要通过 GitHub 账户和 Copilot 订阅进行身份验证，并且没有提供内置选项来配置其他供应商（如 Google 的 Gemini）的自定义 API 密钥。

不过，既然您拥有 Gemini 密钥，仍有替代方法可以在 VSCode 中利用它：

- **Gemini Code Assist**：Google 提供了一款名为 Gemini Code Assist 的 AI 编程助手，其官方扩展支持 VSCode。该扩展专为与 Google 的 Gemini 模型配合工作而设计，很可能允许您输入 Gemini API 密钥进行身份验证。您可以从 VSCode 应用市场安装此扩展，并使用您的密钥进行配置，从而获得由 Gemini 驱动的代码补全功能。

- **第三方插件**：市场上可能还有其他第三方 VSCode 扩展支持多种 AI 供应商，并允许您使用包括 Gemini 在内的自定义 API 密钥。这些插件可以让您连接到 Gemini API 以获取代码建议，尽管可能需要额外的设置。

### 为何 Copilot 不支持自定义密钥
GitHub Copilot 是一款专有工具，为其自身生态系统进行了优化。尽管近期的发展显示 GitHub 与 Google 合作将 Gemini 模型集成到 Copilot 中，但该集成由 GitHub 管理，不允许用户直接输入自己的 Gemini API 密钥。相反，对任何支持的模型（包括 Gemini，如果可用）的访问都是通过 Copilot 服务本身在 GitHub 的控制下提供的。

### 实用建议
如果您的目标是在 VSCode 中使用您的 Gemini 密钥，安装 **Gemini Code Assist 扩展**是最直接且官方支持的选择。您可以按以下步骤操作：

1. 打开 VSCode。
2. 进入扩展视图（Windows/Linux 使用 `Ctrl+Shift+X`，macOS 使用 `Cmd+Shift+X`）。
3. 搜索 “Gemini Code Assist”（或查阅 Google 官方文档以确认确切名称）。
4. 安装扩展，并按照其设置说明输入您的 Gemini API 密钥。

这种方法确保您按预期使用工具，避免潜在问题，如违反服务条款或处理对 Copilot 的不受支持的修改。

总之，虽然 VSCode 的 Copilot 插件本身无法使用您的 Gemini 密钥，但您仍然可以通过选择 Gemini Code Assist 扩展或兼容的第三方插件，在 VSCode 中使用 Gemini 来实现您的目标。
