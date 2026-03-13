---
audio: false
generated: true
image: false
lang: en
layout: post
title: Switch OpenClaw to PinCC Relay Guide
translated: false
type: note
---

Question: How do I configure OpenClaw to use a Claude relay service like `https://v2-as.pincc.ai/` (a PinCC relay), while currently using OpenRouter?

Answer:

## Background: How OpenClaw Handles Custom Relay/Proxy Providers

OpenClaw does not care who actually runs inference. It just needs a compatible HTTP API that looks like OpenAI or Anthropic. When you configure a provider in OpenClaw, you define a `baseUrl` — if that URL points to a relay/proxy instead of a cloud vendor, OpenClaw never needs to know.

The PinCC relay (`https://v2-as.pincc.ai/`) is an **Anthropic-compatible messages API**, so you configure it with `api: "anthropic-messages"`.

---

## Step 1 — Open Your Config File

```bash
nano ~/.openclaw/openclaw.json
```

---

## Step 2 — Add PinCC as a Custom Provider

Add a custom provider block using the PinCC relay address and your PinCC token. The config uses `api: "anthropic-messages"` since PinCC speaks the Anthropic protocol:

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

> **Note:** The model reference format is `provider-name/model-id`. OpenClaw splits on the first `/` — so `pincc-claude/claude-sonnet-4-6` means provider `pincc-claude`, model `claude-sonnet-4-6`.

---

## Step 3 — Keep OpenRouter as Fallback (Optional)

Since you are already using OpenRouter, you can keep it as a fallback so if PinCC relay fails, it rolls over to OpenRouter automatically:

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

## Step 4 — Restart OpenClaw Gateway

```bash
openclaw restart
```

Or if using systemd:

```bash
sudo systemctl restart openclaw
```

---

## Step 5 — Verify the New Provider Is Loaded

```bash
openclaw models list
```

You should see `pincc-claude/claude-sonnet-4-6` listed. If not, check for JSON syntax errors first:

```bash
# Validate JSON syntax
python3 -m json.tool ~/.openclaw/openclaw.json
```

---

## Step 6 — Test the Relay Connection

```bash
# Quick curl test directly against the PinCC relay
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

If you get a valid response, your relay is working and OpenClaw will use it correctly.

---

## Summary of Key Config Differences

| Setting | OpenRouter | PinCC Relay |
|---|---|---|
| `api` type | built-in (no `models.providers` needed) | `"anthropic-messages"` |
| `baseUrl` | automatic | `https://v2-as.pincc.ai` |
| `apiKey` | `sk-or-...` from OpenRouter | Your PinCC token |
| Model ref format | `openrouter/anthropic/claude-sonnet-4-5` | `pincc-claude/claude-sonnet-4-6` |
| `authHeader` | not needed | `true` |

References:

- [PinCC OpenClaw Custom Provider Official Guide](https://pincc.ai/openclaw-custom-provider)
- [OpenClaw API Proxy Setup - LumaDock](https://lumadock.com/tutorials/openclaw-api-proxy-setup)
- [Add Custom LLM Providers to OpenClaw - LaoZhang AI Blog](https://blog.laozhang.ai/en/posts/openclaw-custom-model)
- [OpenRouter Integration - OpenClaw Docs](https://docs.openclaw.ai/providers/openrouter)
- [OpenClaw Config Provider Concepts](https://open-claw.bot/docs/concepts/model-providers/)