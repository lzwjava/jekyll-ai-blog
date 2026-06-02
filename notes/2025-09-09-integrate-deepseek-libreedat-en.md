---
audio: false
date: 2025-09-09
generated: true
image: false
lang: en
layout: post
model: openai/gpt-5
title: Integrate DeepSeek with LibreChat Guide
translated: false
type: note
---

Here’s the fastest way to get **DeepSeek working in LibreChat**. I’ll show two options—use the **official DeepSeek API** (recommended), or go through **OpenRouter**.

---

## Option A — Use DeepSeek’s official API (recommended)

1. **Get a DeepSeek API key**
   Create one in your DeepSeek account, then note the base URL:
   `https://api.deepseek.com` (or OpenAI-compatible `https://api.deepseek.com/v1`). ([DeepSeek API Docs][1], [deepseek.apidog.io][2])

2. **Add a DeepSeek endpoint in `librechat.yaml`**
   Put this under `endpoints:` → `custom:`:

```yaml
- name: deepseek
  apiKey: ${DEEPSEEK_API_KEY}
  baseURL: https://api.deepseek.com/v1
  models:
    default: deepseek-chat
    fetch: true
    list:
      - deepseek-chat        # V3 (general)
      - deepseek-coder       # code-centric
      - deepseek-reasoner    # R1 reasoning
  titleConvo: true
  dropParams: null
```

LibreChat ships a **DeepSeek** config guide and confirms model names (`deepseek-chat`, `deepseek-coder`, `deepseek-reasoner`) and notes about R1 streaming its “thought process.” ([LibreChat][3])

3. **Expose the API key via `.env`**
   In your LibreChat `.env` file:

```
DEEPSEEK_API_KEY=sk-...
```

LibreChat supports custom OpenAI-compatible providers via `librechat.yaml` + `.env`. ([LibreChat][4])

4. **Restart your stack**
   From your LibreChat folder:

```bash
docker compose down
docker compose up -d --build
```

(Needed so the API container reloads `librechat.yaml` and `.env`.) If your custom endpoints don’t appear, check the `api` container logs for config errors. ([GitHub][5])

---

## Option B — Use DeepSeek via OpenRouter

If you already use OpenRouter, just register the DeepSeek models in an OpenRouter endpoint block.

`librechat.yaml`:

```yaml
- name: openrouter
  apiKey: ${OPENROUTER_KEY}
  baseURL: https://openrouter.ai/api/v1
  models:
    default: deepseek/deepseek-chat
    list:
      - deepseek/deepseek-chat
      - deepseek/deepseek-coder
      - deepseek/deepseek-reasoner
```

Two important notes from LibreChat docs:
• Don’t set `OPENROUTER_API_KEY` env var name (use a different name like `OPENROUTER_KEY`) or you’ll accidentally override the OpenAI endpoint.
• OpenRouter is first-class in LibreChat’s custom endpoints list. ([LibreChat][6])

OpenRouter exposes DeepSeek models with an OpenAI-compatible surface. ([OpenRouter][7])

---

## Tips & gotchas

* **R1 / `deepseek-reasoner`**: It can stream its chain-of-thought (“thought process”). Some OpenAI parameters may not apply. If you see odd output, test with `deepseek-chat` first. ([LibreChat][3])
* **Model fetching**: Setting `fetch: true` lets LibreChat pull the latest model list when supported; otherwise the `list:` you specify is used. ([LibreChat][8])
* **Where these settings live**: `librechat.yaml` is the custom endpoints file; `.env` carries keys and proxy settings. ([LibreChat][8])

If you want, paste your current `librechat.yaml` and I’ll patch it to add DeepSeek cleanly (no tables, I promise).

[1]: https://api-docs.deepseek.com/?utm_source=chatgpt.com "DeepSeek API Docs: Your First API Call"
[2]: https://deepseek.apidog.io/your-first-api-call-835227m0?utm_source=chatgpt.com "DeepSeek API: Your First API Call"
[3]: https://www.librechat.ai/docs/configuration/librechat_yaml/ai_endpoints/deepseek?utm_source=chatgpt.com "Deepseek"
[4]: https://www.librechat.ai/docs/quick_start/custom_endpoints?utm_source=chatgpt.com "Custom Endpoints"
[5]: https://github.com/danny-avila/LibreChat/discussions/2487?utm_source=chatgpt.com "Fix the librechat.yaml file in the main repository. #2487"
[6]: https://www.librechat.ai/docs/configuration/librechat_yaml/ai_endpoints/openrouter?utm_source=chatgpt.com "Openrouter"
[7]: https://openrouter.ai/deepseek/deepseek-v3-base%3Afree/api?utm_source=chatgpt.com "DeepSeek V3 Base – Run with an API"
[8]: https://www.librechat.ai/docs/configuration/librechat_yaml?utm_source=chatgpt.com "librechat.yaml config file"
