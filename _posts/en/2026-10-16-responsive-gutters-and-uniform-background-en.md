---
audio: false
generated: true
image: false
lang: en
layout: post
title: Responsive Gutters and Uniform Background
translated: false
type: note
---

Done. To answer your design question first: **use max-width on the main container, not fixed `margin-left/right: 300px`**. Fixed margins break on smaller windows (they can exceed the viewport and cause horizontal scrolling), while `max-width` + `margin: 0 auto` is fluid and self-adjusting. The app already capped `#wrapper` at 480px — what was actually "not ok" was that cards/images ran edge-to-edge inside the column (no gutters) and the page showed two different grays around the column on desktop.

**Changes:**

`src/App.vue`
- `.view` (the root of every routed view) now gets responsive side gutters: `padding 0 12px` on phones, `0 28px` above 481px. This applies to the whole app in one place — intro page, lists, profile, forms — so nothing touches the screen edges and you never need per-view margins.
- `.live-view` opts out (`padding 0`) since the live room is a full-screen video+chat layout.
- Removed the heavy desktop box-shadow, since the background is now uniform.

`src/stylus/base.styl`
- `body` background changed from `#D2D2D2` to `#e7e7e7` (same as `#wrapper`), so on desktop the centered column blends into the page instead of showing a two-tone gray frame.

Nice side effect of the CSS box model: absolutely-positioned full-bleed elements (live video player, profile header band, fixed bottom bars) resolve against the padding box, so they still span the full column automatically — no extra code needed.

Verified with headless Chromium screenshots at 390px, 768px, and 1280px widths: the intro page cards are inset with clean gutters, the column stays centered at 480px max on desktop, and the live player remains edge-to-edge. Production build passes.