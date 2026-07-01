---
audio: false
generated: true
image: false
lang: zh
layout: post
title: PinCC 屏蔽非 Claude 代码客户端修复
translated: true
type: note
---

问题：在将 OpenClaw 配置为使用 PinCC relay (`https://v2-as.pincc.ai/`) 后，为什么它返回 `HTTP 503 api_error: No available accounts: this group only allows Claude Code clients`？如何修复？

回答：

## 根本原因：这是 PinCC 服务端限制，不是 OpenClaw 配置错误

此错误**并非**来自 OpenClaw 配置错误。它来自 **PinCC relay 服务器本身**，该服务器会主动检查传入请求是否看起来像是来自官方 Claude Code CLI。

2026 年 1 月，Anthropic 部署了严格的新技术防护措施，阻止订阅 OAuth token 在官方 Claude Code CLI 之外使用。错误消息 `"This credential is only authorized for use with Claude Code"`（或变体如 `"this group only allows Claude Code clients"`）是 Anthropic 和 relay 操作者设置的关卡，用于强制执行此限制。

像 OpenCode 和第三方 harness 这样的工具之前通过将自身呈现为合法的 Claude Code 客户端来工作——模仿与 Anthropic 自身 CLI 相关的 headers 或 client identifiers。Anthropic 的新检查切断了这种连接。

在 PinCC relay 的情况下：relay 本身基于 **Claude Code Max 订阅账户**（carpool/共享席位）。PinCC 的 carpool 服务通过在多个用户之间共享 Claude Code Max 订阅成本来工作。因为这些账户使用订阅 OAuth token（而非付费 API），relay 强制要求请求**看起来像是来自 Claude Code**，并拒绝任何未通过其 client 检查的内容。

---

## 此错误实际含义

| Term | Meaning |
| --- | --- |
| `No available accounts` | 没有 relay 后端账户接受此请求 |
| `this group only allows Claude Code clients` | 您使用的 PinCC group 特别要求 `User-Agent`（或等效 headers）标识为官方 Claude Code CLI |

---

## 修复选项

### 选项 A — 在 OpenClaw 中添加 Claude Code 客户端 Headers（可能有效）

relay 检查 headers 以决定请求是否来自 Claude Code。您需要 OpenClaw 发送与官方 `claude-code` CLI 匹配的正确 `User-Agent`。在您的 OpenClaw provider 配置中查找 `headers` 或 `extraHeaders` 字段：

```json
"pincc-claude": {
  "baseUrl": "https://v2-as.pincc.ai",
  "apiKey": "YOUR_PINCC_TOKEN_HERE",
  "api": "anthropic-messages",
  "authHeader": true,
  "extraHeaders": {
    "User-Agent": "claude-code/1.0",
    "anthropic-version": "2023-06-01"
  },
  ...
}
```

> **注意：** PinCC 要求的精确 `User-Agent` 字符串可能不同。请检查 PinCC 的文档或其 Telegram/Discord 支持群组以获取当前接受的值。

---

### 选项 B — 使用官方 Claude Code CLI 作为代理（推荐）

由于 PinCC relay 专为 Claude Code 设计，正确的工作流程是：

1. 安装官方 Claude Code CLI
2. 通过环境变量将其指向 PinCC relay：

```bash
export ANTHROPIC_BASE_URL="https://v2-as.pincc.ai"
export ANTHROPIC_AUTH_TOKEN="YOUR_PINCC_TOKEN_HERE"
```

3. 然后正常运行 Claude Code —— 它将透明地使用 relay。

这完全绕过了 client-check，因为您使用的是实际的官方客户端。

---

### 选项 C — 切换到基于 API Key 的 Relay（最佳长期修复）

通过阻止第三方 harness，Anthropic 正在将高容量自动化强制导向两条官方路径：Commercial API（按 token 计量计费）和官方 Claude Code 环境。

PinCC relay 的“仅限 Claude Code 客户端”group 基于 **订阅 OAuth** 账户，这本质上带有此限制。如果您想自由使用 OpenClaw，应该使用由 **Anthropic API keys**（而非订阅账户）支持的 relay group 或 provider：

- **OpenRouter** — 已与 OpenClaw 兼容，使用真实 API keys，无 client-check 问题
- **不同的 PinCC group** — PinCC 可能提供基于 API key 的 group；联系其支持询问
- **直接 Anthropic API** — 使用付费 API key 直接配置 OpenClaw 与 `api.anthropic.com`

---

## 总结

| 修复方法 | 努力程度 | 可靠性 |
| --- | --- | --- |
| 在 OpenClaw 中添加正确的 `User-Agent` headers | 低 | 不确定 — 如果 PinCC 更新检查，可能再次失效 |
| 使用官方 Claude Code CLI 与 PinCC relay | 中等 | 高 — 这是 PinCC 的设计用途 |
| 切换到 OpenRouter 或基于 API key 的 provider | 低 | 高 — 完全无 client-check 限制 |

**底线：** PinCC relay 上标记为“仅限 Claude Code 客户端”的 group 不适合与像 OpenClaw 这样的第三方客户端使用。要么配置 OpenClaw 发送正确的 Claude Code headers，要么使用官方 CLI，要么切换到像 OpenRouter 这样无此限制的基于 API key 的 provider。

参考资料：

- [Anthropic's Walled Garden: The Claude Code Crackdown (paddo.dev)](https://paddo.dev/blog/anthropic-walled-garden-crackdown/)
- [Anthropic cracks down on unauthorized Claude usage (VentureBeat)](https://venturebeat.com/technology/anthropic-cracks-down-on-unauthorized-claude-usage-by-third-party-harnesses)
- [Anthropic Tightens Control Over Claude Code Access (techbuddies.io)](https://www.techbuddies.io/2026/01/12/anthropic-tightens-control-over-claude-code-access-disrupting-third-party-harnesses-and-rival-labs/)
- [PinCC Carpool Service](https://pincc.ai/en/join-carpool)
- [PinCC Claude Code Installation Guide](https://pincc.ai/en/claude-code-install)
