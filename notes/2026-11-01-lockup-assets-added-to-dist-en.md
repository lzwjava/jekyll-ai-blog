---
audio: false
generated: true
image: false
lang: en
layout: post
title: Lockup assets added to dist
translated: false
type: note
---

Done — added a full lockup (tower + "TruthSoft 求真软件" wordmark) to `dist/`, keeping the tower-only set untouched.

**New lockup assets in `dist/`:**
- `truthsoft-lockup.svg` — horizontal (tower left, wordmark right), vector, 206×90
- `truthsoft-lockup.png` / `truthsoft-lockup-3x.png` — 1× and retina PNG
- `truthsoft-lockup-dark.svg/.png/-3x` — dark-tone variant for dark backgrounds
- `truthsoft-lockup-stacked.svg/.png` + `-dark` — stacked layout (tower above text, 170×158)

**Details:**
- Wordmark matches the mockup exactly: *TruthSoft* in Playfair Display Bold 30px (#2C1A0E / #FAF0E0 on dark), 求真软件 in Inter Light 12px with 0.26em letter-spacing (#8B6B50 / #9C7A5A)
- The wordmark is baked into the SVG as vector text, so no webfont loading is needed to use it — but the tooling is project-local (`fonts/` + `fonts.conf` + the source SVGs) so you can re-render/edit text anytime
- CJK 求真软件 renders via PingFang/Hiragino fallback (same as the browser does)
- `preview.html` and `README.txt` updated — the README shows `<img src="/dist/truthsoft-lockup.svg" width="206" height="90">` for the header brand

Tip: for the live site, the scan-to-crispest approach is the SVG for desktop and the 3× PNG only if you need a raster fallback. Open `dist/preview.html` in a browser to see all variants at once — the lockup section now sits right next to the tower-only icons.
