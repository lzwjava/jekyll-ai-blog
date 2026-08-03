---
audio: false
generated: true
image: false
lang: en
layout: post
title: Tiny Video Text Fixed
translated: false
type: note
---

Server is back up and healthy. The earlier restart race was the `pkill` pattern matching the freshly launched process — started cleanly this time.

**Fixed — the video text was tiny because of two bugs:**

1. **Font fallback bug** (the main culprit): The code only looked for macOS font paths (`/System/Library/Fonts/...`). On this Linux box those don't exist, so it silently fell back to PIL's tiny default bitmap font (~11px!). Added Linux font paths: **DejaVu Sans Bold** (title) and **DejaVu Sans** (subtitle), with Liberation as backup.
2. **Small sizes**: even when a font loaded, 40px on a 1920px-tall frame is small.

**Changes in `ahl/gen_video/video.py`:**

| Element | Before | After |
| --- | --- | --- |
| Title font | 72px (often ~11px fallback) | **110px** bold |
| Subtitle font | 40px (often ~11px fallback) | **64px** |
| Title bar | 12%–18% of frame | **10%–19%** (taller) |
| Subtitle bar | 82%–88% | **80%–89%** (taller) |
| Title layout | single line, no wrap | **word-wraps to 2 lines**, auto-shrinks if needed |
| Line heights | fixed 48px | **scale with font** (1.25× / 1.2×) |

**Verified by rendering test slides** (1080×1920):

- Title text now renders **172px tall** (was ~11px fallback)
- Subtitle text **138–168px tall**
- Both fit neatly inside their darkened bars

Server restarted — new videos generated via `http://localhost:8000` will use the larger text. Want me to commit and push?
