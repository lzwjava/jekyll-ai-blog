---
audio: false
generated: true
image: false
lang: en
layout: post
title: Taller header and no-wrap links
translated: false
type: note
---

The changes are in place. Here's what I adjusted in `style.css`:

1. **Taller top bar** — `.nav__inner` height increased from `64px` → `80px`, plus a `gap: 16px` between the brand and the links group, so the brand has breathing room on the left and the lang toggle has space on the right.

2. **No more two-line wrap in English** — `.nav__links` now has `white-space: nowrap` and a slightly tighter `gap` (`22px` → `18px`), so all the English items ("Services · AI Services · AI Team · Tech Stack · Portfolio · Finance · Clients · Team · Contact") stay on a single line instead of wrapping.

Since the links no longer wrap, the taller bar gives a comfortable, more spacious header with the logo/brand clear of the left edge and the 中/EN toggle clear of the right edge. Mobile responsive hiding still works as before.
