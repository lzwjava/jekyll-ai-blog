---
audio: false
generated: true
image: false
lang: en
layout: post
title: Automated Liquid Fix in Blog Pipeline
translated: false
type: note
---

Both repos clean and pushed. Summary:

---

**What was done:**

1. **Fixed ~160 blog files** in `jekyll-ai-blog` across `_posts/` and `notes/` — wrapped unprotected `{{ }}`/`{% %}` patterns with `{% raw %}...{% endraw %}` so the Jekyll build passes (0 Liquid Exceptions, 28K site files generated)

2. **Added auto-fix to the `ww` note pipeline** — `fix_liquid_raw_tags()` in `create_note_utils.py` is called automatically in `write_note()` before every note is saved. It:
   - Detects fenced code blocks with `{{ }}` or `{% %}` 
   - Wraps them with `{% raw %}...{% endraw %}`
   - Skips already-wrapped blocks (no double-wrapping)
   - Logs: `[fix] Wrapped N code block(s) with {% raw %} tags for Liquid safety`

This means future notes created via `ww note` will never produce Liquid build errors again — the fix is automatic at creation time, before the note ever hits the Jekyll build.