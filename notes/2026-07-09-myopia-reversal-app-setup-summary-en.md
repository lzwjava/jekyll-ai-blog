---
audio: false
generated: true
image: false
lang: en
layout: post
title: Myopia Reversal App Setup Summary
translated: false
type: note
---

Done. Here's what I found and what I set up:

**openclaw** — A Node.js Telegram/WhatsApp bot agent framework (`v2026.5.12`), installed globally at `/home/lzw/.npm-global/lib/node_modules/openclaw/`. Config lives at `~/.openclaw/openclaw.json`. It's having persistent Telegram API connectivity issues (DNS timeouts to `api.telegram.org` — looks like a proxy/network blocking situation). Not related to Hermes.

**myopia-reversal-app** — Found at `/home/lzw/.openclaw/workspace/myopia-reversal-app/`. A single-page web app (vanilla HTML/CSS/JS) that calculates reduced near-vision prescriptions (typically -1.50D from full correction) for active myopia reversal. Features: unit toggle (degrees vs diopters), EN/CN bilingual, dark mode, recovery tips. Uses Vite devDependency but just `index.html` + inline JS at Mar 14 commit.

**nginx** — Configured and reloaded:

- `http://localhost/myopia/` → serves the app
- Existing `/movies/` and `/todo/` routes unchanged
- `nginx -t` passed, reloaded, returns 200
