---
audio: false
generated: true
image: false
lang: en
layout: post
title: Focus Testing on High-Churn Files
translated: false
type: note
---

Here's the data and the strategy:

**Churn data (top 15 files by commit count):**

```
62  ww/main.py                     ← CLI entry point, by far #1
12  ww/note/create_normal_log.py
10  ww/note/create_note_utils.py
10  ww/note/create_log.py
 9  ww/image/screenshot.py
 8  ww/sync/remote.py
 8  ww/llm/openrouter_client.py
 8  ww/github/gitmessageai.py
 6  ww/note/note_workflow.py
 6  ww/note/create_note.py
 6  ww/note/create_note_from_clipboard.py
 6  tests/test_main.py
 5  ww/note/screenshot_log.py
 5  ww/git/git_update.py
 4  ww/search/search_*.py (4 files)
 4  ww/git/git_squash.py, git_show_command.py, etc.
```

**The distribution is extreme:**

- 721 tracked files in `ww/`
- 45 files have 3+ commits (~6%)
- 693 files have 1-2 commits (~94%) — added once, barely touched

**Why this strategy works:**

1. **Churn = bug injection surface.** Files that change frequently are where regressions happen. A file touched 62 times (main.py) has 62x more opportunities for bugs than a file touched once.

2. **The 80/20 is even more extreme here.** The top ~45 files (6%) account for the vast majority of commits. Testing those covers where 80%+ of future changes will land.

3. **Current coverage is backwards.** You have 60-100% on note/git/image/utils — but some high-churn files like `main.py` (62 commits), `create_normal_log.py` (12), `screenshot.py` (9), `remote.py` (8), `openrouter_client.py` (8) may have zero or thin coverage.

4. **The 0%-coverage untested modules (agent/, audio/, cloud/, etc.) are mostly low-churn.** They were built once and left alone. Testing them has low ROI — they rarely change, so bugs there are rare.

**The playbook:**

```
Step 1: git log --format= --name-only ww/ | sort | uniq -c | sort -rn > /tmp/churn.txt
Step 2: For each file in the top 30% (~20-25 files):
   - Does a test file exist? (tests/*/<module>/test_<name>.py)
   - If yes, what's the coverage? (pytest --cov=<module>)
   - If no, that's a gap — write a test
Step 3: Priority order = churn count × (1 - existing_coverage)
```

**The formula:** `priority = commits × (1 - coverage%)` — this gives you a ranked list where a file with 62 commits and 0% coverage (main.py) scores highest, and a file with 1 commit and 80% coverage scores near zero.

**Bottom line:** Yes, this is the right way to think about it. Testing high-churn files first is the single highest-leverage move for improving real-world test quality. The current 12% overall number is misleading — if you cover the top 30 files by churn well, you're protecting where it actually matters.
