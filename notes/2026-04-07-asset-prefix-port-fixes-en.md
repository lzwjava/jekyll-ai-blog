---
audio: false
generated: true
image: false
lang: en
layout: post
title: Asset Prefix and Port Fixes
translated: false
type: note
---

Here's the full summary of changes across both repos:

### live-mobile-web (3 changes)

1. **`vite.config.js`** — Added `base: process.env.VITE_BASE_URL || '/'` so the build output uses the correct asset prefix
2. **`.env.production`** — Added `VITE_BASE_URL=/static/` so prod builds resolve assets under `/static/`
3. **`src/router/index.js`** — Fixed Vue Router 4 catch-all: `'*'` → `'/:pathMatch(.*)*'`

### live-server (2 changes)

1. **`docker-compose.yml` (frontend service)** — Added `VITE_BASE_URL=/static/` env var so it's available during the Docker build
2. **`docker-compose.yml` (app service)** — Port remap `8081:80` → `8082:80` (8081 was taken by llama-server)

Want me to commit and push both repos? 🦞