---
audio: false
generated: true
image: false
lang: en
layout: post
title: Expanding User Paths in Environment Variables
translated: false
type: note
---

Pushed. Commit `cb60fb4` on `main` → `origin/main`.

Summary of what went up:

- **`ww/env/__init__.py`** — `load_env()` now expands `~` in `BASE_PATH` and writes the resolved path back to `os.environ`
- **`ww/note/create_note_utils.py`** — `get_base_path()` calls `os.path.expanduser()` for defense-in-depth
- **`ww/db.py`** — expanded before constructing `ww.db` path
- **`ww/llm/update_env.py`** — expanded before looking for `.env`
- **`ww/main.py` + `completions/_ww` + `ww/env/github_desktop.py`** — also included the github-desktop command that was sitting in your working tree
