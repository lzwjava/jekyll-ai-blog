---
audio: false
generated: true
image: false
lang: en
layout: post
title: DeepSeek Flash Default Configured
translated: false
type: note
---

Done. `~/.pi/agent/settings.json` now has:

```json
"defaultProvider": "openrouter",
"defaultModel": "~deepseek/deepseek-flash-latest",
"defaultThinkingLevel": "high"
```

Notes:
- The exact model ID is `~deepseek/deepseek-flash-latest` (the leading `~` is part of the OpenRouter ID), provider `openrouter`.
- `high` thinking is supported by this model (`off`, `low`, `high`, `max` are available), so the existing `defaultThinkingLevel` was kept — that matches the `• h` badge you saw in the picker.
- Backup saved at `~/.pi/agent/settings.json.bak`. Applies to new sessions; the current session keeps its model unless you switch with `/model`.