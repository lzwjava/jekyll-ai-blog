---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix avatar sizing and grid layout
translated: false
type: note
---

Build passes. Here's what was wrong and what I changed:

## Root cause

**`src/components/user-avatar.vue`** — `.avatar` had **no width/height**, while its child `img` was `width: 100%; height: 100%`. Those percentages resolve against an auto-sized parent, so they fall back to the image's **intrinsic size** — that's the giant circle filling the page.

**`src/views/UsersView.vue`** — the style block still targeted the *old* markup (`li .avatar`), and `.users-content`, `.user-list`, `.user-item`, `.username` had **zero CSS**. Every other page (Invite, Intro, LiveItem, Profile…) explicitly sizes `.avatar` with a nested selector, which is why only `/live/:id/users` exploded.

## Fixes

**`src/components/user-avatar.vue`** — safe defaults so this can never recur:

- `.avatar` gets `width: 50px; height: 50px; overflow: hidden; flex-shrink: 0` (overridable by any more-specific selector, so existing pages are unaffected)
- `img` → `display: block` + `object-fit: cover` (no distortion, fills circle)
- letter fallback `span` → flex centering (works at any avatar size, unlike fixed `line-height`)

**`src/views/UsersView.vue`** — replaced stale `li` rules with real layout:

- `.user-list`: CSS grid `repeat(auto-fill, minmax(64px, 1fr))` with gaps → responsive avatar grid
- `.user-item`: flex column, avatar centered above the name
- `.username`: 12px, centered, single-line ellipsis so long names like `伯阳阳阳阳阳阳阳阳阳阳` truncate instead of overflowing
- `.users-content`: light padding around the grid

Result: each user renders as a 50px circular avatar with the name underneath in a tidy grid, and the "点击加载更多" bar sits below.
