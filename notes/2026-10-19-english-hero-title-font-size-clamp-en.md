---
audio: false
generated: true
image: false
lang: en
layout: post
title: English hero title font-size clamp
translated: false
type: note
---

Done. Added a `.hero__title:lang(en)` rule in `style.css` that only applies when the page is in English (i18n.js sets `html lang="en"`):

```css
.hero__title:lang(en) {
  font-size: clamp(14px, 2.8vw, 30px);
  line-height: 1.3;
}
```

- **Max 30px** on desktop (vs 56px for Chinese) — that's ~54%, not 70%. I went smaller than your 70% guess because at 39px (70%) the first line "More than turning your ideas into shippable products —" is still ~1240px wide and would wrap to 3 lines. At 30px it fits the 1032px container on one line, so the title is exactly 2 lines.
- **`2.8vw`** scales it down proportionally on smaller screens so it stays 2 lines down to ~640px.
- Chinese is untouched — it keeps the big `clamp(34px, 6vw, 56px)`.

If you'd rather keep it bigger and accept 3 lines, I can bump the max to ~39px.
