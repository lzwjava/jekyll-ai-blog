---
audio: false
generated: true
image: false
lang: en
layout: post
title: Page 9 photo row fixed
translated: false
type: note
---

Fixed ✅ — page 9 now renders the photo row properly (std 78.6, 414 columns of bright photo content vs. the broken literal-text before).

**The bug:** inside a raw HTML `<div class="gallery">`, Marp skips markdown parsing, so your `![width:190px height:340px](...)` lines were printed as literal text — that's why the sizing was all wrong.

**The fix:** moved the four images to top-level markdown (Marp processes these into real `<img>` tags) and styled the row via a per-slide `gallery_slide` class:
```css
.gallery_slide p { display: inline-block; margin: 26px 16px 0 0; }
.gallery_slide img { width: 190px; height: 338px; object-fit: cover; border-radius: 10px; box-shadow: ...; }
```
CSS controls sizing now (190×338 ≈ the source screenshots' 1:1.78 phone aspect), so no more inline width/height conflicts.

All three exports and previews are regenerated:
- `output/announcement.html` / `.pdf` / `.pptx`
- `output/previews/slide-09.png` — check it to eyeball the gallery

The other 9 slides are unchanged and verified. Anything else on the deck — maybe add labels under each photo (like "Jimiao Community 极喵社区")?
