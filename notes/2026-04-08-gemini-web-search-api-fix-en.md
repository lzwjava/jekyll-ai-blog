---
audio: false
generated: true
image: false
lang: en
layout: post
title: Gemini Web Search API Fix
translated: false
type: note
---

## Session Summary

### Goal
Fix the `web_search` tool in OpenClaw which was failing due to a missing `GEMINI_API_KEY`.

---

### What Was Found

- OpenClaw config at `~/.openclaw/openclaw.json`
- Web search was configured with `provider: "gemini"` but **no API key** in the search section
- A Google API key was already present under `models.providers.google`

---

### What Was Done

1. **Backup created** — `~/.openclaw/openclaw.json.bak.20260408_041208`

2. **Initial edit** — Added `apiKey` to `tools.web.search`:
   ```json
   "search": { "enabled": true, "provider": "gemini", "apiKey": "***" }
   ```

3. **Config schema error detected** — On restart, openclaw rejected the config:
   > `tools.web.search provider-owned config moved to plugins.entries.<plugin>.config.webSearch`

4. **Auto-migration via `openclaw doctor --fix`** — This:
   - Moved the API key to the correct location: `plugins.entries.brave.config.webSearch.apiKey`
   - Enabled the `brave` plugin (which handles Gemini web search)
   - Archived 24 orphan session transcript files
   - Updated schema fields (`cacheRead`, `cacheWrite` cost fields, `api` field on models)
   - Restarted the systemd service automatically
   - Saved a fresh backup at `~/.openclaw/openclaw.json.bak`

5. **Gateway confirmed running** — PID 402575 via systemd

---

### Final Config State (relevant section)

```json
"plugins": {
  "entries": {
    "brave": {
      "enabled": true,
      "config": {
        "webSearch": {
          "apiKey": "***"
        }
      }
    }
  }
}
```

---

### Warnings Noted by Doctor (non-blocking)
- Telegram, Signal, and Slack `groupPolicy` is `"allowlist"` but `groupAllowFrom` is empty — group messages will be silently dropped unless IDs are added or policy changed to `"open"`