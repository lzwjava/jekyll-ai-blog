---
audio: false
generated: true
image: false
lang: en
layout: post
title: Pre-commit Pytest Hook Implementation Summary
translated: false
type: note
---

Here's the summary:

WHAT WE DID: Added `pytest` as a pre-commit hook so tests run on every `git commit` (~8s, 1860 tests, all pass).

PARALLEL TESTS: Tested `pytest-xdist` with `-n 2`, `-n 4`, `-n auto`. No improvement — individual tests are too fast (~4ms each) for parallelism overhead to pay off. Also got `Bad file descriptor` errors from I/O tests conflicting with process forking.

VERDICT: Keep sequential. Parallel would only help if individual tests were 100ms+ (API calls, model loading). Added `pytest-xdist` to dev deps anyway for future use with slower suites.

FILES CHANGED:
- `.pre-commit-config.yaml` — added `unit-tests` local hook
- `pyproject.toml` — added `[dependency-groups]` with pytest, pytest-xdist, coverage
