---
audio: false
generated: true
image: false
lang: en
layout: post
title: PNG Bloat in Screenshot Capture
translated: false
type: note
---

Here's the finding:

`ww screenshot interact-note` does NOT use JPG. It's PNG end-to-end with zero optimization:

1. `capture_screenshot()` saves as `screenshot-{ts}.png` (line 18 of `ww/image/screenshot.py`)
2. `_encode_image_to_base64()` reads the raw file bytes and base64 encodes — no resize, no format conversion, no compression (line 20-22 of `ww/note/screenshot_log.py`)
3. MIME type is set based on extension, but since it's always `.png`, it's always `image/png`

So the full-resolution PNG gets sent raw to the vision API. On a Retina display that's likely 2x-3x the pixel density needed for LLM vision, and the base64 payload is bloated by PNG's lossless encoding of gradients/anti-aliased text.

Given your analysis, there's a clear optimization opportunity: convert to JPG quality 50-70 and optionally resize before sending to the vision model. Want me to add that?
