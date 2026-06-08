---
audio: false
generated: true
image: false
lang: en
layout: post
title: Ctrl+C Handling in Iclaw
translated: false
type: note
---

All clean. Here's a summary of the 3 changes:

**1. `iclaw/exec_tool.py` — catch KeyboardInterrupt in exec_command**
When Ctrl+C fires during `subprocess.run()`, the KeyboardInterrupt is now caught and returns `"Error: Command interrupted by user."` instead of bubbling up and killing iclaw.

**2. `iclaw/main.py` line 149 — Ctrl+C at the prompt doesn't exit**
Separated `EOFError` (Ctrl+D → exits with "Goodbye!") from `KeyboardInterrupt` (Ctrl+C → just clears the line and continues the REPL).

**3. `iclaw/main.py` line 626 — Ctrl+C during chat/tool-call loop cancels the current turn**
Saves `msg_count_before = len(messages)` before entering the chat block. On KeyboardInterrupt, rolls back all messages added during that turn (`del messages[msg_count_before:]`), prints "Interrupted.", and returns to the prompt. This covers Ctrl+C during API calls, web_search, edit, browser tools — not just exec.

The key insight: `KeyboardInterrupt` is a `BaseException`, not `Exception`, so the existing `except Exception` handler at line 629 was never catching it — it was always bubbling up to the REPL loop and exiting iclaw.
