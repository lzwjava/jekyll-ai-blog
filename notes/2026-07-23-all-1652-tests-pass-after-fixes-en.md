---
audio: false
generated: true
image: false
lang: en
layout: post
title: All 1652 tests pass after fixes
translated: false
type: note
---

All **1652 tests pass** (3 skipped for optional dependencies).

To recap what was done:
- **Reverted** `ww/env/__init__.py` to the original simple version (only loads `~/.config/ww/.env`)
- **Updated** `tests/test_env.py` — replaced the two `BASE_PATH`-dependent tests with tests that verify the actual XDG config loading behavior using `Path.home()` mocking
- **Fixed** `tests/social/test_x_bulk_unfollow.py` — all 12 broken tests (11 errors + 1 failure) fixed to match the refactored `ww/social/x_bulk_unfollow.py`