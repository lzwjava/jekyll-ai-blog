---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 'Claude Code: 根目录权衡'
translated: true
type: note
---

问题：当从根目录（`/`）启动 Claude Code 时，能否使用 `@` 直接引用所有项目中的文件，而无需复制路径？从 `/` 运行是否会变慢？

回答：

是的，你的直觉是正确的——并且确实存在需要理解的权衡。

## Claude Code 中 `@` 的工作方式

当你在提示中使用 `@` 引用文件时，Claude Code 会将该文件的内容直接包含到对话上下文中。文件路径可以是相对路径或绝对路径，你可以在输入 `@` 后使用 **tab-completion**（Tab 补全）快速导航和选择文件，无需输入完整路径。

`@` 引用语法允许你快速将文件内容添加到上下文中，而无需让 Claude 自行查找并读取文件（后者通常需要更长时间）。

因此，是的——如果你从 `/` 启动，你可以通过 tab-completion `@` 系统上的任何文件，无需从外部复制路径。

## 从 `/` 运行是否会变慢？

**简短回答：是的，明显会更慢。** 原因如下：

### 1. `@` 自动补全使用 ripgrep 扫描目录

如果 `@` 文件引用找不到文件，问题可能出在捆绑的 ripgrep 二进制文件上。Claude Code 使用 ripgrep 来驱动文件搜索和 `@` 自动补全。从 `/` 启动意味着每次你输入 `@something` 时，ripgrep 都必须索引**整个文件系统**，这会非常慢。

### 2. 文件选择器变慢是一个已知问题

如果你的项目是一个大型 monorepo，默认文件选择器速度很慢，你可以通过 `settings.json` 中的 `fileSuggestion` 设置将其替换为自定义命令：

```json
{
  "fileSuggestion": {
    "type": "command",
    "command": "~/.claude/file-suggestion.sh"
  }
}
```

该命令通过标准输入（stdin）接收包含 `query` 字段的 JSON，并输出以换行符分隔的文件路径。

### 3. `@` 自动补全变慢也是一个已确认的 bug

有一个已知的报告问题：使用 `@` 输入文件曾经很迅速，但现在匹配文件的出现需要将近一秒钟——而且这还是发生在**普通项目目录**中，而不是从 `/` 启动。如果从 `/` 启动，情况会更糟。

### 4. 上下文窗口很快被填满

上下文窗口是需要管理的最重要资源。单次调试会话或代码库探索可能会生成并消耗数万个 token。随着上下文被填满，LLM 的性能会下降——Claude 可能会开始“遗忘”早期的指令或犯更多错误。

## 更好的替代方案：使用 `--add-dir`

与其从 `/` 运行，不如**在你的主要项目内部**启动 Claude Code，并根据需要添加其他项目目录：

Claude Code 的多目录支持允许你使用 `--add-dir` 标志在单个会话中跨多个目录工作：

```bash
claude --add-dir /path/to/backend --add-dir /path/to/frontend
```

这样你无需切换会话就能在前端、后端和共享模块之间工作，同时保持良好的性能。

## 总结

| 方法 | 跨项目 `@` 引用 | 性能 |
|---|---|---|
| 从 `/` 启动 | ✅ 可以引用所有内容 | ❌ 自动补全极慢，ripgrep 范围巨大 |
| 从项目启动 + `--add-dir` | ✅ 显式多目录访问 | ✅ 快速，搜索范围受限 |
| 仅从项目目录启动 | ❌ 仅限于一个项目 | ✅ 最快 |

**建议：** 对于跨项目工作，使用 `--add-dir`。它提供了从多个项目引用文件的相同便利性，同时避免了从 `/` 扫描带来的性能损失。

参考资料：

- [Claude Code 文件引用指南 - Steve Kinney](https://stevekinney.com/courses/ai-development/referencing-files-in-claude-code)
- [Claude Code 最佳实践 - Anthropic 文档](https://code.claude.com/docs/en/best-practices)
- [Claude Code 故障排除 - Anthropic 文档](https://code.claude.com/docs/en/troubleshooting)
- [Claude Code 设置参考](https://claudefa.st/blog/guide/settings-reference)
- [多目录支持 - Apidog](https://apidog.com/blog/claude-code-multi-directory-support/)
- [`@` 文件自动补全变慢 - GitHub 问题](https://github.com/anthropics/claude-code/issues/2078)
