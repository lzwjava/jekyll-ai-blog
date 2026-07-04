---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixed tilde expansion in DB_PATH
translated: false
type: note
---

All fixed. Here's what happened and what was done:

**Root cause**: `~/.config/ww/.env` had `DB_PATH=~/projects/jekyll-ai-blog/ww.db` (literal tilde). In `ww/db.py`, `get_db_path()` returned `DB_PATH` directly without `os.path.expanduser()`, so `os.makedirs()` treated the `~` as a literal directory name — creating `fineweb-code-sec-gpt/~/projects/jekyll-ai-blog/ww.db` when you ran from `zz/`.

**Fixes applied:**

1. **`ww/db.py`** — added `os.path.expanduser()` to the `DB_PATH` branch so `~` gets expanded whether it comes from env var or `.env` file. Committed as `1d283a1`.

2. **`~/.config/ww/.env`** — changed `DB_PATH` from `~/projects/jekyll-ai-blog/ww.db` → `~/.config/ww/ww.db` (canonical XDG config location).

3. **`zz` repo** — removed the tracked `~/projects/jekyll-ai-blog/ww.db` file from git history via `git commit --amend`, deleted the literal `~` directory tree, and added `*.db` to `.gitignore` to prevent future sqlite files from being accidentally committed.

Now when `ww` writes its command history db, it goes to `~/.config/ww/ww.db` with the tilde properly expanded, so no more ghost directories under your project.
