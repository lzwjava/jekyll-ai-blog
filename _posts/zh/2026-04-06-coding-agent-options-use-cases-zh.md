---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 编码代理选项与应用场景
translated: true
type: note
---

基于 `coding-agent` 技能，我有以下几种可用工具：

- **Claude Code** — 大多数任务的首选（Anthropic 的命令行工具，无需 PTY，仅需 `--print --permission-mode bypassPermissions` 参数）
- **Codex** — OpenAI 的命令行工具，表现良好但需要 `pty:true`
- **OpenCode** / **Pi** — 替代方案，同样需要 PTY

对于多数编码工作，我会选择 **Claude Code** — 它最直接便捷，因为无需 PTY。进行快速编辑或阅读代码时，我直接使用内置工具（`edit`、`read`、`exec`）。只有当任务需要实际文件探索、跨多文件重构或从零开始构建新内容时，我才会委托给智能体执行。

你想解决什么问题？
