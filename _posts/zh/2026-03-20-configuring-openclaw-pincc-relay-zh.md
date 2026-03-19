---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 为 PinCC Relay 配置 OpenClaw
translated: true
type: note
---

在 OpenClaw 的最近版本（截至 2026 年 3 月），认证凭据通过 **auth profiles** 与主配置文件分开管理（通常存储在 `~/.openclaw/auth-profiles.json` 或每个代理在 `~/.openclaw/agents/<agent>/agent/auth-profiles.json` 中）。主文件 `~/.openclaw/openclaw.json` 引用这些 profiles，但出于安全原因 **不** 直接存储实际的 API keys/tokens。

像 OpenRouter 这样的内置 providers 使用预定义的 auth profiles（例如 `"openrouter:default"`），并且 **不** 需要 `models.providers` 块 — OpenClaw 通过 pi-ai catalog 自动知道它们的 endpoints 和 model catalogs。

对于像 PinCC（Anthropic-compatible）这样的自定义 relays/proxies，您 **必须** 在 `openclaw.json` 的 `models` 部分使用 `models.providers` 定义它们。这是添加自定义 providers 的正确位置，即使文件当前缺少 `models` 键。

### 推荐配置步骤

**步骤 1 — 为 PinCC 添加 auth profile 引用（可选但推荐）**  
由于 PinCC 是自定义 provider，您可以在 `openclaw.json` 的 `"auth.profiles"` 下为其定义一个命名 auth profile。这保持了凭据管理的统一性。

将以下内容添加到现有的 `auth` 部分或合并：

```json
"auth": {
  "profiles": {
    "openrouter:default": {
      "provider": "openrouter",
      "mode": "api_key"
    },
    "pincc:default": {
      "provider": "pincc",
      "mode": "api_key"
    }
  }
}
```

然后使用 CLI 设置实际的 token（这会安全存储，通常在 keychain 或加密文件中）：

```bash
openclaw auth set pincc:default --key "YOUR_PINCC_API_TOKEN_HERE"
```

如果您跳过此步骤并在下面的 provider 块中使用内联 `apiKey`，OpenClaw 仍然可以工作，但使用 profiles 更安全，并且与 OpenRouter 的处理方式一致。

**步骤 2 — 在 `models` 部分添加 PinCC 自定义 provider**  
在 `~/.openclaw/openclaw.json` 中创建或扩展 `models` 块。使用 `mode: "merge"` 来保留内置 providers（包括 OpenRouter）。

```json
"models": {
  "mode": "merge",
  "providers": {
    "pincc": {
      "baseUrl": "https://v2-as.pincc.ai",
      "api": "anthropic-messages",
      "authHeader": true,
      "apiKey": "YOUR_PINCC_API_TOKEN_HERE",   // optional if using auth profile above
      // or use profile reference (preferred):
      // "authProfile": "pincc:default",
      "models": [
        {
          "id": "claude-sonnet-4-6",
          "name": "Claude Sonnet 4.6 (PinCC)",
          "contextWindow": 200000,
          "maxTokens": 8192,
          "input": ["text"],
          "reasoning": false,
          "cost": { "input": 0, "output": 0 }
        },
        {
          "id": "claude-opus-4-6",
          "name": "Claude Opus 4.6 (PinCC)",
          "contextWindow": 200000,
          "maxTokens": 8192,
          "input": ["text"],
          "reasoning": false,
          "cost": { "input": 0, "output": 0 }
        }
        // Add more models as supported by PinCC
      ]
    }
  }
}
```

**步骤 3 — 将 PinCC 设置为主（带 OpenRouter 回退）**  
更新代理默认设置：

```json
"agents": {
  "defaults": {
    "model": {
      "primary": "pincc/claude-sonnet-4-6",
      "fallback": [
        "openrouter/anthropic/claude-sonnet-4-5"   // or your preferred OpenRouter model
      ]
    }
  }
}
```

**步骤 4 — 验证、重启并测试**  
- 验证 JSON：`python3 -m json.tool ~/.openclaw/openclaw.json`  
- 重启：`openclaw restart`（或如果作为服务运行则 `sudo systemctl restart openclaw`）  
- 列出模型：`openclaw models list` — 查找 `pincc/...` 条目  
- 直接 relay 测试（如前）：使用 curl 测试 `https://v2-as.pincc.ai/v1/messages`，带您的 token 和 `"anthropic-version": "2023-06-01"` header。

这种方法有效是因为自定义 providers 需要明确的 `models.providers` 定义，而像 OpenRouter 这样的内置 providers 只依赖 auth profiles + 模型引用如 `openrouter/...`。

如果遇到验证错误（例如，无法识别的键），请检查 OpenClaw 日志或运行 `openclaw doctor`。有关最新 schema 详情，请参考官方配置参考。

References:  

- [OpenClaw Configuration Reference](https://docs.openclaw.ai/gateway/configuration)
- [OpenClaw Model Providers Documentation](https://docs.openclaw.ai/concepts/model-providers)
- [OpenRouter Integration with OpenClaw](https://openrouter.ai/docs/guides/coding-agents/openclaw-integration)
- [Adding Custom Models to OpenClaw](https://blog.laozhang.ai/en/posts/openclaw-custom-model)
- [OpenClaw CLI Models Reference](https://docs.openclaw.ai/cli/models)