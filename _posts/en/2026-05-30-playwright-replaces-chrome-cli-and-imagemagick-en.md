---
audio: false
generated: true
image: false
lang: en
layout: post
title: Playwright replaces Chrome CLI and ImageMagick
translated: false
type: note
---

Done. Here's what changed:

```
Before: pandoc → Chrome CLI --screenshot → PNG → ImageMagick -trim → JPG
After:  pandoc → Playwright Chromium → direct JPG (exact content size)
```

Improvements from the Playwright rewrite:
- **No ImageMagick dependency** — Playwright outputs JPEG directly
- **Exact content fit** — `document.body.scrollHeight` sets viewport height precisely, no trim needed
- **Font loading** — `wait_for_load_state("networkidle")` ensures Google Fonts load before screenshot
- **Cleaner pipeline** — 2 steps instead of 3

Test result:
```
$ ww md md2jpg /tmp/test3.md
[1/2] markdown -> HTML
[2/2] HTML -> JPG (Playwright screenshot)
Done: /tmp/test3.jpg

$ file /tmp/test3.jpg
JPEG image data, 900x272, 20K   ← exact content size, no white space
```

Dependencies added:
- `playwright>=1.40.0` in `pyproject.toml`
- Chromium browser installed via `playwright install chromium`