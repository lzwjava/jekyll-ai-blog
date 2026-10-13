---
audio: false
generated: true
image: false
lang: en
layout: post
title: Remote Pi Fully Configured and Verified
translated: false
type: note
---

Everything's done and verified end-to-end. 🎉

## Option 1 complete — remote pi is fully configured

| Step | Result |
|---|---|
| `settings.json` copied | ✅ `openrouter` / `xiaomi/mimo-v2.6-flash`, thinking `high`, theme `dark` |
| `OPENROUTER_API_KEY` → remote `~/.bashrc` | ✅ appended once (73 chars, value never printed; traveled only inside the encrypted SSH channel) |
| Key visible in interactive shells | ✅ `bash -ic` sees it |
| **Live API smoke test** | ✅ `pi -p "Reply with exactly: PI_REMOTE_OK"` → **`PI_REMOTE_OK`** |

The smoke test ran pi in print mode on the remote with your real config, authenticated through `OPENROUTER_API_KEY` → OpenRouter → `xiaomi/mimo-v2.6-flash`, so the whole chain works.

## Final remote state

```
~/.pi/agent/
├── settings.json          ← model/theme config (copied from local)
├── bin/pi                 → launcher (auto-adds standalone Node to PATH)
└── install/releases/1.2.0 ← managed install (update with: pi update)

~/.local/bin/pi            ← on PATH via ~/.profile + ~/.bashrc
~/.local/share/pi-node/    ← Node.js v22.23.3 (standalone, no sudo)
~/.bashrc                  ← PATH lines + export OPENROUTER_API_KEY
```

**Usage:** `ssh lzw@192.168.1.137` then run `pi` — it'll start with your default model ready. You can adjust anything with `/settings` or `/model` (Ctrl+S to save a new default) inside a session.