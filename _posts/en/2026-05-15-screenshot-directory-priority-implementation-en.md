---
audio: false
generated: true
image: false
lang: en
layout: post
title: Screenshot Directory Priority Implementation
translated: false
type: note
---

Done. Here is a summary of the changes:

**Priority for screenshot save directory:**

1. `SCREENSHOT_DIR` from `.env` (global config) -- checked first
2. `[dir]` CLI argument -- fallback if no env config
3. `.` (current dir) for macOS, `assets/screenshots` for Linux -- final default

**Files changed:**

- `/Users/lzwjava/projects/ww/ww/image/screenshot.py` -- Added `load_dotenv()`, reads `SCREENSHOT_DIR` env var first, then falls back to CLI `[dir]`, then `.`. Resolution: `env_dir or cli_dir or "."`
- `/Users/lzwjava/projects/ww/ww/image/screenshot_linux.py` -- Moved all module-level code inside `main()`, added `load_dotenv()`, reads `SCREENSHOT_DIR` with fallback to `assets/screenshots`. Resolution: `env_dir or "assets/screenshots"`
- `/Users/lzwjava/projects/ww/.env` -- Added `SCREENSHOT_DIR=` config entry (currently empty, meaning use defaults)
- `/Users/lzwjava/projects/ww/ww/main.py` -- Updated help text to mention `SCREENSHOT_DIR`
- `/Users/lzwjava/projects/ww/README.md` -- Updated docs

To use it, set `SCREENSHOT_DIR` in your `.env`, e.g.:

```
SCREENSHOT_DIR=/Users/lzwjava/projects/jekyll-ai-blog/assets/screenshots
```

If empty or unset, the old behavior is preserved (`.` for macOS, `assets/screenshots` for Linux, or whatever you pass as `[dir]`).
