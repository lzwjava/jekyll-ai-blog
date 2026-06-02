---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 禁用 Claude 代码计费标头
translated: true
type: note
---

问题：Claude Code 的 `settings.json` 中的 `"CLAUDE_CODE_ATTRIBUTION_HEADER": "0"` 是什么意思？

答案：问题：Claude Code 的 `settings.json` 中的 `"CLAUDE_CODE_ATTRIBUTION_HEADER": "0"` 是什么意思？

答案：

## `CLAUDE_CODE_ATTRIBUTION_HEADER` 到底是什么

这是一个**未文档化但真实的环境变量**，它控制 Claude Code 是否在每个 API 请求中发送一个名为 `x-anthropic-billing-header` 的特殊计费/跟踪 header。

### Header 的样子

从 Claude Code 版本 2.1.36 开始，Claude Code 在每个请求中发送一个特殊的 header，它每次请求都会变化。样子如下：
```
x-anthropic-billing-header: cc_version=xxxx; cc_entrypoint=cli; cch=xxxx;...
```

### Header 的用途

默认情况下，Claude Code 在每个请求中发送这个计费归属 header — `x-anthropic-billing-header`。当你直接调用 Anthropic 的实际 API 时，这是有意义的：他们需要跟踪使用情况。但当你将 Claude Code 指向本地模型或 relay proxy 时，这个 header 仍然会被发送，你的服务器必须处理它 — 每个请求的开销，却没有任何好处。

### 将其设置为 `"0"` 的作用

当在 env 中将 `CLAUDE_CODE_ATTRIBUTION_HEADER` 设置为 `0` 时，Claude Code 会停止发送这个 header。

### 为什么这对你的 PinCC 设置很重要

这**直接与你的情况相关**。Claude Code 发送的 `x-anthropic-billing-header` 包含每次请求都会变化的值（例如会话哈希 `cch=xxxx`）。在使用 relay 时，这会造成两个问题：

1. **破坏 prompt caching** — 因为 header 每次请求都变化，relay/Anthropic 后端将每个请求视为唯一，无法重用缓存，导致响应更慢且更昂贵。
2. **可能触发客户端验证检查** — relay 可能会检查这个 header 作为其“这是真正的 Claude Code 吗？”检查的一部分。畸形或意外的值可能导致 `503 only allows Claude Code clients` 错误。

### 如何在 `settings.json` 中设置

将其放置在 `env` 块内：

```json
{
  "env": {
    "CLAUDE_CODE_ATTRIBUTION_HEADER": "0"
  }
}
```

这是 Claude Code 的 `settings.json` 中持久设置环境变量的正确方式，而不是使用 shell export。

### 总结表格

| 值 | 行为 |
|---|---|
| 未设置（默认） | Claude Code 在每个请求中发送 `x-anthropic-billing-header`（每个请求变化） |
| `"0"` | Claude Code 完全抑制该 header — 不发送计费归属 |

### 对你的 PinCC 设置的推荐

将此添加到你的 `~/.claude/settings.json`：

```json
{
  "env": {
    "CLAUDE_CODE_ATTRIBUTION_HEADER": "0",
    "ANTHROPIC_BASE_URL": "https://v2-as.pincc.ai",
    "ANTHROPIC_AUTH_TOKEN": "YOUR_PINCC_TOKEN_HERE"
  }
}
```

这会抑制动态计费 header，有助于 prompt 缓存稳定，并避免向 relay 发送意外的 header 内容。它不会影响指向 PinCC 的官方 Claude Code CLI 的核心功能。

参考资料：

- [修复：使用 CLAUDE_CODE_ATTRIBUTION_HEADER 避免破坏缓存 — claude-code-router PR #1220](https://github.com/musistudio/claude-code-router/pull/1220)
- [我让 Claude Code 使用本地模型快 3 倍 — Medium/Coding Nexus](https://medium.com/coding-nexus/i-made-claude-code-3-faster-with-local-models-heres-the-one-env-variable-nobody-talks-about-7fd515eabe21)
- [Claude Code 设置参考 — claudefa.st](https://claudefa.st/blog/guide/settings-reference)
