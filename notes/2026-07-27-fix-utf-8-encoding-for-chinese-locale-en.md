---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix UTF-8 Encoding for Chinese Locale
translated: false
type: note
---

All three fixes are applied correctly. Here's a summary of what was changed:

**Problem:** On Windows with Chinese locale (gbk/cp936), `Path.read_text()` defaults to the system encoding instead of UTF-8, causing `'gbk' codec can't decode byte 0x94` when reading the queue JSON file.

**Fixes applied:**

1. **`ww/note/note_queue.py` — `_load_queue()` (line 28):** Changed `qf.read_text()` → `qf.read_text(encoding="utf-8")` so JSON loading uses UTF-8 explicitly.

2. **`ww/note/note_queue.py` — `_save_queue()` (line 33):** Changed `tmp.write_text(...)` → `tmp.write_text(..., encoding="utf-8")` so the file is also written as UTF-8 (consistent with reading).

3. **`ww/note/note_watcher.py` (line 88):** Changed `qf.read_text()` → `qf.read_text(encoding="utf-8")` in the watcher's change-detection loop.