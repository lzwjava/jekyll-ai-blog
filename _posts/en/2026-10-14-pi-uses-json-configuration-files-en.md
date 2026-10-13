---
audio: false
generated: true
image: false
lang: en
layout: post
title: Pi uses JSON configuration files
translated: false
type: note
---

Checked. Key finding: **pi doesn't use a `config.yaml`** — it's all JSON files in the agent directory `~/.pi/agent/`. Here's the state:

## Remote machine (`192.168.1.137`) — no model config yet

```
~/.pi/agent/
├── install/managed-install.json   ← installer marker (only file that exists)
└── bin/pi
```

- **No `settings.json`**, **no `models.json`**, **no `auth.json`** — it's a pristine install; we only ran `pi --version`, never a full session.
- **No provider credentials**: 0 provider/API-key env vars set (`OPENAI_*`, `ANTHROPIC_*`, `OPENROUTER_API_KEY`, …).
- So currently pi would start with **automatic/bundled model catalog but no usable authentication** — `/model` would show no available models until you either `/login` or set an API key env var.

## Reference: this machine's config (what "configured" looks like)

`~/.pi/agent/settings.json`:
```json
{
  "lastChangelogVersion": "1.2.0",
  "theme": "dark",
  "defaultProvider": "openrouter",
  "defaultModel": "xiaomi/mimo-v2.6-flash",
  "hideThinkingBlock": false,
  "defaultThinkingLevel": "high"
}
```
- `models.json`: doesn't exist (no custom endpoints)
- `auth.json`: empty `[]` — this machine authenticates OpenRouter via the `OPENROUTER_API_KEY` env var, not stored credentials

## Where model config lives (docs: `configuration.md` / `settings.md`)

| File | Purpose |
|---|---|
| `~/.pi/agent/settings.json` | `defaultProvider`, `defaultModel`, `defaultThinkingLevel`, `enabledModels`, theme |
| `~/.pi/agent/models.json` | Custom/compatible endpoints (Ollama, vLLM, proxies…) |
| `~/.pi/agent/auth.json` | Credentials written by `/login` (or use env vars) |

Want me to **copy your `settings.json` over to the remote** (OpenRouter / `xiaomi/mimo-v2.6-flash` / thinking `high`)? You'd still need to provide `OPENROUTER_API_KEY` on that host — either export it in its shell profile, or run `pi` → `/login` interactively there.