---
audio: false
generated: true
image: false
lang: en
layout: post
title: Stone Tower Logomark Asset Export
translated: false
type: note
---

Done. I extracted the Stone Tower logomark from the HTML mockup and exported a ready-to-serve asset set in `/Users/lzwjava/projects/employment-files/logo/dist/`:

**Vector (recommended — crisp at any size)**
- `truthsoft-tower.svg` — light tower, 3:5 ratio (54×90 viewBox)
- `truthsoft-tower-dark.svg` — dark-toned variant
- `truthsoft-square.svg` — tower centered on a 90×90 canvas (favicon source)

**PNG icons (square canvas, transparent padding)** — `icon-16 … icon-512.png` at 16, 32, 48, 64, 128, 192, 256, 512 px, plus `apple-touch-icon.png` (180×180, iOS home screen) and `icon-dark-512.png` (for dark-mode UI)

**Multi-size ICO** — `favicon.ico` containing 256/128/64/48/32/16 frames

**Natural 3:5 logo PNGs** — `truthsoft-logo-90x150.png`, `truthsoft-logo-180x300.png` (2× for retina), plus `-dark` variants

**Extras**
- `preview.html` — open in a browser to eyeball every size
- `README.txt` — copy-paste `<head>` snippet, PWA `site.webmanifest`, and header-brand markup

Note: the mockup's wordmark ("TruthSoft" Playfair Display + "求真软件") relies on Google Fonts, so I exported the tower mark only — render the text in your own HTML/CSS next to the SVG for a full logo. How to serve: point `/favicon.ico` at `dist/favicon.ico`, use `dist/truthsoft-tower.svg` for the header, and the PNGs for PWA/Apple icons.
