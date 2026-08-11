---
audio: false
generated: true
image: false
lang: en
layout: post
title: Move Zed project panel left
translated: false
type: note
---

Done. Created `~/.config/zed/settings.json`:

```json
{
  "project_panel": {
    "dock": "left"
  }
}
```

Notes:
- This is the setting Zed uses to position the file explorer ("project panel"): `project_panel.dock` accepts `"left"` or `"right"` (verified against your Zed 1.14.2 binary's embedded settings schema).
- Zed hot-reloads `settings.json`, so an open window should re-dock the panel immediately. If a workspace was previously saved with the panel dragged to the right, restart Zed (or drag it back once) and it'll stay left from then on.
- Bonus: `~/.config/zed/` is exactly what `ww sync zed` syncs, so this change propagates to your other machines with `uv run ww sync zed`.