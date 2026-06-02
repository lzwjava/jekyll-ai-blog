---
audio: false
generated: true
image: false
lang: en
layout: post
title: Race Condition in File Creation
translated: false
type: note
---

Looking at the code path, a lock isn't the root cause. The duplicate happens because `create_filename` silently falls back to a counter suffix when the slug already exists.

**The race path the user hypothesizes (concurrent `ww note`):**

Two invocations on the same machine can race past `check_duplicate_notes()`:

1. Both pass `check_uncommitted_changes()` and `git pull --rebase`
2. Both call `check_duplicate_notes()` — neither sees the other's file yet
3. Both call `create_filename()` — one gets `...-en.md`, the other hits the fallback at `create_note_utils.py:77-79`:

   ```python
   while os.path.exists(file_path):
       file_path = os.path.join(notes_dir, f"{date_str}-{short_title}-{counter}-en.md")
   ```

4. Both commit & push — end result: two near-identical notes.

A lock would prevent *this* race. But it wouldn't prevent the more common path.

**The likelier path (and what the test output actually shows):**

The pair `2026-04-20-iphone-daylight-timelapse-en.md` and `...-timelapse-1-en.md` is the signature of the counter-suffix branch. That branch can be reached even *sequentially*, not just concurrently, when:

- `check_duplicate_notes` misses because `_are_notes_quick_similar` requires the first 250 chars byte-identical + ≥450/500 char matches — any whitespace/clean-up diff dodges it (`check_duplicate_notes.py:12-30`)
- LLM regenerates the same slug for similar-but-not-identical clipboard content
- `create_filename` treats an existing slug as a signal to disambiguate, not as a red flag

**What actually fixes it:**

1. Make slug collision fatal in `create_filename` — if `{date}-{slug}-en.md` exists, abort (or require a flag). The counter-suffix fallback is the real hole.
2. Strengthen `check_duplicate_notes` to also flag same-date same-slug before writing.
3. Optionally add a `flock` on the notes dir for belt-and-suspenders against the in-process race.

Fix (1) is the highest-leverage — it closes both the race and the sequential repeat. Want me to make that change?
