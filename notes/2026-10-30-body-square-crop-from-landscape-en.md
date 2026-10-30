---
audio: false
generated: true
image: false
lang: en
layout: post
title: Body Square Crop from Landscape
translated: false
type: note
---

Done. New image created:

**`image/photo_6126_body_600x600.jpg`** (600×600, quality 95, 300 DPI, 65 KB)

How it was made from `IMG_6126.JPG` (5184×3456):

- Detected the person with macOS Vision → full body box (1190,530)–(4125,3453), center **(2658,1991)**
- Square source crop centered on the **body center**, height = body height × 1.05 → crop `x=1124..4192, y=387..3456` (3068×3069)
- Resampled with Lanczos to exactly **600×600**

Note: the source is landscape, so the square crop clips to the bottom edge of the frame — the body is centered horizontally and sits centered vertically, but there's only ~3 px of margin below the feet (the top margin is ~143 px). If you'd prefer tighter framing or a different margin, I can rerun with an adjusted factor.

Script saved at `image/make_6126_body_600.py` if you want to tweak `MARGIN` or the output name.
