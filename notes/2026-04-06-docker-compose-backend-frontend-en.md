---
audio: false
generated: true
image: false
lang: en
layout: post
title: Docker Compose for Backend and Frontend
translated: false
type: note
---

Here's the setup:

### How it works

**Normal dev** (just backend):

```bash
cd live-server && docker compose up -d
```

→ PHP + nginx + MySQL + Redis. Frontend ignored.

**Build everything** (with frontend):

```bash
cd live-server && docker compose --profile frontend up -d
```

→ Also builds `live-mobile-web`, drops static files into a shared volume, nginx serves them at `/static/`.

**Local frontend dev** (hot reload):

```bash
cd live-mobile-web && npm run dev
```

→ Vite dev server with proxy to `api.quzhiboapp.com` (or set `VITE_API_PROXY=http://localhost:8080` to use your local backend).

### Key changes

| File | What |
|---|---|
| `live-server/docker-compose.yml` | Added `frontend` service (profile-gated), `frontend-dist` shared volume mounted in nginx |
| `live-server/nginx.conf` | Added `/static/` location with immutable cache headers |
| `live-mobile-web/.env.production` | Sets `VITE_API_BASE_URL=/api` so prod builds point to nginx |
| `live-mobile-web/vite.config.js` | Proxy target now uses `VITE_API_PROXY` env var (defaults to `api.quzhiboapp.com`) |

Repos stay separate, one compose file orchestrates both. 🦞
