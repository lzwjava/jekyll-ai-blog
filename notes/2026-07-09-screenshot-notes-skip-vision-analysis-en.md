---
audio: false
generated: true
image: false
lang: en
layout: post
title: Screenshot Notes Skip Vision Analysis
translated: false
type: note
---

Done. Here's what I changed:

**3 files modified:**

**`ww/note/screenshot_log.py`** (`ww screenshot note`)
- Added `--skip-analysis` flag to argparse
- When set: skips `_vision_describe()` and `_summarize_with_extra_prompt()` entirely — creates the note with a simple fallback text and the screenshot embedded, no vision model called
- Also wrapped the `call_openrouter_api_with_messages()` call in `_vision_describe()` with try/except so a non-vision model (like your `sourceful/riverflow-v2.5-pro`) doesn't crash with a raw exception — instead prints a warning with the `--skip-analysis` tip

**`ww/image/interact_note.py`** (`ww screenshot interact-note`)
- Added `--skip-analysis` flag (checked via `sys.argv` since this is an interactive flow, not argparse)
- Same bypass logic: skips vision model, creates note with screenshot embedded

**`ww/main.py`**
- Updated help text to show `[--skip-analysis]` on the `ww screenshot note` line

**Usage:**
```bash
# Skip vision analysis entirely — no model needed
ww screenshot note --skip-analysis

# With a prompt for the note title
ww screenshot note --skip-analysis --prompt "LLaMA.cpp benchmark results"

# Interactive mode
ww screenshot interact-note --skip-analysis
```

The `sourceful/riverflow-v2.5-pro` empty-content error you hit was because it's not a vision model but was set as `VISION_MODEL` — now with `--skip-analysis` you bypass vision entirely.