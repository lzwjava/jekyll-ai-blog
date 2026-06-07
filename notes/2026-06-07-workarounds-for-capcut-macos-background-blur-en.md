---
audio: false
generated: true
image: false
lang: en
layout: post
title: Workarounds for CapCut macOS Background Blur
translated: false
type: note
---

Question: CapCut macOS doesn't have a visible background blur option — what are the actual workarounds?

Answer:

You're right — CapCut macOS **doesn't expose a dedicated background blur feature** in the UI like the mobile version does. Here are the practical options:

**Option 1: FFmpeg (most reliable, terminal-first)**

```bash
ffmpeg -i input.mp4 -vf "scale=640:480:force_original_aspect_ratio=decrease,pad=640:480:(ow-iw)/2:(oh-ih)/2,boxblur=15" output.mp4
```

Replace dimensions with your target (4:3 = 640×480, 1920×1440, etc.). Adjust `boxblur=15` to taste (higher = more blur).

Then import `output.mp4` into CapCut.

**Option 2: Use a different tool (faster UI-wise)**

- **DaVinci Resolve** (free, macOS) — native blur background support
- **Adobe Premiere** — Adjustment Layers + Gaussian Blur
- **FFmpeg + imagemagick** — fully automatable

**Option 3: CapCut workaround (clunky)**

1. Add a **Background layer** (solid color or image)
2. Add a **second layer** of your image scaled up to fill canvas
3. Apply **Gaussian Blur** to the background layer
4. Put your original image on top at correct aspect ratio

This duplicates your source but works.

---

**My recommendation:** Use FFmpeg one-liner above. You're terminal-first, it's 3 seconds, produces pixel-perfect output, and CapCut just imports it. Way faster than hunting UI in CapCut.

Do you want me to write a shell script that batch-processes multiple videos this way?
