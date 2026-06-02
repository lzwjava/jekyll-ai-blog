---
audio: false
generated: true
image: false
lang: en
layout: post
title: LLM Title Fixes Summary
translated: false
type: note
---

Good. Here's a summary of the three fixes applied:

**Problem:** The LLM ignored the "respond with only the title" instruction and returned 1518 chars of analysis instead of a 6-word title. The code then crashed with a `ValueError`.

**Fixes (3 changes across 2 files):**

1. **`create_note_utils.py` -- `max_tokens=60` on the API call:** This is the key fix. Previously no `max_tokens` was set, so the model could ramble freely. 60 tokens is generous for 6 words but cuts off long explanations.

2. **`create_note_utils.py` -- Retry logic (3 attempts):** Instead of crashing on the first too-long title, it retries up to 3 times with a warning. Only raises `ValueError` after exhausting retries.

3. **`create_note_from_clipboard.py` -- Stronger prompt:** Changed from a long instruction to a concise prompt ending with `\n\nTitle:` -- this primes the model to complete with just the title, which works better with many models than imperative instructions.
