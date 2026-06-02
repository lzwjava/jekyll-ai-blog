---
audio: false
generated: true
image: false
lang: en
layout: post
title: Note Saving from Conversation History
translated: false
type: note
---

Done. Here's what was implemented:

**3 changes across 2 files:**

1. `hermes_cli/commands.py` — Added `CommandDef("note", ...)` next to the `copy` command
2. `cli.py` — Added dispatch `elif canonical == "note":` in `process_command()`
3. `cli.py` — Added `_handle_note_command()` method (58 lines) right after `_handle_copy_command()`

**How it works:**

The `/note` command does what `ww note` does — calls `create_note_from_content()` from the `ww` package — but instead of reading from the clipboard, it takes the last assistant response directly from `self.conversation_history`.

**Usage:**

```
/note                        # save last response as note (uses LLM to generate title)
/note 3                      # save 3rd assistant response
/note --title "My Title"     # save with a custom title (skips LLM title generation)
/note --dir ~/my-notes       # save to a custom directory (default: $BASE_PATH/notes)
/note 2 --title "Foo" --dir ~/notes
```

**Key details:**
- Uses `ww`'s `create_note_from_content()` — generates front matter, slug, calls LLM for title if no `--title` given
- Falls back gracefully if `ww` isn't installed (`pip install -e ~/projects/ww`)
- Notes go to `$BASE_PATH/notes/` by default (same as `ww note`), or whatever `--dir` you pass
- No git operations, MathJax fixing, or browser opening — just creates the file. The full `ww note` pipeline (git pull, push, mathjax) stays in the `ww` CLI

**To test:** restart Hermes and run `/note` after getting a response. The `ww` package is already installed in your venv.
