---
audio: false
generated: true
image: false
lang: en
layout: post
title: Zed Panel Config Applies Immediately
translated: false
type: note
---

Done. Created `/home/lzwjava/.config/zed/settings.json` with:

```json
{
  "project_panel": {
    "dock": "left"
  }
}
```

Zed picks this up immediately on next focus — no restart needed. If your project panel is on the right still, just close and re-open the project or toggle the panel with `Cmd+B` / `Ctrl+B` to refresh.