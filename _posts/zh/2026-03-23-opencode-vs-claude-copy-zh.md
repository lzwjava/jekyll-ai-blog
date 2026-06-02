---
audio: false
generated: true
image: false
lang: zh
layout: post
title: OpenCode 导出与 Claude 复制的比较
translated: true
type: note
---

**Question:** 这里的分析在比较 OpenCode 的 `/export`（会话转录）功能与 Claude Code 的 `/copy` 按钮时是否准确 —— 特别是关于 OpenCode 导出完整的 Agentic "journey"（旅程），而 Claude Code 仅复制最后一次回复的描述？

**Answer:**

你的分析**基本正确**，但根据这两个工具的实际文档记录，有一些细节需要完善。

---

## OpenCode 的 `/export` 命令

OpenCode 的 TUI 提供了一个 `/export` 命令，可以将当前对话导出为 Markdown，并在你的默认编辑器中打开（使用 `$EDITOR` 环境变量）。

导出对话框（`DialogExportOptions`）允许用户设置输出文件名（默认为 `session-<id-prefix>.md`），切换是否包含 thinking blocks、tool 详情及 assistant 元数据，并可选择仅在 `$EDITOR` 中打开而不写入磁盘。

因此，这确实是一个**完整的、结构化的会话导出** —— 而不仅仅是最后一轮对话。细粒度的开关（thinking blocks、tool 详情、元数据）证明它捕捉了整个 Agentic 过程，而非仅仅是最终结果。

---

## Claude Code 的 `/copy` 命令

Claude Code 的行为比简单的“复制最后一次回复”更复杂一些：

Claude Code 的 `/copy` 命令会将 Claude 最近的一次回复复制到剪贴板。如果回复中包含 code blocks，你会看到一个交互式选择器，可以抓取单个代码块而不是全文。你还可以传入一个数字来回溯 —— 例如 `/copy 2` 抓取倒数第二次回复。

然而，Claude Code **确实**也提供了一个完整的导出选项：

Claude Code 中的 `/export` 命令会将完整对话以纯文本形式直接写入磁盘 —— 没有提示，没有对话框。导出的内容仅限纯文本，没有 JSON，没有结构化格式。它仅仅是一个转录文本。

关键区别在于 Claude Code 的 UI 中没有显著的内置导出按钮；对话以 JSONL 文件形式存储在 `~/.claude/projects/` 中。这导致开发者们构建了第三方工具来弥补这一空缺。

---

## 核心区别

你的核心观点依然成立：

| 功能 | OpenCode `/export` | Claude Code `/copy` |
|---|---|---|
| **范围** | 完整会话，所有轮次 | 最后一次回复（或前 N 次） |
| **格式** | 带有开关的结构化 Markdown | 纯文本或剪贴板 |
| **Tool 详情** | 可选（thinking blocks, tool calls） | 默认不包含 |
| **Thinking 追踪** | 可选 | 默认隐藏；手动复制终端会话时不会包含 thinking 追踪 |
| **设计理念** | 一等公民级的 TUI 导出对话框 | 针对单次回复的剪贴板辅助工具 |

来自 Claude Code 会话的转录捕捉了极其重要的 Context —— 包括提出了什么要求、Claude 建议了什么、做出了哪些决定，以及 Claude 在实现功能时为其决策提供的辩护。社区显然非常看重这一点，这正是为什么像 `claude-code-transcripts`（由 Simon Willison 开发）之类的工具会被创建，以弥补 Claude Code 缺乏完善内置导出流程的不足。

---

## 对你描述的一个修正

OpenCode **并非**如所述基于 Zig 或 "OpenTUI/Zig" 构建。OpenCode 的交互式 TUI 是使用 Bubble Tea（一个 Go 框架）构建的，旨在提供流畅的终端体验，并且它支持多个 AI Provider，包括 Anthropic Claude, OpenAI, Google Gemini, AWS Bedrock, Groq, Azure OpenAI, 和 OpenRouter。

因此：**功能对比是准确的**，但架构描述（Zig/OpenTUI）有误 —— OpenCode 是一个 Go + Bubble Tea 项目。

**References:**

- [OpenCode TUI Documentation](https://opencode.ai/docs/tui/)
- [OpenCode TUI Commands — DeepWiki](https://deepwiki.com/anomalyco/opencode/9.2-tui-commands)
- [OpenCode GitHub (opencode-ai/opencode)](https://github.com/opencode-ai/opencode)
- [Claude Code Export Guide — kentgigger.com](https://kentgigger.com/posts/claude-code-export-save-conversation)
- [Simon Willison: A new way to extract detailed transcripts from Claude Code](https://simonwillison.net/2025/dec/25/claude-code-transcripts/)
- [ZeroSumQuant/claude-conversation-extractor](https://github.com/ZeroSumQuant/claude-conversation-extractor)
