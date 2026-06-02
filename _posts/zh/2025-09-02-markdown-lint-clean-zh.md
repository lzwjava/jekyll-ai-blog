---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Markdown 语法检查确保文件规范整洁
translated: true
type: note
---

以下是 David Anson 对 **markdownlint** 项目的清晰易懂介绍：

---

## 什么是 **markdownlint**？

**markdownlint** 是一款基于 Node.js 的 Markdown/CommonMark 文件静态分析工具。其核心目标是强制执行 Markdown 内容的一致性和样式规则——帮助作者保持整洁统一的格式，并避免在不同解析器中可能破坏或渲染不一致的结构 ([GitHub][1])。

该工具受 Ruby 版 markdownlint (markdownlint/mdl) 启发，拥有丰富的 linting 规则库。它采用 micromark 解析器以支持 CommonMark，并扩展了 GitHub 风味 Markdown (GFM) 功能，包括表格、自动链接、指令、脚注和数学公式 ([GitHub][1])。

## 核心特性与集成

* **规则覆盖**：提供全面的内置规则集——涵盖标题样式、列表缩进、尾随空格和行长度等（例如 MD001、MD009、MD013…）([GitHub][1])。
* **生态兼容性**：

  * **命令行工具**：
    * `markdownlint-cli` – 传统 CLI 界面
    * `markdownlint-cli2` – 更快速的配置化 CLI，支持灵活格式化选项、通配符匹配、多输出格式、自动修复及 CI 工作流集成 ([GitHub][2], [GitHub][3])
  * **VS Code 扩展**：
    * `vscode‑markdownlint` 为编辑器提供实时 linting 功能。违规内容会以内联方式标记（下划线显示），支持悬停提示和快速修复建议 ([GitHub][4])
  * **GitHub Action**：
    * `markdownlint‑cli2‑action` 可将 markdownlint 嵌入 CI 流水线，在 GitHub 工作流中实现自动检查（及可选自动修复）([GitHub][5])

---

## 为什么使用它？

* **一致性**：确保 Markdown 文件遵循既定样式指南，减少项目中的格式偏差
* **编辑器辅助**：VS Code 等集成环境中的实时反馈让写作更清晰高效
* **自动化**：在 CI 流水线中配合 lint 工具或 GitHub Actions 使用，可在合并前强制执行标准
* **可定制性**：可通过配置文件或行内注释自定义规则集或禁用特定规则（例如禁用 MD013 以允许长行）([GitHub][5], [Software Recommendations Stack Exchange][6])

---

需要快速入门指南吗？可了解通过 npm 安装、使用 VS Code 扩展或集成到 CI 工作流的具体方法。

[1]: https://github.com/DavidAnson/markdownlint?utm_source=chatgpt.com "DavidAnson/markdownlint: A Node.js style checker and lint ..."
[2]: https://github.com/markdownlint/markdownlint?utm_source=chatgpt.com "Markdown lint tool"
[3]: https://github.com/DavidAnson/markdownlint-cli2?utm_source=chatgpt.com "DavidAnson/markdownlint-cli2"
[4]: https://github.com/DavidAnson/vscode-markdownlint?utm_source=chatgpt.com "DavidAnson/vscode-markdownlint: Markdown linting and ..."
[5]: https://github.com/DavidAnson/markdownlint-cli2-action?utm_source=chatgpt.com "DavidAnson/markdownlint-cli2-action"
[6]: https://softwarerecs.stackexchange.com/questions/7138/markdown-lint-tool?utm_source=chatgpt.com "validation - Markdown lint tool"
