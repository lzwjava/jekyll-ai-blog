---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Claude Code 源码泄露详情
translated: true
type: note
---

问题：如何查看 Claude Code 源码泄露的相关信息？

回答：据报道，Anthropic 的 **Claude Code**（官方 CLI 工具）源代码于 **2026年3月31日** 泄露。此次泄露源于 npm registry 上 `@anthropic-ai/claude-code` 包中暴露的一个 `.map` (source map) 文件。

虽然你链接的原始仓库 (`instructkr/claude-code`) 被描述为一个受泄露事件启发而开发的 **Python feature port** 和工作空间，但实际的泄露细节和证据可以通过以下迹象找到：

### 1. 泄露源 (npm)
此次泄露是由安全研究员 **Chaofan Shou (@Fried_rice)** 发现的。他在官方 npm 包中发现了一个 `cli.js.map` 文件（约 60MB）。该 source map 包含了对原始、未混淆的 TypeScript 源代码的引用，随后这些代码被镜像到各个 GitHub 仓库中。

### 2. 泄露代码中的证据
泄露的代码库（估计约 512,000 行代码）包含了一些“放飞自我”且未发布的功能，确认了其作为 Anthropic 内部代码的真实性：
* **"Buddy" 系统：** 终端内部一个隐藏的拓麻歌子风格宠物系统，会根据你的 user ID 孵化出一个 ASCII 同伴（如鸭子、水豚或龙）。
* **Undercover Mode：** 当 Anthropic 员工向公共仓库贡献代码时，该功能会自动隐藏 AI 痕迹（如 `Co-Authored-By` 行）。
* **内部代号：** 代码中将项目称为 **"Tengu"**，并提到了未来的模型版本，如 **"Fennec"** (Opus 4.7) 和 **"Sonnet 4.8"**。
* **"Dream" 系统：** 一个每 24 小时触发一次的后台进程，用于“整合”和整理会话记忆。

### 3. Repository 结构
泄露的 `src/` 目录通常包括：
* `src/tools/`：`BashTool`、`FileEditTool` 和 `YOLO classifier`（一种自动化权限系统）等工具的实现。
* `src/commands/`：Slash commands，如 `/commit`、`/review` 和 `/compact`。
* `src/bridge/`：用于 IDE extensions (VS Code/JetBrains) 的通信层。

References:
* [Claude Code — Leaked Source (2026-03-31) - GitHub](https://github.com/nirholas/claude-code)
* [Anthropic's Claude Code source leaked via npm - PiunikaWeb](https://piunikaweb.com/2026/03/31/anthropic-claude-code-source-leaked-npm-registry/)
* [I dug through Claude Code's leaked source - Reddit](https://www.reddit.com/r/ClaudeAI/comments/1s8lkkm/i_dug_through_claude_codes_leaked_source_and/)