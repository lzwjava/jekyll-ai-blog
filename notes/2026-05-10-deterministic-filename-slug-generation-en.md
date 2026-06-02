---
audio: false
generated: true
image: false
lang: en
layout: post
title: Deterministic Filename Slug Generation
translated: false
type: note
---

Clean and correct. Here's the summary of this second fix:

**The problem:** The second LLM call (for `short_title`) had the same issue -- the model rambled and produced garbage like `basedonthetitlerequirementhereisaconcisefilenameblockchain-learning-reflectionmd`. After `_validate_and_clean_short_title` stripped all non-alphanumeric chars, the rambling text collapsed into one long word with no hyphens, failing the "max 8 words" validation.

**The fix:** Eliminated the second LLM call entirely. Instead of asking the model to generate a filename slug (which is a purely mechanical task), I derive it programmatically from `full_title` using `_title_to_slug`:

1. Lowercase, remove quotes, replace spaces with hyphens
2. Strip non a-z0-9- characters
3. Collapse repeated hyphens
4. Truncate to 8 words max, 80 chars max

**Why this is better:**
- Zero risk of LLM rambling -- it's pure string manipulation
- One fewer API call (saves time and money)
- Deterministic -- same title always produces the same slug
- The slug derivation logic was already proven in `_titles_from_custom` (line 42-45), this just applies the same approach with slightly better validation
