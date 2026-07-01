---
audio: false
generated: true
image: false
lang: en
layout: post
title: Updated Note and Degree Features
translated: false
type: note
---

Here's the full session summary:

---

## 1. Triggered gh-pages workflow

Ran `gh workflow run gh-pages.yml` on the jekyll-ai-blog repo. Confirmed it started at:
<https://github.com/lzwjava/jekyll-ai-blog/actions/runs/27012471396>

---

## 2. `ww degree --months` filter

**Problem:** `ww degree` showed all 20 scraped articles regardless of age. User only cares about recent 3 months.

**Changes (4 files):**

- `ww/degree/degree.py` — Added `from datetime import datetime, timedelta`, added `--months N` argument (default 3, pass 0 to disable). After fetching entries, filters by date: `e["date"] >= cutoff` where cutoff is `now - N*30 days`.
- `ww/main.py` — Added `--months` to the help text under the Degree section.
- `README.md` / `README-CN.md` — Added `--months` row to the degree command table.

**Usage:**

```
ww degree              # last 3 months (default)
ww degree --months 6   # last 6 months
ww degree --months 0   # all articles (no filter)
```

**Commit:** `b57960d` — `feat(degree): filter articles by --months (default 3)`
**CI:** All 3 workflows passed (Lint & Security, Unit Test, Integration Test).

---

## 3. Duplicate note detection fix

**Problem:** Two notes with the same content were created on 2026-06-05:

- `2026-06-05-embedding-in-english-and-ai-explained-en.md`
- `2026-06-05-embeddings-from-language-to-ai-models-en.md`

The pre-commit hook (`test_duplicate_notes.py`) caught the duplicate and blocked the commit. But the duplicate shouldn't have been created in the first place.

**Root cause:** Two different algorithms were in use:

| Location | Algorithm | Behavior |
| --- | --- | --- |
| `check_duplicate_notes.py` (production) | First 250 chars must be *exactly equal*, then 450/500 chars match | Too strict — missed near-duplicates with slightly different wording |
| `test_duplicate_notes.py` (pre-commit test) | First 200 chars with 90% similarity OR last 200 chars with 90% similarity | Lenient — caught semantic duplicates |

When the same question ("What is an embedding?") was answered twice by the LLM with slightly different titles/wording, the strict production check passed, but the lenient pre-commit test caught it.

**Changes (3 files):**

- `ww/ww/note/check_duplicate_notes.py` — Replaced the strict algorithm with the same first/last 200-char 90% similarity check used by the test. Added `_char_similarity()` helper function. Now production and test use identical logic.
- `ww/tests/note/test_check_duplicate_notes_extended.py` — Updated 2 tests:
  - `test_different_first_and_last_chars_returns_false` — changed to have different endings (was only different at start, but old algo didn't check endings)
  - `test_long_strings_with_many_differences` — changed to expect `True` since first/last 200 chars now match
- `jekyll-ai-blog/notes/2026-06-05-embeddings-from-language-to-ai-models-en.md` — Deleted the duplicate file.

**Commit (ww):** `75ec6ac` — `fix(note): align duplicate detection with test algorithm`
**Commit (jekyll-ai-blog):** `fcf99761f` — `fix(notes): remove duplicate embedding note`
**CI:** All 35 duplicate check tests pass. Pre-commit hook passes.

---

## Why duplicates kept happening

The note creation flow is: hermes `/note` plugin → clipboard → `ww note` → queue → `ww note watch` → `create_note_from_content()`. The duplicate check inside `create_note_from_content()` existed but used an algorithm that was too strict — it required near-exact character-level matches in the first 500 chars. When the LLM generated the same answer to the same question at different times with minor wording differences (different title, slightly different phrasing), the check passed and a duplicate was created. The pre-commit hook used a more forgiving algorithm that caught these, which is why commits kept failing. Now both use the same algorithm.
