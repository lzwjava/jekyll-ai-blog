---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 开源助手代理说明书
translated: true
type: note
---

问题：在 OpenCode（或开源助手）中，什么相当于 CLAUDE.md？

回答：
在 2026 年的开源和智能 IDE 生态中，相当于 `CLAUDE.md` 的是 **`AGENTS.md`**。

虽然 Anthropic 通过 `CLAUDE.md` 普及了这一概念，但开源社区及多个“开源”替代方案（如 **OpenCode**、**Continue** 和 **Aider**）已围绕 `AGENTS.md` 形成共识，将其作为全局和项目特定指令的供应商中立标准。

### 1. 标准：`AGENTS.md`
该文件作为任何 AI agent 与你的代码库交互时的“单一事实来源”。大多数开源工具现已支持类似 `.gitignore` 工作的分层发现流程：
* **全局规则：** 位于 `~/.config/agents/AGENTS.md`（或类似的家目录路径）。这些规则适用于你打开的每个项目。
* **项目规则：** 位于项目根目录（`./AGENTS.md`）。这些规则会覆盖该特定仓库的全局规则。
* **作用域规则：** 某些工具（如 OpenCode）允许在子目录中使用 `AGENTS.md` 文件，为特定模块（例如前端与后端）提供上下文。

### 2. 特定工具等效文件
如果你正在使用特定的开源或热门 Claude Code 替代方案，以下是它们寻找“全局规则”的位置：

| 工具 | 主要配置文件 | 支持 `AGENTS.md` 吗？ |
| :--- | :--- | :--- |
| **OpenCode** | `OPENCODE.md` 或 `.opencode/rules.md` | **是**（原生后备） |
| **Continue** | `.continue/config.json`（系统提示） | 通过自定义上下文提供者 |
| **Aider** | `.aider.conf.yml` 或 `.aider.instructions.md` | **是** |
| **Cursor** | `.cursor/rules/*.mdc` | 部分（作为参考读取） |
| **Cline / Roo Code** | `.clinerules` | **是** |

### 3. 应在“全局规则”中包含哪些内容
无论文件名是什么，你的等效文件都应遵循相同的 Markdown 结构以确保有效：
* **风格与惯例：**（例如：“始终使用函数组件”、“优先使用 TypeScript 而非 JS。”）
* **技术栈：** 库的特定版本，以避免 AI 猜测过时的 API。
* **禁止模式：**（例如：“绝不使用 `any`”、“不要使用 Barrel 导出。”）
* **工作流钩子：** 构建和测试命令（例如：`## 命令 - 测试: npm test`）。

### 4. 为什么使用 `AGENTS.md`？
在 OpenCode 中使用 `AGENTS.md` 标准允许你保持 **LLM 无关性**。如果你将后端从 Claude 切换到 GPT-5 或本地的 Llama 4 模型，agent 仍将读取相同的规则集，而无需你手动重命名文件或在 UI 中更新系统提示。

参考文献：
* [如何配置每个 AI 编程助手：CLAUDE.md、AGENTS.md、Cursor Rules 等指南](https://www.deployhq.com/blog/ai-coding-config-files-guide)
* [Claude Code 概述 - 使用 CLAUDE.md 进行自定义](https://code.claude.com/docs/en/overview)
* [2026 年 Cursor 替代方案 - Builder.io](https://www.builder.io/blog/cursor-alternatives-2026)
