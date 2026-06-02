---
audio: false
generated: true
image: false
lang: en
layout: post
title: Updated Multi-Model Proxy Config Guide
translated: false
type: note
---

Here you go—drop this in as your updated config:

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
    "default": "openrouter,openai/gpt-5-mini",
    "background": "openrouter,google/gemini-2.5-flash",
    "think": "openrouter,qwen/qwen3-coder",
    "longContext": "openrouter,moonshotai/kimi-k2",
    "longContextThreshold": 2000,
    "webSearch": "openrouter,mistralai/mistral-medium-3.1",
    "overrides": {
      "anthropic/claude-sonnet-4": "anthropic-proxy,anthropic/claude-sonnet-4",
      "anthropic/claude-3.5-sonnet": "anthropic-proxy,anthropic/claude-3.5-sonnet",
      "anthropic/claude-3.7-sonnet:thinking": "anthropic-proxy,anthropic/claude-3.7-sonnet:thinking",
      "anthropic/claude-opus-4": "anthropic-proxy,anthropic/claude-opus-4",
      "deepseek/deepseek-chat-v3.1": "openrouter,deepseek/deepseek-chat-v3.1"
    }
  }
}
```

If your runner exposes a flag to suppress reasoning streams on DeepSeek (sometimes called `reasoning.exclude` or similar), enable it for `deepseek/deepseek-chat-v3.1` to avoid UI parse hiccups.
