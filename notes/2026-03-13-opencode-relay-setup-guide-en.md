---
audio: false
generated: true
image: false
lang: en
layout: post
title: OpenCode and Relay Service Setup Guide
translated: false
type: note
---

Question: Can OpenCode connect to the claude-relay-service (pincc.ai) using `ANTHROPIC_BASE_URL` and `ANTHROPIC_AUTH_TOKEN`, and how does it differ from Claude Code in this regard?

Answer:

## Overview: OpenCode vs Claude Code with a Relay Service

**Claude Code** and **OpenCode** handle custom base URLs very differently. Understanding this distinction is key to making the pincc.ai relay work.

---

## The Core Problem: OpenCode ≠ Claude Code

Claude Code respects `ANTHROPIC_BASE_URL` and `ANTHROPIC_AUTH_TOKEN` environment variables natively — it is Anthropic's own tool, so it reads those env vars and routes traffic accordingly.

**OpenCode does NOT automatically read those env vars the same way.** When users try to set `ANTHROPIC_BASE_URL` via environment variable or via `opencode.json`'s `baseURL` option for the `anthropic` provider, OpenCode returns the error: `Route /api/messages not found`. This is a known open bug.

Additionally, in newer versions of OpenCode (e.g. v0.3.133+), simply setting `baseURL` inside `provider.anthropic.options` causes the config validator to throw `Required provider.anthropic.models`, meaning you also must explicitly declare models.

---

## What pincc.ai / claude-relay-service Actually Is

The claude-relay-service (pincc.ai) is a self-hosted Claude API relay that converts Claude, OpenAI, and Gemini subscriptions into standard API calls, with multi-account management and cost-splitting features.

It is designed primarily for Claude Code, and sets the relay up using:

```bash
export ANTHROPIC_BASE_URL="http://127.0.0.1:3000/api/"
export ANTHROPIC_AUTH_TOKEN="your-key-from-dashboard"
```

This works seamlessly with **Claude Code**, but not out-of-the-box with **OpenCode**.

---

## How to Connect OpenCode to pincc.ai Relay

Since pincc.ai exposes an Anthropic-compatible `/messages` endpoint, you need to configure OpenCode using the **`opencode.json` provider config** with the `@ai-sdk/anthropic` npm package (not the OpenAI-compatible one). Here is the correct approach:

### Option 1: Use `@ai-sdk/anthropic` with `baseURL` + explicit models

Edit `~/.config/opencode/opencode.json`:

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

Then set your env var:

```bash
export ANTHROPIC_AUTH_TOKEN="your-pincc-api-key"
```

### Option 2: Use `@ai-sdk/openai-compatible` (if the relay exposes OpenAI-format endpoint)

If the relay exposes a `/v1/chat/completions` endpoint (OpenAI-compatible format), you can use the `@ai-sdk/openai-compatible` npm package with `baseURL` pointing to that path.

---

## Key Caveats & Known Issues

**1. The `Route /api/messages not found` error:**
This happens because the same configuration that works in Claude Code fails in OpenCode — Claude Code reads `ANTHROPIC_BASE_URL` natively, but OpenCode's internal routing does not honor it the same way.

**2. Options not being forwarded (bug):**
When using `@ai-sdk/openai-compatible` as a custom provider, the `options` (including `baseURL` and `apiKey`) from `opencode.json` may not be passed to actual API calls — resulting in requests going to the wrong endpoint. This is a confirmed bug in OpenCode.

**3. `models` field is required:**
When setting a custom `baseURL`, OpenCode requires `provider.anthropic.models` to be declared — it will not infer available models automatically.

**4. Endpoint path matters:**
The pincc.ai relay path is `/api/` (e.g. `https://v2-as.pincc.ai/api/`). OpenCode's Anthropic SDK will append `/messages` to this, resulting in `https://v2-as.pincc.ai/api/messages` — verify this matches what the relay expects.

---

## Summary Table

| Feature | Claude Code | OpenCode |
|---|---|---|
| Reads `ANTHROPIC_BASE_URL` env | ✅ Native support | ❌ Not reliable |
| Reads `ANTHROPIC_AUTH_TOKEN` env | ✅ Native support | ❌ Not reliable |
| Custom relay via `opencode.json` | N/A | ✅ Possible (with workarounds) |
| Compatible with pincc.ai | ✅ Out of the box | ⚠️ Requires manual config |

---

## Recommendation

If your goal is just to use the pincc.ai relay for Claude access:

- **Stick with Claude Code** — it works natively with `ANTHROPIC_BASE_URL` + `ANTHROPIC_AUTH_TOKEN`.
- If you must use OpenCode, configure a **named custom provider** in `opencode.json` with explicit models and `baseURL`, using `{env:ANTHROPIC_AUTH_TOKEN}` for the API key.

References:

- [OpenCode Providers Docs](https://opencode.ai/docs/providers/)
- [GitHub Issue #5163 - Custom baseURL "Route /api/messages not found"](https://github.com/anomalyco/opencode/issues/5163)
- [GitHub Issue #5674 - Custom provider options not forwarded](https://github.com/anomalyco/opencode/issues/5674)
- [GitHub Issue #5428 - baseURL requires `provider.anthropic.models`](https://github.com/anomalyco/opencode/issues/5428)
- [Wei-Shaw/claude-relay-service on GitHub](https://github.com/Wei-Shaw/claude-relay-service)
- [pincc.ai Claude Code Install Guide](https://pincc.ai/en/claude-code-install)
- [OpenCode + API Relay Guide (apiyi.com)](https://help.apiyi.com/en/opencode-api-proxy-configuration-guide-en.html)
