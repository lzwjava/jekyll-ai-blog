---
audio: false
generated: true
image: false
lang: en
layout: post
title: Nav Overflow Fix for Container
translated: false
type: note
---

Done. The nav was overflowing the 1080px container in English (11 links + 2 buttons), which forced "Truth Software" to wrap. Changes in `style.css` (shared by both `index.html` and `portfolio.html`):

1. **`.nav__brand`** — added `white-space: nowrap` so the brand can never wrap to two lines, and reduced font from 17px → 16px.
2. **`.nav__links`** — reduced gap from 18px → 10px.
3. **`.nav__links a`** — reduced font from 14.5px → 13.5px.
4. **New `@media (max-width: 1000px)`** — further compresses spacing (gap 8px, font 13px, tighter CTA padding) for screens between 800–1000px where all links are still visible. Below 800px the existing rule already hides non-CTA links.

The brand now stays on one line at all widths, and the full link set fits down to ~800px.
