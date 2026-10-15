---
audio: false
generated: true
image: false
lang: en
layout: post
title: Static path no longer 404s
translated: false
type: note
---

Frontend deployed to Google Cloud — `/static/` no longer 404s. Summary:

## What was done

1. **Copied `live-mobile-web`** from local machine to `/home/lzw/live-mobile-web` on the `live-server` VM (excluded `node_modules/`, `.git/`, stale `static/`, and `uploadqn.json` credentials) — path matches the compose bind mount `../live-mobile-web:/app`
2. **Ran the frontend build** via the compose profile: `docker compose --profile frontend up frontend` → Vite built successfully in 18s into the `frontend-dist` volume (with `VITE_BASE_URL=/static/` injected by compose, which correctly overrides `.env.production`)
3. **Verified externally:**

| URL | Status |
|---|---|
| `/static/` | **200** — SPA index.html (趣直播) |
| `/static/index.html` | 200 |
| `/static/assets/index-CgRn8J2L.js` + CSS chunks | 200 |
| `/static/logo.png` | 200 |
| `/topics` (API) | 200 — still fine |

The `web` container needed no restart — the volume mount picks up the built files directly.

## Notes

- **`VITE_SUPABASE_URL` / `VITE_SUPABASE_ANON_KEY` are empty** in `.env.production` → chat will show the "not configured" notice. Fill them in and re-run `docker compose --profile frontend up frontend` to rebuild.
- **Rebuild after frontend changes:** `cd /home/lzw/live-server && docker compose --profile frontend up frontend`
- **`npm ci` on the VM added `node_modules/` (~112M)** to the project dir — excluded from future copies? It'll speed up rebuilds, so I left it.
- Disk now at **74%** (2.5G free) — the node build + images ate ~400M more. Still worth attaching a larger disk.
- Remaining open items from before: real Supabase keys in backend `.env`, HTTPS/domain, DB password change, SRS streaming.