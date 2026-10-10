---
audio: false
generated: true
image: false
lang: en
layout: post
title: Align Tests and Push to Main
translated: false
type: note
---

Pushed to `origin/main` — working tree clean.

## Commits

| Commit | Contents |
|---|---|
| `64d35e3` **test: align gpu and note plugin tests with refactored code** | Fixed pre-existing test failures that were blocking the pre-commit hooks |
| `d6ae2db` **feat(linux): add screen-lock command for Ubuntu/GNOME idle lock control** | `ww/linux/screen_lock.py` (new), dispatch in `ww/linux/main.py`, help in `ww/main.py`, `completions/_ww` |

## What had to be fixed to get green hooks

1. **My pyright errors** — `_bad_time()` now annotated `-> NoReturn` so `secs` narrows after the parse-failure check.

2. **17 stale gpu tests** (`tests/linux/test_gpu.py`) — commit `c0a079b` rewrote `ww/linux/gpu.py` (dropping `get_gpu_info`/`check_proxy_settings`) without updating tests. Rewrote them against the current API: `detect_gpus` (DRM sysfs + lspci), nvidia/nouveau/amd memory helpers, temperature, renderer, `tool_available`, and `run()` smoke tests.

3. **2 stale note-plugin tests** (`tests/plugins/test_note_plugin.py`) — they imported the plugin from `~/.hermes/plugins` (machine-dependent, older than the repo copy) and asserted on the removed `create_note_from_content` call. Now they import the repo copy (`agent_plugin/hermes/plugins/`) and assert the queue behavior (`custom_title` / `directory` extras) via a temp queue file.

4. **Queue pollution cleanup** — the old tests were writing a junk `"x"*300` entry into your real `~/.config/ww/note_queue.json`; I removed it, and the reworked tests no longer touch the real queue (verified: 0 entries after a full run).

Final state: **1805 tests pass, 68 skipped**, all hooks pass (`SKIP=bandit` per AGENTS), ruff/pyright clean.