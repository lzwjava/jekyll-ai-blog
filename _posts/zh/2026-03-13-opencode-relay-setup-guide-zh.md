---
audio: false
generated: true
image: false
lang: zh
layout: post
title: OpenCode 与中继服务设置指南
translated: true
type: note
---

问题：OpenCode 是否可以使用 `ANTHROPIC_BASE_URL` 和 `ANTHROPIC_AUTH_TOKEN` 连接到 claude-relay-service (pincc.ai)，并且与 Claude Code 在这方面的区别是什么？

回答：

## 概述：使用中继服务时的 OpenCode 与 Claude Code

**Claude Code** 和 **OpenCode** 处理自定义 base URL 的方式截然不同。理解这一区别是让 pincc.ai 中继正常工作的关键。

---

## 核心问题：OpenCode ≠ Claude Code

Claude Code 原生支持 `ANTHROPIC_BASE_URL` 和 `ANTHROPIC_AUTH_TOKEN` 环境变量——它是 Anthropic 的官方工具，因此会读取这些环境变量并相应路由流量。

**OpenCode 不会以相同方式自动读取这些环境变量。** 当用户尝试通过环境变量设置 `ANTHROPIC_BASE_URL` 或通过 `opencode.json` 的 `anthropic` provider 的 `baseURL` 选项设置时，OpenCode 会返回错误：`Route /api/messages not found`。这是一个已知未修复的 bug。

此外，在 OpenCode 的较新版本（例如 v0.3.133+）中，仅在 `provider.anthropic.options` 内设置 `baseURL` 会导致配置验证器抛出 `Required provider.anthropic.models` 错误，这意味着您还必须显式声明模型。

---

## pincc.ai / claude-relay-service 究竟是什么

claude-relay-service (pincc.ai) 是一个自托管的 Claude API 中继服务，它将 Claude、OpenAI 和 Gemini 订阅转换为标准 API 调用，并提供多账户管理和成本分摊功能。

它主要针对 Claude Code 设计，并使用以下方式设置中继：

```bash
export ANTHROPIC_BASE_URL="http://127.0.0.1:3000/api/"
export ANTHROPIC_AUTH_TOKEN="your-key-from-dashboard"
```

这与 **Claude Code** 无缝兼容，但与 **OpenCode** 开箱即用不兼容。

---

## 如何将 OpenCode 连接到 pincc.ai 中继

由于 pincc.ai 暴露了与 Anthropic 兼容的 `/messages` 端点，您需要使用 **`opencode.json` provider 配置** 和 `@ai-sdk/anthropic` npm 包（不是 OpenAI 兼容的那个）来配置 OpenCode。以下是正确方法：

### 选项 1：使用 `@ai-sdk/anthropic` 配合 `baseURL` + 显式模型

编辑 `~/.config/opencode/opencode.json`：

```json
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "pincc": {
      "npm": "@ai-sdk/anthropic",
      "name": "Pincc Relay",
      "options": {
        "baseURL": "https://v2-as.pincc.ai/api/",
        "apiKey": "{env:ANTHROPIC_AUTH_TOKEN}"
      },
      "models": {
        "claude-sonnet-4-6": {
          "name": "Claude Sonnet 4.6",
          "limit": {
            "context": 200000,
            "output": 65536
          }
        },
        "claude-opus-4-6": {
          "name": "Claude Opus 4.6",
          "limit": {
            "context": 200000,
            "output": 32000
          }
        }
      }
    }
  }
}
```

然后设置环境变量：

```bash
export ANTHROPIC_AUTH_TOKEN="your-pincc-api-key"
```

### 选项 2：使用 `@ai-sdk/openai-compatible`（如果中继暴露 OpenAI 格式端点）

如果中继暴露 `/v1/chat/completions` 端点（OpenAI 兼容格式），您可以使用 `@ai-sdk/openai-compatible` npm 包，并将 `baseURL` 指向该路径。

---

## 关键注意事项与已知问题

**1. `Route /api/messages not found` 错误：**
这是因为在 Claude Code 中有效的相同配置在 OpenCode 中失败——Claude Code 原生读取 `ANTHROPIC_BASE_URL`，但 OpenCode 的内部路由不会以相同方式处理它。

**2. 选项未被转发（bug）：**
在使用 `@ai-sdk/openai-compatible` 作为自定义 provider 时，`opencode.json` 中的 `options`（包括 `baseURL` 和 `apiKey`）可能不会传递到实际 API 调用中——导致请求发送到错误的端点。这是 OpenCode 中的一个已确认 bug。

**3. `models` 字段是必需的：**
设置自定义 `baseURL` 时，OpenCode 要求声明 `provider.anthropic.models`——它不会自动推断可用模型。

**4. 端点路径很重要：**
pincc.ai 中继路径是 `/api/`（例如 `https://v2-as.pincc.ai/api/`）。OpenCode 的 Anthropic SDK 会将 `/messages` 附加到此路径，结果为 `https://v2-as.pincc.ai/api/messages`——请验证这是否符合中继的预期。

---

## 总结表格

| 功能 | Claude Code | OpenCode |
| --- | --- | --- |
| 读取 `ANTHROPIC_BASE_URL` 环境变量 | ✅ 原生支持 | ❌ 不可靠 |
| 读取 `ANTHROPIC_AUTH_TOKEN` 环境变量 | ✅ 原生支持 | ❌ 不可靠 |
| 通过 `opencode.json` 使用自定义中继 | N/A | ✅ 可能（需变通方法） |
| 与 pincc.ai 兼容 | ✅ 开箱即用 | ⚠️ 需要手动配置 |

---

## 推荐

如果您的目标只是使用 pincc.ai 中继访问 Claude：

- **坚持使用 Claude Code**——它原生支持 `ANTHROPIC_BASE_URL` + `ANTHROPIC_AUTH_TOKEN`。
- 如果必须使用 OpenCode，请在 `opencode.json` 中配置**命名自定义 provider**，使用显式模型和 `baseURL`，并将 API 密钥使用 `{env:ANTHROPIC_AUTH_TOKEN}`。

参考资料：

- [OpenCode Providers Docs](https://opencode.ai/docs/providers/)
- [GitHub Issue #5163 - Custom baseURL "Route /api/messages not found"](https://github.com/anomalyco/opencode/issues/5163)
- [GitHub Issue #5674 - Custom provider options not forwarded](https://github.com/anomalyco/opencode/issues/5674)
- [GitHub Issue #5428 - baseURL requires `provider.anthropic.models`](https://github.com/anomalyco/opencode/issues/5428)
- [Wei-Shaw/claude-relay-service on GitHub](https://github.com/Wei-Shaw/claude-relay-service)
- [pincc.ai Claude Code Install Guide](https://pincc.ai/en/claude-code-install)
- [OpenCode + API Relay Guide (apiyi.com)](https://help.apiyi.com/en/opencode-api-proxy-configuration-guide-en.html)
