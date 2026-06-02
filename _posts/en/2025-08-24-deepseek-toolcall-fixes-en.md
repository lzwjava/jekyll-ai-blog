---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix DeepSeek Tool Call Conflicts
translated: false
type: note
---

You’re hitting a **tool-call validation error**. DeepSeek (OpenAI-style) is being used in a Claude Code flow that expects Anthropic-style tool messages. Two safe fixes:

* **Route all Claude Code work to Anthropic (via the proxy)**.
* **When you *do* use DeepSeek, turn tools off** (so it only returns plain text) and suppress reasoning streams.

Here’s an updated single-file config that does both. Paste it as-is:

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

What this does:

* Claude Code paths (`default/background/think`) go to **Anthropic via `anthropic-proxy`**, so tool use works.
* DeepSeek stays available, but with `"tool_choice":"none"` and `"reasoning.exclude": true`, so it won’t emit tool calls or thinking chunks that break your IDE agent.
* You can still pick DeepSeek explicitly (e.g., for plain chat or drafting), and it’ll route through OpenRouter cleanly.

If you still see “Invalid tool parameters,” it means some layer is *still* letting DeepSeek emit a tool call. In that case, make sure your runner actually respects per-model `params`. If it doesn’t, set your DeepSeek usage only in contexts where tools are disabled, or switch `default` back to `openai/gpt-5-mini` and reserve DeepSeek for a manual “no-tools” profile.
