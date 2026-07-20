---
audio: false
generated: true
image: false
lang: en
layout: post
title: Silent video with title and subtitle
translated: false
type: note
---

Committed and pushed at `abe19a5`. Here's what changed:

**`ww gen-video <file>` now produces:**
- 15 seconds total — 5 slides × 3 seconds each
- **No audio** — silent video
- **Image centered** in the frame (middle 60% of the vertical canvas)
- **Title** at the top (bold, white on semi-transparent black bar)
- **Subtitle** at the bottom (word-wrapped, same style)
- 1080×1920 vertical, optimized for Douyin / WeChat Video Account

**Pipeline changes:**
- LLM now generates `title` + `subtitle` + `image_prompt` per scene (no narration script)
- Removed all TTS code (`say` command, audio conversion, duration calculation)
- Simplified video assembly — always fixed 3s per slide, no audio track
