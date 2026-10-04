---
audio: false
generated: true
image: false
lang: en
layout: post
title: Pi's Default Model Updated to MiMo
translated: false
type: note
---

Done. Pi's default model is now `xiaomi/mimo-v2.6-flash`.

**What I changed** — `~/.pi/agent/settings.json`:

```json
"defaultProvider": "openrouter",
"defaultModel": "xiaomi/mimo-v2.6-flash",
```

**Details:**
- The model is in Pi's catalog under the **openrouter** provider (`Xiaomi: MiMo-V2.6-Flash`), 1M context, reasoning-capable, vision input — previously the default was `deepseek/deepseek-v4.1-flash`.
- `OPENROUTER_API_KEY` is already set in your environment, so authentication will work (your `auth.json` is empty, but Pi falls back to the env variable).
- The change applies to **new sessions**; the current session keeps its model. Press `Ctrl+P` or run `/model` in this session if you want to switch now.

If you ever want to revert, run `/model` in Pi, pick the DeepSeek model, and press `Ctrl+S` to save it as the default.