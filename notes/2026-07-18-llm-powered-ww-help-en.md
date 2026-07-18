---
audio: false
generated: true
image: false
lang: en
layout: post
title: LLM-powered ww help
translated: false
type: note
---

Done. Here's what was implemented:

**New command: `ww help <file_path>`**

It uses the LLM (`deepseek/deepseek-v4-flash`) to read a module file, look up how it's wired in `main.py`, and tell you the exact `ww` command to use.

```
ww help ww/gcp_speech/transcribe.py
ww help ww/ffmpeg/merge.py
ww help ~/projects/ww/ww/display/appearance.py
```

**Files changed:**

- **`ww/help_llm/help.py`** (new) — the help module: reads the target file + scans `main.py` for its import/wiring, sends both to the LLM, prints the explanation
- **`ww/help_llm/__init__.py`** (new) — empty package init
- **`ww/main.py`** — added `help` as a separate command group (`ww help <path>` → LLM help, `ww help` → existing help; `--help`/`-h` still shows the help page unchanged)
- **`~/.zsh/completions/_ww`** — added `help` to commands list and dispatch case (tab-completes file paths)
