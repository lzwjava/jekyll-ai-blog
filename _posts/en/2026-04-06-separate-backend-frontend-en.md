---
audio: false
generated: true
image: false
lang: en
layout: post
title: Keep Backend and Frontend Separate
translated: false
type: note
---

Now I have a clear picture. Here's my take:

---

**Keep them separate.** Here's why:

**They're fundamentally different things:**

- **live-server** = PHP backend (CodeIgniter 4) — REST API, DB, WeChat integration, RTMP hooks, payments
- **live-mobile-web** = Vue 3 frontend — mobile web UI, calls the API via `/api` proxy

**Current relationship:**

- `live-mobile-web` proxies `/api` → `api.quzhiboapp.com` in dev (via Vite proxy)
- In production, nginx serves the static Vue build and proxies `/api` to the PHP backend
- They're already decoupled — the frontend doesn't need the backend code to build

**Why combining would be bad:**

- Mixing PHP and Node.js in one repo = messy dependency management, confusing builds
- They have different deployment cycles (update UI without redeploying backend)
- Different runtimes, different Docker images, different scaling needs

**What you should do instead:**

1. **One `docker-compose.yml` at a higher level** (or in `live-server`) that orchestrates both:
   - `live-server` already has nginx config that could serve the Vue static build
   - Just add a build step: build `live-mobile-web` → output to `live-server/public/` → nginx serves it all

2. **Or keep current repos, deploy separately:**
   - `live-server` → Docker: PHP-FPM + nginx + MySQL + Redis (already set up)
   - `live-mobile-web` → build static → copy to nginx's static dir (or serve from CDN)

The simplest path: **extend `live-server`'s Docker setup to build and include the frontend** — add a stage in the Dockerfile or a `frontend` service in docker-compose that builds the Vue app and shares the output via a volume. No need to merge repos.

Want me to set that up?
