---
audio: false
generated: true
image: false
lang: en
layout: post
title: Configuring OpenClaw for PinCC Relay
translated: false
type: note
---

Question: How do I configure OpenClaw to use a Claude relay service like <https://v2-as.pincc.ai/> (a PinCC relay), while currently using OpenRouter? The config doesn't have a "models" section, and it uses an "auth" section with profiles like "openrouter:default".

Answer:

In recent versions of OpenClaw (as of March 2026), authentication credentials are managed separately from the main configuration file through **auth profiles** (typically stored in `~/.openclaw/auth-profiles.json` or per-agent in `~/.openclaw/agents/<agent>/agent/auth-profiles.json`). The main `~/.openclaw/openclaw.json` file references these profiles but does **not** store the actual API keys/tokens directly for security reasons.

Built-in providers like OpenRouter use predefined auth profiles (e.g., `"openrouter:default"`) and do **not** require a `models.providers` block — OpenClaw automatically knows their endpoints and model catalogs via the pi-ai catalog.

For custom relays/proxies like PinCC (Anthropic-compatible), you **must** define them in the `models` section of `openclaw.json` using `models.providers`. This is the correct place to add custom providers, even if the file currently lacks a `models` key.

### Recommended Configuration Steps

**Step 1 — Add the auth profile reference for PinCC (optional but recommended)**
Since PinCC is a custom provider, you can define a named auth profile for it in `openclaw.json` under `"auth.profiles"`. This keeps credential management consistent.

Add or merge this into your existing `auth` section:

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

Then set the actual token using the CLI (this stores it securely, often in keychain or encrypted file):

```bash
openclaw auth set pincc:default --key "YOUR_PINCC_API_TOKEN_HERE"
```

If you skip this and use inline `apiKey` in the provider block (below), OpenClaw will still work, but using profiles is more secure and aligns with how OpenRouter is handled.

**Step 2 — Add the PinCC custom provider in the `models` section**
Create or extend the `models` block in `~/.openclaw/openclaw.json`. Use `mode: "merge"` to preserve built-in providers (including OpenRouter).

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

**Step 3 — Set PinCC as primary (with OpenRouter fallback)**
Update the agent defaults:

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

**Step 4 — Validate, restart, and test**

- Validate JSON: `python3 -m json.tool ~/.openclaw/openclaw.json`
- Restart: `openclaw restart` (or `sudo systemctl restart openclaw` if running as service)
- List models: `openclaw models list` — look for `pincc/...` entries
- Direct relay test (as before): use curl against `https://v2-as.pincc.ai/v1/messages` with your token and `"anthropic-version": "2023-06-01"` header.

This approach works because custom providers require explicit `models.providers` definitions, while built-ins like OpenRouter rely only on auth profiles + model references like `openrouter/...`.

If you encounter validation errors (e.g., unrecognized keys), check OpenClaw logs or run `openclaw doctor`. For the latest schema details, refer to the official configuration reference.

References:

- [OpenClaw Configuration Reference](https://docs.openclaw.ai/gateway/configuration)
- [OpenClaw Model Providers Documentation](https://docs.openclaw.ai/concepts/model-providers)
- [OpenRouter Integration with OpenClaw](https://openrouter.ai/docs/guides/coding-agents/openclaw-integration)
- [Adding Custom Models to OpenClaw](https://blog.laozhang.ai/en/posts/openclaw-custom-model)
- [OpenClaw CLI Models Reference](https://docs.openclaw.ai/cli/models)
