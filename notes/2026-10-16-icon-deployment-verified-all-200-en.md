---
audio: false
generated: true
image: false
lang: en
layout: post
title: Icon Deployment Verified, All 200
translated: false
type: note
---

All 8 icon references serve **200**. Deployed and verified. Here's a summary:

## What happened

The deployment target for this project is the **GCP VM `live-server`** (34.150.108.243), not the AWS box the old deploy script pointed to. On the VM, the mobile SPA runs from a docker stack:

- `/home/lzw/live-mobile-web` — source copy of this repo
- `docker compose --profile frontend run --rm frontend` — builds vite output (`VITE_BASE_URL=/static/`) into the `live-server_frontend-dist` volume, mounted into the `nginx` container (`/var/www/html/public/static`), serving `funlive.io`

## Changes made

| File | Change |
|---|---|
| `index.html` | Added 8 favicon links (SVG, 32/48/64/128/256 PNG, apple-touch-icon) using the repo's root-path pattern (like the existing `/logo.png`) |
| `public/logo.png` | Replaced with new icon (256px) — also synced to `static/logo.png` locally |
| `public/fun-live-icon/` | Full icon set (32–1024 PNG + SVG) |
| `public/apple-touch-icon.png` | 180×180 for iOS |
| VM `nginx.conf` | Added root aliases `location = /apple-touch-icon.png` and `location ^~ /fun-live-icon/` in both mobile server blocks (backup saved as `nginx.conf.bak.funlive-icon`), then `nginx -t` ✓ + reload |

## Verified live (all 200)

- `https://funlive.io/` — new HTML served
- `/logo.png`, `/apple-touch-icon.png` (root fetches, incl. iOS auto-request)
- `/fun-live-icon/fun-live-icon.svg` + all size refs
- Every icon `href` inside the served `index.html`

One note: during verification I found vite rewrites root icon refs to `/static/...` in the built HTML (served by the existing `/static/` location). The nginx root aliases I added are still worth keeping — iOS Safari fetches `/apple-touch-icon.png` directly from the root, bypassing HTML links.
