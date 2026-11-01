---
audio: false
generated: true
image: false
lang: en
layout: post
title: Equal Height QR Images
translated: false
type: note
---

Done. Both QR images now render at exactly the same height (200px) since the layout uses a fixed `height` with `width: auto` and `object-fit: contain`:

- **wechat_group.jpg** (1050×1575) → 200px tall, ~133px wide
- **whatsapp_group.jpg** (1280×1240) → 200px tall, ~206px wide

`object-fit: contain` preserves each image's aspect ratio, so the QR codes stay undistorted — only their height is locked, and both flex items stay centered side by side.
