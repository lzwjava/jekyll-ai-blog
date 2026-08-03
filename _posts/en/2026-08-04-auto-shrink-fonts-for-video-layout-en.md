---
audio: false
generated: true
image: false
lang: en
layout: post
title: Auto-Shrink Fonts for Video Layout
translated: false
type: note
---

All done. ✅

**Layout summary** — final video is **1080×1920 (9:16), 30fps, 5 slides × 3s = 15s**:

```
┌─────────────────────┐  y=0      black background (1080×1920)
│                     │
│   TITLE  (110px)    │  y=192–365  title bar (10%–19%)
│  "Attention..."     │  white bold, centered, max 2 lines
│─────────────────────│  y=384
│                     │
│   SCENE IMAGE       │  y≈420–1500  square images scale to
│   (1080×1080)       │  1080×1080, centered in the 1080×1152 area
│                     │
│─────────────────────│  y=1536
│  SUBTITLE (64px)    │  y=1536–1708  subtitle bar (80%–89%)
│  "How transformer…" │  white, centered, max 3 lines
└─────────────────────┘  y=1920
```

**What I fixed** (verified with rendered slides):

- Title and subtitle fonts now **auto-shrink until they fit inside their bars** (previously 2-line titles and 3-line subtitles overflowed into the image area)
- Extreme stress test passes: title y=212–336 and subtitle y=1545–1695, both fully inside their bars ✓

**Committed & pushed**: `b6331b2` — "Fit title/subtitle text within their bars: auto-shrink fonts until they fit" → `origin/main`

Server running at `http://localhost:8000` with all changes.
