---
audio: false
generated: true
image: false
lang: en
layout: post
title: Name and QR Code Square
translated: false
type: note
---

Done. The crop now includes the group name plus the QR code.

**Result:** `assets/images/group/gg2-qr.jpg` — 300×300 square (regenerated/overwritten)

What the crop contains (from the original 1290×2796 screenshot):

- **Name "AI * Truth"** — detected as the text block at y=770–870, centered at x=645
- The two smaller subtitle lines below it (y≈911–1021)
- **Center QR code** (y=1135–1665), verified still decoding to the WhatsApp invite link

How it was done:

- Cropped a centered **square** region from y=764 to y=1677 (name top down to QR bottom), width = height = 913px, horizontally centered on x=645
- Resized to **300×300** with Lanczos downsampling

Note: since the source screenshot has whitespace between the name and the QR, the crop keeps that natural gap (name near top, QR near bottom, white margins on the sides to keep it square). If you'd prefer a tighter rectangle that trims some of the side/vertical whitespace instead of a square, just say the word.
