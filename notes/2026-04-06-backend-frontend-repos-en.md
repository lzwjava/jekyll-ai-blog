---
audio: false
generated: true
image: false
lang: en
layout: post
title: Separate Repositories for Backend and Frontend
translated: false
type: note
---

Question: What do you think about keeping `live-server` (PHP/CodeIgniter 4 backend) and `live-mobile-web` (Vue 3 frontend) as separate repositories vs. combining them, given the architecture described?

Answer:

I agree with the analysis completely. Here's my structured take:

---

## ✅ Keep Them Separate — The Right Call

### Why the separation is correct

**Different runtimes, different concerns:**

- `live-server` = PHP 8 + CodeIgniter 4 — stateful, DB-connected, handles business logic
- `live-mobile-web` = Node.js/Vite + Vue 3 — stateless build tool, outputs pure static assets

Mixing these in one repo gives you the worst of both worlds: PHP devs tripping over `node_modules`, frontend devs confused by Composer files.

**Independent deployment cycles matter:**

- Fix a UI bug → rebuild Vue → push static files. Backend never touched.
- Patch a payment API → redeploy PHP. Frontend never touched.
- This is the whole point of decoupling.

**Already decoupled by design:**

- The Vite proxy (`/api → api.quzhiboapp.com`) proves the frontend doesn't care where the backend runs
- nginx in production is the only "glue" — and that belongs in `live-server`'s config, not the frontend repo

---

## 🏗️ Recommended Architecture

The cleanest production setup:

```
live-server/
├── docker-compose.yml        ← orchestrates everything
├── nginx/
│   └── default.conf          ← serves static + proxies /api to php-fpm
├── public/
│   └── (Vue build output dropped here)
└── ...PHP/CI4 app...
```

**docker-compose.yml** adds a frontend build stage:

```yaml
services:
  frontend-builder:
    image: node:20-alpine
    working_dir: /app
    volumes:
      - ../live-mobile-web:/app          # mount sibling repo
      - ./public:/app/dist               # output to live-server/public
    command: sh -c "npm ci && npm run build"

  php-fpm:
    build: .
    depends_on:
      - mysql
      - redis

  nginx:
    image: nginx:alpine
    volumes:
      - ./public:/var/www/html/public    # serves Vue static files
      - ./nginx/default.conf:/etc/nginx/conf.d/default.conf
    depends_on:
      - php-fpm
      - frontend-builder
```

This way:

- **Repos stay separate** — no code merging
- **One `docker-compose up`** builds everything and wires it together
- **nginx serves both** — static Vue assets + proxied PHP API — from one container

---

## 🚫 What to Avoid

| Temptation | Why It's Bad |
| --- | --- |
| Merge into monorepo | Dependency hell, confusing CI/CD, single point of failure |
| Serve Vue from a separate Node.js server in production | Unnecessary extra process — nginx already handles static files perfectly |
| Hardcode `api.quzhiboapp.com` in Vue prod build | Should be an env var (`VITE_API_BASE_URL`) injected at build time |

---

## 💡 One Improvement Worth Adding

Make sure your Vue build uses environment variables properly:

```env
# live-mobile-web/.env.production
VITE_API_BASE_URL=/api
```

```javascript
// vite.config.js — only needed in dev
proxy: {
  '/api': { target: 'http://localhost:8080', changeOrigin: true }
}
```

In production, `/api` is handled by nginx directly — no Vite proxy involved. This keeps the separation clean.

---

**Bottom line:** The architecture is sound. The Docker orchestration approach (build frontend → drop into `live-server/public` → nginx serves everything) is the pragmatic sweet spot — one deploy command, no repo merging, clean separation maintained.
