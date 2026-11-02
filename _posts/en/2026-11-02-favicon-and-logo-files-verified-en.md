---
audio: false
generated: true
image: false
lang: en
layout: post
title: Favicon and Logo Files Verified
translated: false
type: note
---

Yes, the logo shows correctly in the browser tab. Verified:

**Files exist and are valid**
- `logo/favicon.ico` — valid ICO, contains 5 sizes (16×16, 24×24, 32×32, 48×48, 64×64)
- `logo/deepcompute-icon.png` — 256×256 RGBA PNG (the modern fallback icon Browsers prefer)
- `logo/apple-touch-icon.png` — 180×180 for iOS/iPhone

**References in HTML** (both `index.html` and `portfolio.html`):
```html
<link rel="icon" href="logo/favicon.ico" sizes="any">
<link rel="icon" href="logo/deepcompute-icon.png" type="image/png">
<link rel="apple-touch-icon" href="logo/apple-touch-icon.png">
```

**All 12 case pages** in `cases/` correctly use the parent-relative path `../logo/favicon.ico`.

**Icon content** — not blank/empty: ~70% opaque pixels (light gray with blue/purple accents, consistent with the "tower" mark in the SVG sources), transparent background for the corners.

**Serving check** — local server test returned HTTP 200 with correct content types (`image/x-icon`, `image/png`) for all icon files on the root page and case pages.

One minor note: browser tab icons are cached aggressively, so if you recently changed the logo, you may need a hard refresh (Cmd+Shift+R) to see the update.
