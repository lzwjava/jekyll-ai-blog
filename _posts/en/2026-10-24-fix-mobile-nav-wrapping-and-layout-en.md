---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix mobile nav wrapping and layout
translated: false
type: note
---

Fixed. Two changes in `index.html`:

1. **`white-space: nowrap`** on `.site-nav a` — this stops "Work with me" from wrapping onto multiple lines inside the button when the nav gets squeezed.

2. **Mobile header layout** (in the `@media (max-width: 620px)` block) — the header now wraps to a second row on small phones:
   - `.header-inner` uses `flex-wrap: wrap` with `height: auto` instead of a fixed 60px height
   - `.site-nav` moves to its own full-width row (`order: 3; width: 100%`) below the wordmark and language/theme tools, right-aligned

So on mobile, the nav links (Research / Services / About / **Work with me**) sit on their own row with the CTA staying on a single line, instead of being crushed into multiple rows next to the wordmark and tools.
