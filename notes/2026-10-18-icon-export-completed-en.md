---
audio: false
generated: true
image: false
lang: en
layout: post
title: Icon Export Completed
translated: false
type: note
---

Done. I extracted the hero icon SVG from `Fun Live Icon.html` (the 160×160 version with full gradients, pupil shadow, and rim light) and exported PNGs into a new folder:

**Output folder:** `/Users/lzwjava/Downloads/fun-live-icon/`

| File | Size | Use case |
| ------ | ------ | ---------- |
| `fun-live-icon-1024.png` | 1024×1024 | App Store / high-res master |
| `fun-live-icon-512.png` | 512×512 | Play Store, preview |
| `fun-live-icon-256.png` | 256×256 | Standard app/favicon |
| `fun-live-icon-160.png` | 160×160 | Original hero size |
| `fun-live-icon-128.png` | 128×128 | Favicon / small app |
| `fun-live-icon-64.png` | 64×64 | Chrome web store, tray |
| `fun-live-icon-48.png` | 48×48 | Favicon standard |
| `fun-live-icon-32.png` | 32×32 | Favicon small |
| `fun-live-icon.svg` | — | Vector source (kept for future exports) |

All PNGs are RGBA, rendered at native resolution (not upscaled) from the SVG, so they stay crisp. If you also want a version with transparent rounded corners (no background tile), a mask-only/monochrome variant, or different sizes, let me know.
