---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix Claude Code DeepSeek Config Routing
translated: false
type: note
---

Got you. Your config is sending **Claude Code’s Anthropic-style traffic** into **OpenRouter’s OpenAI-style endpoint** for DeepSeek V3.1. When Claude Code (the IDE agent) tries to do tools/plan/stream, the message schema doesn’t line up → errors.

Below is a clean way to wire it so **Anthropic models** still use an Anthropic-style gateway, while **DeepSeek V3.1** (OpenAI-style) stays on `/chat/completions`. I’ll show the exact edits you can paste.

---

### 1) Verify the DeepSeek V3.1 slug

OpenRouter’s chat model slug is:

```
deepseek/deepseek-chat-v3.1
```

(That’s the instruct/chat model—distinct from the “base” model.) ([OpenRouter][1])

---

### 2) Add an Anthropic-format proxy for Claude Code

Claude Code expects **Anthropic Messages** (`/messages`, `tool_use` blocks). The simplest fix is to run a tiny proxy that converts Anthropic→OpenAI (OpenRouter) and back again. There’s a ready-made one: **maxnowack/anthropic-proxy**. Start it like this (env var is your OpenRouter key):

```bash
OPENROUTER_API_KEY=YOUR_KEY npx anthropic-proxy
```

It listens locally and translates schemas for you. ([GitHub][2])

Now, add a **second provider** that points Claude Code traffic to that proxy.

#### 🔧 Replace your JSON with these focused changes

**Add this provider (keep your current `openrouter` provider as-is):**

```json
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
```

**Keep your existing OpenRouter provider (it’s correct to use `/chat/completions` for DeepSeek and other OpenAI-schema models).** OpenRouter normalizes to an OpenAI-compatible schema and supports extras like reasoning tokens, tools, etc. ([OpenRouter][3])

---

### 3) Route models to the right provider

Point Anthropic models to the **anthropic-proxy**; point DeepSeek/GPT/Gemini/Qwen to **openrouter**.

Example Router block you can drop in:

```json
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
```

> If your router doesn’t support an `overrides` map, the equivalent is: create separate “profiles” in your app (e.g., “Claude Code via anthropic-proxy” vs “General chat via openrouter”) and pick the profile per action.

---

### 4) Avoid reasoning stream collisions on DeepSeek (optional but safer)

DeepSeek V3.1 supports **“thinking” tokens**. Many wrappers choke if those appear mid-stream. On OpenRouter you can **exclude reasoning** with a request flag. If your router lets you set per-model params, attach:

```json
"params": {
  "reasoning": { "exclude": true }
}
```

(or `include_reasoning: false` depending on your router’s param naming). This prevents `<think>/reasoning` content from showing up where your Claude Code UI expects plain text. ([OpenRouter][4])

---

### 5) Make the minimal edits directly in your file

Here’s your config with only the necessary deltas:

* **Keep** your existing `Providers[0]` (openrouter) exactly as is.
* **Append** the new `anthropic-proxy` provider (shown above) to `Providers`.
* **Replace** your `Router` block with the one under step 3.

After that, when you pick **DeepSeek V3.1** in your tool, it goes through OpenRouter’s OpenAI-style path. When you pick any **Claude** model, it flows through `anthropic-proxy`, which converts the schema so Claude Code’s tool use works.

---

### Why this works

* DeepSeek V3.1 on OpenRouter is **OpenAI-style** (“chat/completions”, `tool_calls`, optional reasoning field). ([OpenRouter][1])
* Claude Code expects **Anthropic Messages** and **MCP/tool\_use**. The proxy handles that conversion for you. ([GitHub][2])

If you hit a specific error string after this (e.g., JSON pointer errors, “unknown field `tool_use`”, or SSE parse issues), paste it and I’ll tweak the per-model params (e.g., forcing `reasoning.exclude`, capping `max_tokens`, or adjusting tool schema) to match your router’s exact expectations.

[1]: https://openrouter.ai/deepseek/deepseek-chat-v3.1?utm_source=chatgpt.com "DeepSeek V3.1 - API, Providers, Stats"
[2]: https://github.com/maxnowack/anthropic-proxy?utm_source=chatgpt.com "maxnowack/anthropic-proxy"
[3]: https://openrouter.ai/docs/api-reference/overview?utm_source=chatgpt.com "OpenRouter API Reference | Complete API Documentation"
[4]: https://openrouter.ai/docs/use-cases/reasoning-tokens?utm_source=chatgpt.com "Reasoning Tokens | Enhanced AI Model ..."
