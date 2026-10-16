---
audio: false
generated: true
image: false
lang: en
layout: post
title: Bilingual Toggle and Brand Rename
translated: false
type: note
---

Everything works. Final summary:

## Changes

**Brand rename: Zhiwei Software → 智维软件**

- `index.html` — `<title>`, meta description, nav brand, hero subtitle, footer
- `style.css` — header comment
- `README.md` — title (plus a note about the new bilingual support)
- The brand 智维软件 is intentionally kept as-is in both languages

**Full zh / en language toggle**

- **`index.html`** — added a language toggle button (`#langToggle`) in the nav; loads the new `i18n.js`
- **`i18n.js`** (new) — contains:
  - A 123-entry dictionary mapping every exact Chinese string on the page (nav, hero, services, all 23 case studies, filters, clients, team, process, contact, footer) to English — longest-key-first matching so short labels like `开发` never clobber full sentences
  - English `<title>` and meta description per language
  - Toggle logic: swaps all text nodes + `aria-label`s in place, updates `<html lang>`, restores the original Chinese snapshot when switching back, persists choice in `localStorage`, and defaults by browser language (zh browsers → 中文, others → English)
  - Button shows **EN** in Chinese mode / **中** in English mode
- **`style.css`** — `.lang-toggle` pill button styles (visible on mobile, where other nav links hide) and a word-space after English meta labels (`Role Design & development`)

## Verified with Playwright (real Chromium)

- ✅ All 123 Chinese text nodes covered by the dictionary — zero untranslated leftovers in English mode (only the brand name, by design)
- ✅ Toggle round-trips zh → en → zh with full restoration; language persists across reload
- ✅ `<title>`, meta description, and `aria-label`s switch too; no JS errors
- ✅ Case-study platform filters still work in English; screenshots confirm both layouts render cleanly on desktop and mobile
