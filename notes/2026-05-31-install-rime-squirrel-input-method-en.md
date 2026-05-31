---
audio: false
generated: true
image: false
lang: en
layout: post
title: Install RIME Squirrel Input Method
translated: false
type: note
---

All set. Here's what to do now:

**Step 1 — Log out and log back in** (required for macOS to register Squirrel as an input method)

**Step 2 — Add Squirrel to input methods:**
- System Settings → Keyboard → Text Input → Edit
- Click `+` → search "Squirrel" (鼠须管) → add it

**Step 3 — Deploy RIME** (loads your Sogou schema + rime-ice dictionaries):
- Click the Squirrel icon in the menu bar (or `Ctrl+`` to switch input method)
- Click "重新部署" (Deploy)
- Wait ~10-30 seconds for dictionary compilation on first run

After that, you'll have Sogou double pinyin with the rime-ice dictionary (2.2M+ words, English mixed input, emoji support, date/time shortcuts).

Key files created:
- `~/Library/Rime/default.custom.yaml` — schema config (Sogou shuangpin)
- `~/Library/Rime/double_pinyin_sogou.schema.yaml` — the schema itself
- `~/Library/Rime/cn_dicts/` — 6 Chinese dictionaries
- `~/Library/Rime/en_dicts/` — English mixed-input dictionaries

Go log out now, then come back if you hit any issues.