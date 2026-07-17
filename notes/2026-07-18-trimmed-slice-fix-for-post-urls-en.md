---
audio: false
generated: true
image: false
lang: en
layout: post
title: Trimmed slice fix for post URLs
translated: false
type: note
---

**Summary of the bug and fix**

File: `_layouts/post.html:90-100`

**Root cause:** After the existing `replace` filter strips the language suffix (`-en`, `-zh`, `-hant`) from `base_name`, a redundant post-processing block re-slices the **already-clean name** using `length - 3` (or `length - 5` for `hant`), chopping 3 extra characters off the front.

For `2026-02-15-web-analytics-zh.md`:
1. `replace` produces `web-analytics` (correct)
2. Post-slice: `base_name[:15]` → `web-analyt` (broken, only 12 chars remain)
3. Select URL becomes `/web-analyt-zh` — 404

**Fix:** Removed the entire post-slice arithmetic block. The `replace` step already produces the correct value; nothing else is needed.

With the fix applied, all language pairs now generate the correct URL (verified by simulation).
