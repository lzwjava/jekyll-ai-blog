---
audio: false
generated: true
image: false
lang: en
layout: post
title: Model Configuration Updated
translated: false
type: note
---

Done. Updated `/home/lzw/.pi/agent/settings.json`:

```json
{
  "defaultProvider": "openrouter",
  "defaultModel": "deepseek/deepseek-v4.1-flash",
  "defaultThinkingLevel": "high"
}
```

Notes:

- `deepseek/deepseek-v4.1-flash` exists in the catalog (OpenRouter provider, reasoning-capable, 1M context).
- Provider stays `openrouter`, which already has a stored API key in `auth.json`.
- Your thinking level is `high`, which this model supports (`thinkingLevelMap` has `high: "high"`), so no conflict.
- New sessions will now start with this model. Existing sessions keep the model they recorded.
