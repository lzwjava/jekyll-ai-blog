---
audio: false
generated: true
image: false
lang: en
layout: post
title: Deployed New Fun-Live Icon Set
translated: false
type: note
---

Done. Replaced the site icon with the new fun-live icon set:

**What changed:**

1. **`public/logo.png`** — overwritten with `fun-live-icon-256.png` (the `/logo.png` favicon + share/logo references now show the new icon)
2. **`static/logo.png`** — updated to match (this is the git-tracked copy already served by nginx)
3. **`public/fun-live-icon/`** — copied the full icon set (32/48/64/128/160/256/512/1024 PNG + SVG)
4. **`public/apple-touch-icon.png`** — generated a 180×180 version (resized from the 256 PNG) for iOS home-screen icon
5. **`index.html`** — added proper favicon links: SVG icon first, PNG size-specific icons (32–256px), plus the apple-touch-icon, keeping `/logo.png` as fallback

Note: `deploy.sh` runs `vite build` (outDir `static`), so the next deploy will regenerate `static/` from `public/` automatically — the direct `static/logo.png` update just covers the currently-live file.
