---
audio: false
generated: true
image: false
lang: en
layout: post
title: Automated HTML to Image Pipeline
translated: false
type: note
---

Here's the full pipeline:

1. **Read the source** — Started from `timesheet/june-zh.md`, the Chinese attendance requirements markdown.

2. **Build styled HTML** — Created a self-contained HTML file with:
   - Google Fonts (Noto Sans SC) for Chinese rendering
   - Inline CSS with a card-based layout (white card on light gray bg)
   - Stats cards, calendar grid (CSS grid), tables, progress bars, color-coded sections
   - All styles inline (no external deps) so it renders standalone

3. **Render in headless browser** — Used `browser_navigate` to load the local HTML file in a Browserbase-managed Chromium instance. The page renders exactly like a real browser — fonts, grid layout, emoji, gradients all work.

4. **Get content dimensions** — Ran `document.body.scrollWidth/scrollHeight` via JS console to know the exact pixel size of the content (e.g. 720×3008 for the comprehensive version).

5. **Screenshot** — Used `browser_vision` to capture a full-page screenshot. Problem: the browser viewport is 1280px wide but content is only 720px, leaving ~560px of white space on the right.

6. **Crop to content** — Used ImageMagick `convert -crop 720x3008+0+0 +repage` to trim the image to exactly the content bounds, eliminating all white space.

7. **Convert to JPG** — Used `sips -s format jpeg -s formatOptions 95` (macOS native) or ImageMagick to convert PNG → JPG at 95% quality.

8. **Verify** — Ran `vision_analyze` on the final image to confirm layout, readability, and no clipping.

The key trick: browser screenshots always capture the full viewport (1280px wide by default), not just the content. So you either need to:

- Resize the viewport to match content width, or
- Crop after the fact with ImageMagick

I went with crop since it's more reliable — the HTML body width is set to a fixed px value (680/720) and the card fills that, so cropping to `body.scrollWidth` is exact.

Tools used:
  HTML/CSS  → write_file
  Browser   → browser_navigate + browser_vision (Chromium rendering + screenshot)
  JS        → browser_console (measure content dimensions)
  Crop      → ImageMagick convert (tight bounding box)
  Convert   → sips or ImageMagick (PNG → JPG)
  Verify    → vision_analyze (QA the output)
