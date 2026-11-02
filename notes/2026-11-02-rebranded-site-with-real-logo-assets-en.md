---
audio: false
generated: true
image: false
lang: en
layout: post
title: Rebranded site with real logo assets
translated: false
type: note
---

Done. All assets resolve — here's what I did:

**Copied the real TruthSoft logo assets** from `/Users/lzwjava/projects/employment-files/logo/dist` into `logo/`:

- `truthsoft-tower.svg` / `truthsoft-tower-dark.svg` (vector tower mark, light + dark)
- `favicon.ico`, `apple-touch-icon.png`, `icon-192/512.png` (app/PWA icons)
- `truthsoft-lockup*.svg` (horizontal + stacked lockups, available for print/hero use later)

**Replaced the placeholder branding in the site:**

- **Favicon** — both `index.html` and `portfolio.html` swap the emoji/data-URI favicon for `logo/favicon.ico` + the crisp vector `truthsoft-tower.svg`, plus `apple-touch-icon.png` for iOS.
- **Nav brand mark** — the generic gradient circle is now the actual stone-tower mark (19×32, native 3:5 ratio) in `style.css`, and it automatically swaps to the dark-tone variant (`truthsoft-tower-dark.svg`) when the site is in dark mode.

The nav wordmark text ("求真软件" ↔ "TruthSoft") stays as live HTML/CJK text next to the tower, so the existing `i18n.js` zh/EN toggle keeps working — only the `logo/truthsoft-lockup*.svg` files bake the wordmark in as vector text, so I left them out of the nav per the logo README's own recommendation.
