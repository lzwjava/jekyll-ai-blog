---
audio: false
generated: true
image: false
lang: en
layout: post
title: Dark Mode CSS Specificity Fix
translated: false
type: note
---

Fixed and verified. Here's what was going on:

**Root cause — CSS specificity, not the input itself (your hunch about the wrapper was right):**
- Light theme: `.sort-container .deepwiki-link .deepwiki-form` → **3 classes** → `background: #fff`
- Dark theme: `.dark-mode .deepwiki-form` → only **2 classes** → `background: #2a2a2a`

The 3-class light rule outgunned the 2-class dark rule, so the white pill background (and the blue border, shadow, and even `color: #333` on the input text) always won in dark mode.

**Fix** in `_sass/dark-mode.scss`: matched the full chain plus the `.dark-mode` ancestor:
```scss
.sort-container .deepwiki-link .deepwiki-form {   // under .dark-mode →
    background: #2a2a2a;                          // .dark-mode .sort-container .deepwiki-link .deepwiki-form
    border-color: #4f82e6;                        // 4 classes > 3 classes → dark now wins
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5);
    .deepwiki-input { color: #f0f0f0; ... }
}
```

**Verified** with `bundle exec jekyll build` (exit 0) — compiled CSS now contains:
```css
.dark-mode .sort-container .deepwiki-link .deepwiki-form { background: #2a2a2a; ... }
.dark-mode .sort-container .deepwiki-link .deepwiki-form .deepwiki-input { color: #f0f0f0; ... }
```

Reload a page with the toggle on and the DeepWiki pill should be charcoal `#2a2a2a` with light text instead of white.

Heads-up: `_sass/dark-mode.scss` is now modified too, alongside the pre-existing uncommitted `_includes/sort.html` and `_sass/layout.scss` from earlier. Want me to commit these (and push, using the HTTP/1.1 HTTPS workaround since SSH through your proxy is unreliable)?
