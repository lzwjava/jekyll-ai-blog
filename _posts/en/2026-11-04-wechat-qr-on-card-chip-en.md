---
audio: false
generated: true
image: false
lang: en
layout: post
title: WeChat QR on card chip
translated: false
type: note
---

Done (`3c4bc4c`) — WeChat QR is now on the card. All four previews (中文/English × dark/light) are open.

## What changed

- QR code from `~/Downloads/qrcode.jpg` is auto **square-cropped** (the image was 747×719), resized, and placed on a **white chip** at the bottom-center of the left panel — right below the contacts.
- Contacts trimmed from 5 → 4 lines (**TruthSoft · Email · WeChat · WhatsApp**; GitHub stays in the bottom watermark) and spacing tightened to make room.
- Works on both themes and both languages, at full density (816px tall QR region on the 2× output — easily scannable).

```bash
ww card --lang zh                    # QR from default ~/Downloads/qrcode.jpg
ww card --lang en --qr /path/q.png   # any other QR image
```

Verified the QR rendered (1,559 dark module pixels in its region). If the chip position/appearance needs tweaking — e.g. add a "微信 扫码" caption, move it to the bottom-right corner, or a colored (non-white) backing — just say the word.
