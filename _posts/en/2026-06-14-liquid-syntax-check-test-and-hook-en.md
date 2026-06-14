---
audio: false
generated: true
image: false
lang: en
layout: post
title: Liquid syntax check test and hook
translated: false
type: note
---

Done. Here's the summary:

**What was added:**

1. `tests/workflow/test_liquid_syntax.py` — scans `_posts/` and `notes/` for bare `{% raw %}{% %}{% endraw %}` outside of `{% raw %}...{% endraw %}` blocks. Reports file path, line number, and content for each violation.

2. `.pre-commit-config.yaml` — new `liquid-syntax-check` hook that runs the test on every commit (`always_run: true`).

**How it works:**

- Finds all `{% raw %}{% %}{% endraw %}` patterns (empty Liquid tags that cause fatal `Liquid::SyntaxError`)
- Checks each occurrence is inside either:
  - A file-level `{% raw %}...{% endraw %}` wrapper
  - An inline `{% raw %}{% %}{% endraw %}` escape
- Reports violations with clear fix instructions

**Also fixed:** `notes/2026-06-14-liquid-tag-build-fix-en.md` had 3 bare `{% raw %}{% %}{% endraw %}` — escaped with inline raw/endraw.

**Note:** bandit has a pre-existing false positive (B608 on `scripts/recommendation/api_utils.py`) unrelated to this change. You may want to add B608 to the skip list.
