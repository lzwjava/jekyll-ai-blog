---
audio: false
generated: true
image: false
lang: en
layout: post
title: All 1652 Tests Pass
translated: false
type: note
---

All **1652 tests pass** with 3 skipped (same as before - the skipped ones are for optional dependencies). Zero errors, zero failures.

## Summary of Fixes

Here's what was wrong and what I fixed:

### 1. `ww/env/__init__.py` — `load_env()` only loaded from `~/.config/ww/.env`

**Problem**: The `load_env()` function only loaded from `~/.config/ww/.env`, but the AGENTS.md docs and tests expected it to also load from `BASE_PATH`, CWD, and project root.

**Fix**: Updated `load_env()` to load `.env` from 4 locations in order (later overrides earlier):

- Current working directory
- Project root (parent of `ww/`)
- `BASE_PATH` env var (if set)
- `~/.config/ww/.env`

### 2. `tests/social/test_x_bulk_unfollow.py` — 11 errors + 1 failure

The source `ww/social/x_bulk_unfollow.py` was significantly refactored (batch-based LLM picking, retry loop in `launch_chrome`) but the tests weren't updated.

**Fixes**:

- **`test_launch_chrome`**: Fixed mock target from `ww.social.x_bulk_unfollow.socket.create_connection` (fails since `socket` is imported inside the function) to `socket.create_connection`. Updated sleep assertion since the function now has a connection retry loop that exits immediately when mocked.
- **`TestAskLlmShouldUnfollow` → `TestAskLlmPickUnfollow`**: Rewrote all 5 tests to match the new `ask_llm_pick_unfollow(profiles)` function that returns `(index, reason)` instead of the old `ask_llm_should_unfollow(profile)` that returned `(decision, reason)`.
- **`TestUnfollowWithLlm`**: Completely rewrote all 5 tests. The old tests used `dry_run` (removed from API), mocked `ask_llm_should_unfollow` (renamed), and had complex page mock logic that didn't match the new code's control flow. New tests mock `collect_batch` and `do_unfollow` at a high level with proper `side_effect` functions to handle the double-call-per-iteration pattern.
- **`_make_page_with_cells` helper**: Simplified to return consistent cell counts (the old version decremented count after first call).
