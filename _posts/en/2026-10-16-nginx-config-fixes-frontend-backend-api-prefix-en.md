---
audio: false
generated: true
image: false
lang: en
layout: post
title: Nginx config fixes frontend-backend API prefix
translated: false
type: note
---

## Done — `funlive.io` now renders the Vue app

```html
HTTP/1.1 200 OK
Content-Type: text/html
<title>趣直播 - 知识直播平台</title>
<div id="app">
<script src="/static/assets/index-CgRn8J2L.js">
```

Verified through your browser path (proxy), direct IP, and locally on the VM.

## The blocker I found

The frontend and backend disagreed on the API prefix. The built bundle bakes `baseURL:"/api"`, but CI4's routes have **no** prefix:

```
/topics     → 200 {"status":"success"}     ← actual backend route
/api/topics → 404 Can't find a route for 'GET: api/topics'
```

Had I only switched `/` to the SPA, every API call would have 404'd. The original `website.conf` already solved this with `proxy_pass http://api.quzhiboapp.com/;` — the trailing slash strips `/api/`. I replicated that, but had to adapt it: CI4 4.7.5 routes from `REQUEST_URI` (`uriProtocol = 'REQUEST_URI'`, stripping `SCRIPT_NAME`), not `PATH_INFO`, so a plain `proxy_pass` strip would have left CI4 seeing `api/topics`. The config passes the stripped path as `REQUEST_URI`.

## Changes to `/home/lzw/live-server/nginx.conf`

Backed up to `nginx.conf.bak-1792096592`. Four blocks: `/static/` (SPA assets), `/api/` (strip prefix → PHP-FPM), `location = /` (SPA entry), and a catch-all `try_files` so bare legacy paths still reach CI4. Validated with `nginx -t` before a graceful `nginx -s reload` — no container restart.

| Test | Result |
|------|--------|
| `/` → SPA HTML | 200, `text/html`, 1897 bytes |
| `/api/topics` (frontend's baseURL) | 200 JSON ✅ was 404 |
| `/topics` (legacy bare path) | 200 JSON — preserved |
| JS / CSS / logo | 200, correct types |
| `/api/lives/count`, `?query` | 200 |
| **POST** `/api/login` with body | 200 — body survives rewrite |
| unknown `/api/*` | CI4 404 JSON (correct, not SPA) |

Routing is hash-based (`createWebHashHistory`), so no server-side SPA fallback is needed — the browser only ever requests `/`.

## Still open

1. **Apex DNS** — `162.255.119.114` is *still* on `funlive.io`. Delete it in Namecheap; right now ~75% of apex hits get a 302 instead of the site. `www.funlive.io` is clean.
2. **`CI_ENVIRONMENT=development`** (line 25) — still shipping Debugbar headers and stack traces publicly, with `DB_PASS` hardcoded in the same file. I left it since you may still want error detail, but it shouldn't go to production.
3. **No HTTPS** — 443 has no listener; only `http://` works.
4. Minor: `/index.php?/topics` is directly reachable. Not exploitable as-is, but you'd normally block direct front-controller access.

Note the bundle in the volume was built Oct 15 18:27. If you've edited `~/projects/live-mobile-web` since, rebuild with `docker compose --profile frontend up frontend` — or tell me and I'll run it.