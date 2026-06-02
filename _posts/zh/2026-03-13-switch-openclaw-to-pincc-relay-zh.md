---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 从 OpenClaw 切换到 PinCC Relay 指南
translated: true
type: note
---

问题：如何配置 OpenClaw 以使用像 `https://v2-as.pincc.ai/` 这样的 Claude 中继服务（一个 PinCC 中继），同时当前使用 OpenRouter？

回答：

## 背景：OpenClaw 如何处理自定义 Relay/Proxy Providers

OpenClaw 不关心实际运行推理的是谁。它只需要一个兼容的 HTTP API，看起来像 OpenAI 或 Anthropic。当您在 OpenClaw 中配置提供商时，您定义一个 `baseUrl` — 如果该 URL 指向中继/代理而不是云供应商，OpenClaw 无需知道。

PinCC 中继 (`https://v2-as.pincc.ai/`) 是一个 **Anthropic-compatible messages API**，因此使用 `api: "anthropic-messages"` 配置它。

---

## 步骤 1 — 打开您的配置文件

```bash
nano ~/.openclaw/openclaw.json
```

---

## 步骤 2 — 添加 PinCC 作为自定义提供商

添加一个自定义提供商块，使用 PinCC 中继地址和您的 PinCC token。配置使用 `api: "anthropic-messages"`，因为 PinCC 使用 Anthropic 协议：

```json
{
  "models": {
    "mode": "merge",
    "providers": {
      "pincc-claude": {
        "baseUrl": "https://v2-as.pincc.ai",
        "apiKey": "YOUR_PINCC_TOKEN_HERE",
        "api": "anthropic-messages",
        "authHeader": true,
        "models": [
          {
            "id": "claude-sonnet-4-6",
            "name": "Claude Sonnet 4.6",
            "api": "anthropic-messages",
            "reasoning": false,
            "input": ["text"],
            "contextWindow": 200000,
            "maxTokens": 8192,
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 }
          },
          {
            "id": "claude-opus-4-6",
            "name": "Claude Opus 4.6",
            "api": "anthropic-messages",
            "reasoning": false,
            "input": ["text"],
            "contextWindow": 200000,
            "maxTokens": 8192,
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 }
          },
          {
            "id": "claude-haiku-4-5",
            "name": "Claude Haiku 4.5",
            "api": "anthropic-messages",
            "reasoning": false,
            "input": ["text"],
            "contextWindow": 200000,
            "maxTokens": 8192,
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 }
          }
        ]
      }
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "pincc-claude/claude-sonnet-4-6"
      }
    }
  }
}
```

> **注意：** 模型引用格式是 `provider-name/model-id`。OpenClaw 在第一个 `/` 上拆分 — 所以 `pincc-claude/claude-sonnet-4-6` 表示提供商 `pincc-claude`，模型 `claude-sonnet-4-6`。

---

## 步骤 3 — 保留 OpenRouter 作为后备（可选）

由于您已经在使用 OpenRouter，您可以将其保留为后备，这样如果 PinCC 中继失败，它会自动回退到 OpenRouter：

```json
"agents": {
  "defaults": {
    "model": {
      "primary": "pincc-claude/claude-sonnet-4-6",
      "fallback": [
        "openrouter/anthropic/claude-sonnet-4-5"
      ]
    }
  }
}
```

---

## 步骤 4 — 重启 OpenClaw Gateway

```bash
openclaw restart
```

或如果使用 systemd：

```bash
sudo systemctl restart openclaw
```

---

## 步骤 5 — 验证新提供商已加载

```bash
openclaw models list
```

您应该看到 `pincc-claude/claude-sonnet-4-6` 被列出。如果没有，首先检查 JSON 语法错误：

```bash
# 验证 JSON 语法
python3 -m json.tool ~/.openclaw/openclaw.json
```

---

## 步骤 6 — 测试中继连接

```bash
# 直接针对 PinCC 中继的快速 curl 测试
curl https://v2-as.pincc.ai/v1/messages \
  -H "x-api-key: YOUR_PINCC_TOKEN_HERE" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-sonnet-4-6",
    "max_tokens": 64,
    "messages": [{"role": "user", "content": "say hi"}]
  }'
```

如果您获得有效响应，您的中继工作正常，OpenClaw 将正确使用它。

---

## 关键配置差异总结

| 设置 | OpenRouter | PinCC 中继 |
|---|---|---|
| `api` 类型 | 内置（无需 `models.providers`） | `"anthropic-messages"` |
| `baseUrl` | 自动 | `https://v2-as.pincc.ai` |
| `apiKey` | 来自 OpenRouter 的 `sk-or-...` | 您的 PinCC token |
| 模型引用格式 | `openrouter/anthropic/claude-sonnet-4-5` | `pincc-claude/claude-sonnet-4-6` |
| `authHeader` | 不需要 | `true` |

参考资料：

- [PinCC OpenClaw Custom Provider Official Guide](https://pincc.ai/openclaw-custom-provider)
- [OpenClaw API Proxy Setup - LumaDock](https://lumadock.com/tutorials/openclaw-api-proxy-setup)
- [Add Custom LLM Providers to OpenClaw - LaoZhang AI Blog](https://blog.laozhang.ai/en/posts/openclaw-custom-model)
- [OpenRouter Integration - OpenClaw Docs](https://docs.openclaw.ai/providers/openrouter)
- [OpenClaw Config Provider Concepts](https://open-claw.bot/docs/concepts/model-providers/)
