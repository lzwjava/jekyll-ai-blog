---
audio: false
generated: true
image: false
lang: en
layout: post
title: Dark/Light Mode Toggle on Every Page
translated: false
type: note
---

Done ✅ — committed as `8cc20d2` and pushed to `main`.

**Dark / light mode toggle** is now on every page (index, portfolio, all 12 case pages):

- **Button** — a 🌙 / ☀️ icon button next to the EN/中 toggle in the nav
- **`theme.js`** — shared toggle logic:
  - Saves the choice to `localStorage` (`zhiwei-theme`)
  - First visit: follows the OS `prefers-color-scheme` setting
  - A small inline `<head>` snippet applies the theme *before* CSS loads → no flash (FOUC)
- **`style.css`** — `[data-theme="dark"]` overrides: dark backgrounds for cards/nav/stats/filter chips/tags, adjusted hero & contact gradients, darker thumb placeholders, `color-scheme: dark` for native scrollbars/inputs
- **`i18n.js`** — the toggle's `aria-label` follows the active language (Switch to light/dark mode)

Verified with headless Chrome across two profiles:

- `data-theme` applied correctly, including dark persisted → case pages honor it too
- Screenshot luminance confirmed real dark (28/255 avg) vs light (247/255 avg) rendering
- No missing assets or broken references
