---
audio: false
generated: true
image: false
lang: en
layout: post
title: Timeouts and Error Handling Improvements
translated: false
type: note
---

Done. Here's a summary of all changes across 3 files:

**1. `/Users/lzwjava/projects/ww/ww/llm/openrouter_client.py`**
- Added `timeout=(5, 30)` to `requests.post()` — 5s connect, 30s read (was: no timeout = hang forever)
- Same fix for the streaming endpoint

**2. `/Users/lzwjava/projects/ww/ww/note/create_note_from_clipboard.py`**
- Replaced `sys.exit(1)` with `raise ValueError(...)` for empty/short content (was: killed the entire Hermes CLI)
- Removed unused `sys` import

**3. `/Users/lzwjava/projects/ww/ww/note/create_note_utils.py`**
- Replaced `sys.exit(1)` with `raise RuntimeError(...)` in `_call_llm_or_exit()` (was: killed the CLI on LLM failure)
- Removed unused `traceback` and `sys` imports

**4. `/Users/lzwjava/.hermes/plugins/note/__init__.py`**
- Added `import os`
- Added fallback MODEL env var loading from `~/projects/ww/.env` when dotenv doesn't populate it
- Added `print("Generating title via LLM...")` so user sees feedback
- Added `ValueError` catch for content validation errors (returns clean message instead of traceback)

Try running `/note` again — you should now see "Generating title via LLM..." immediately, and if the API is slow it'll timeout after 30s instead of hanging forever.
