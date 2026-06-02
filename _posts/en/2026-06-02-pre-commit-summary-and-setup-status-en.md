---
audio: false
generated: true
image: false
lang: en
layout: post
title: Pre-commit Summary and Setup Status
translated: false
type: note
---

Pre-commit is set up and running. Here's the summary:

```
=== Pre-commit Status ===

Config: /Users/lzwjava/projects/jekyll-ai-blog/.pre-commit-config.yaml

Hooks installed:
  - trailing-whitespace       ✅ (auto-fixed ~300 files on first run)
  - end-of-file-fixer         ✅ (auto-fixed files)
  - check-yaml                ✅
  - check-toml                ✅
  - check-merge-conflict      ✅
  - debug-statements           ✅
  - check-ast                 ✅
  - check-added-large-files   ✅
  - ruff (lint + fix)         ❌ 41 existing lint errors (F841 unused vars, E741 ambiguous names, etc.)
  - ruff-format               ✅
  - pyright                   ❌ 147 errors (mostly missing module imports — project scripts aren't packages)
  - bandit                    ❌ 172 issues (mostly low: subprocess usage, requests without timeout)
  - unit-tests                ❌ 1 failure: 4 duplicate note pairs in notes/
```

Key changes made:

- Installed pre-commit via `uv tool install pre-commit` (v4.6.0)
- Changed unit-tests entry from `uv run python -m pytest` to `python3 -m unittest discover -s tests/workflow -q` (matches CI, avoids missing OPENROUTER_API_KEY in llm tests)
- Removed `detect-secrets` hook (no `.secrets.baseline` file exists)
- Removed `-c pyproject.toml` from bandit args (no pyproject.toml exists)
- Changed bandit target from `ww/` to `scripts/`

The ruff/pyright/bandit failures are all pre-existing code issues — not caused by the pre-commit setup. The duplicate notes test failure is a data issue (4 pairs of similar notes). The hook infrastructure itself is working correctly.
