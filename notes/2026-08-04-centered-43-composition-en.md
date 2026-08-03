---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Centered 4:3 Composition"
translated: false
type: note
---

Done. ✅ Scene image is now **4:3 and centered**, with title/subtitle symmetric around it:

```
┌─────────────────────┐  y=0
│                     │  black background
│                     │
│   TITLE (110px)     │  y=382–555   title bar (20%–29%)
│                     │
│─────────────────────│  y=555
│                     │
│   SCENE IMAGE       │  y=555–1365  1080×810 (4:3)
│   4:3, full width   │  truly centered — 559px margin top, 555px bottom
│                     │
│─────────────────────│  y=1365
│   SUBTITLE (64px)   │  y=1365–1538  subtitle bar (71%–80%)
│                     │
└─────────────────────┘  y=1920
```

**Changes (3 files):**

1. **`video.py`** — the slide composer now:
   - Reserves a **4:3 image area (1080×810)**, centered vertically in the 1920 frame
   - **Cover-crops** any source image (square, 4:3, whatever the provider returns) to fill exactly 1080×810 with a center crop — no distortion, no side bars
   - Title bar sits directly above the image, subtitle directly below → balanced, centered composition

2. **`sd_cpp_provider.py`** — default generation size changed from 768×768 → **960×720 (4:3)** (still VRAM-safe for the RTX 4070)

3. **`local_provider.py`** — diffusers FLUX size changed from 1024×1024 → **1024×768 (4:3)**

**Verified** by rendering slides: image spans y=559–1364, full 1080 width, margins 559/555px (symmetrical), both square and 4:3 sources produce identical centered results.

**Committed & pushed**: `516f66a` → `origin/main`. Server running at `http://localhost:8000`.