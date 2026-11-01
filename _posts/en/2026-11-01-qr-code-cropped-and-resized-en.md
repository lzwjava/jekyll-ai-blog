---
audio: false
generated: true
image: false
lang: en
layout: post
title: QR Code Cropped and Resized
translated: false
type: note
---

Done. The QR code was cropped and resized successfully.

**Result:** `assets/images/group/gg2-qr.jpg` (44 KB, 300×300)

- **Located** the QR code in the original 1290×2796 screenshot (at x:379–909, y:1135–1665) using OpenCV's QR detector
- **Cropped** just the center QR code region with an 8px clean margin
- **Square** — cropped region was already square (546×546 after margin)
- **Made small** — resized to 300×300 with Lanczos resampling
- **Verified** — the cropped QR still decodes correctly to the WhatsApp invite link:
  `https://chat.whatsapp.com/IHLI78x48IG8Q94eQWVFmO?...`
