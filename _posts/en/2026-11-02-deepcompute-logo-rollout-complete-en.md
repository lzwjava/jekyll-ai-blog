---
audio: false
generated: true
image: false
lang: en
layout: post
title: DeepCompute Logo Rollout Complete
translated: false
type: note
---

Done. The DeepCompute icon is now the logo throughout the site.

**What I did:**

1. **Generated logo assets** in `logo/` from `zhiwei_deepcompute_logo_icon_1024px.png`:
   - `deepcompute-icon.png` (256px) — new nav logo
   - `favicon.ico` — rebuilt with 16/24/32/48/64px sizes
   - `apple-touch-icon.png` (180px), `icon-192.png`, `icon-512.png` — refreshed from the new mark

2. **HTML** (`index.html`, `portfolio.html`): replaced the `truthsoft-tower.svg` favicon link with `logo/deepcompute-icon.png`.

3. **CSS** (`style.css`):
   - `.nav__logo` is now a square 28×28 icon using `deepcompute-icon.png` (was 19×32 tall tower SVG)
   - removed the `html[data-theme="dark"] .nav__logo` override since the same icon works in both themes

One thing to note: the icon is a light (white tile + purple mark) logo, so in dark mode it shows as a white tile, and in light mode the tile blends into the white nav leaving the purple mark visible — it reads fine in both.

The old `truthsoft-tower*.svg` and `truthsoft-lockup*.svg` files are still in `logo/` but no longer referenced anywhere. Want me to delete them, or keep them around?
