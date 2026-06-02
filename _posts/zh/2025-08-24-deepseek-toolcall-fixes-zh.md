---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复DeepSeek工具调用冲突
translated: true
type: note
---

你遇到了**工具调用验证错误**。当前在需要 Anthropic 格式工具消息的 Claude Code 流程中使用了 DeepSeek（OpenAI 格式）。有两种安全的解决方案：

* **将所有 Claude Code 工作路由至 Anthropic（通过代理）**
* **当使用 DeepSeek 时，关闭工具功能**（使其仅返回纯文本）并屏蔽推理流

以下是实现这两个功能的更新版单文件配置，请直接复制使用：

```json
{
  "PROXY_URL": "http://127.0.0.1:7890",
  "LOG": true,
  "Providers": [
    {
      "name": "openrouter",
      "api_base_url": "https://openrouter.ai/api/v1/chat/completions",
      "api_key": "",
      "models": [
        "moonshotai/kimi-k2",
        "anthropic/claude-sonnet-4",
        "anthropic/claude-3.5-sonnet",
        "anthropic/claude-3.7-sonnet:thinking",
        "anthropic/claude-opus-4",
        "google/gemini-2.5-flash",
        "google/gemini-2.5-pro",
        "deepseek/deepseek-chat-v3-0324",
        "deepseek/deepseek-chat-v3.1",
        "deepseek/deepseek-r1",
        "mistralai/mistral-medium-3.1",
        "qwen/qwen3-coder",
        "openai/gpt-oss-120b",
        "openai/gpt-5",
        "openai/gpt-5-mini",
        "x-ai/grok-3-mini"
      ],
      "transformer": {
        "use": ["openrouter"]
      },
      "params": {
        "deepseek/deepseek-chat-v3.1": {
          "tool_choice": "none",
          "reasoning": { "exclude": true }
        },
        "deepseek/deepseek-r1": {
          "tool_choice": "none",
          "reasoning": { "exclude": true }
        }
      }
    },
    {
      "name": "anthropic-proxy",
      "api_base_url": "http://127.0.0.1:3000/v1/messages",
      "api_key": "",
      "models": [
        "anthropic/claude-sonnet-4",
        "anthropic/claude-3.5-sonnet",
        "anthropic/claude-3.7-sonnet:thinking",
        "anthropic/claude-opus-4"
      ]
    }
  ],
  "Router": {
    "default": "anthropic-proxy,anthropic/claude-sonnet-4",
    "background": "anthropic-proxy,anthropic/claude-sonnet-4",
    "think": "anthropic-proxy,anthropic/claude-sonnet-4",
    "longContext": "openrouter,moonshotai/kimi-k2",
    "longContextThreshold": 2000,
    "webSearch": "openrouter,mistralai/mistral-medium-3.1",
    "overrides": {
      "deepseek/deepseek-chat-v3.1": "openrouter,deepseek/deepseek-chat-v3.1",
      "deepseek/deepseek-r1": "openrouter,deepseek/deepseek-r1",
      "google/gemini-2.5-flash": "openrouter,google/gemini-2.5-flash",
      "google/gemini-2.5-pro": "openrouter,google/gemini-2.5-pro",
      "qwen/qwen3-coder": "openrouter,qwen/qwen3-coder",
      "openai/gpt-5-mini": "openrouter,openai/gpt-5-mini"
    }
  }
}
```

这个配置实现了：

* Claude Code 路径（`default/background/think`）通过 **`anthropic-proxy` 路由至 Anthropic**，确保工具调用正常工作
* DeepSeek 仍可用，但设置了 `"tool_choice":"none"` 和 `"reasoning.exclude": true`，避免产生破坏 IDE 代理的工具调用或推理片段
* 你仍可显式选择 DeepSeek（例如用于纯聊天或草稿撰写），它会通过 OpenRouter 正常路由

如果仍然出现“无效工具参数”错误，说明某些层级仍在允许 DeepSeek 发出工具调用。这种情况下，请确保你的运行器确实遵循每个模型的 `params` 设置。如果问题依旧，请仅在禁用工具的上下文中使用 DeepSeek，或将 `default` 改回 `openai/gpt-5-mini` 并将 DeepSeek 保留用于手动“无工具”场景。
