---
audio: false
generated: true
image: false
lang: en
layout: post
title: Set default OpenRouter DeepSeek model
translated: false
type: note
---

Set as default in `~/.pi/agent/settings.json`:

```json
"defaultProvider": "openrouter",
"defaultModel": "~deepseek/deepseek-flash-latest",
"defaultThinkingLevel": "high"
```

Notes:
- The `~` is part of the actual model ID in OpenRouter's catalog (`~deepseek/deepseek-flash-latest`, "DeepSeek: DeepSeek Flash Latest"), so it's stored verbatim.
- Provider and thinking level were already `openrouter` / `high`, so only `defaultModel` changed (was `xiaomi/mimo-v2.6-flash`).
- New sessions will use it; the current session keeps its model until you `/model` or restart.