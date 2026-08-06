---
audio: false
generated: true
image: false
lang: en
layout: post
title: Default OpenRouter Key Configured
translated: false
type: note
---

Done — the key is now the server default and users don't need to supply one. Verified end-to-end through the public tunnel.

## What I did

1. **Added the key as the server default** — appended `OPENROUTER_API_KEY=sk-or-v1-346a...613` to `/root/.config/fluxreel/.env` (chmod 600). The server's `load_env()` hook loads this file with `override=True` at startup, and all OpenRouter calls (`_openrouter_chat`, `OpenRouterProvider`, `/api/check-key`) already fall back to `os.getenv("OPENROUTER_API_KEY")`.

2. **Restarted the port-8000 FluxReel server** (now PID 61349, `nohup`/`setsid` detached, log at `/root/fluxreel-8000.log`). The localhost-only 8081 instance and the frp tunnel were untouched.

3. **Updated the frontend** (`server.py` → FRONTEND_HTML) so the UI says: *"No key needed — a server default key is already configured. Enter your own OpenRouter key only to override it."* The "Check" button now also works with an empty field (it validates the default key).

## Verified

| Check | Result |
|---|---|
| Key validity (direct OpenRouter call) | ✅ valid, limit 3, expires 2026-09-05 |
| `POST /api/check-key` with **no key** (via public URL) | ✅ `{"valid":true,"label":"sk-or-v1-346...613","usage":"$0.01"}` |
| Wrong user-supplied key | ✅ still rejected (`User not found.`) |
| Frontend hint served | ✅ "No key needed — a server default key is already configured." |
| `GET /health` via public URL | ✅ `{"status":"ok","jobs":0,"local_models":[]}` |

## Resulting behavior

- **Users submit without a key** → server silently uses your default key (free tier, limit 3 concurrent).
- **User enters their own key** → their key takes precedence (`req.openrouter_api_key or env`), so per-user billing still works.
- Exposed URL unchanged: **`https://rc-8666f2536fc493ec.radeon.firstdg.ai/`**

One note: the restart cleared the in-memory job store, so the earlier completed job (`eee5172d`) is no longer listed — jobs aren't persisted to disk.
