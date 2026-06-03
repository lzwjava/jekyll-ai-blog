---
audio: false
generated: true
image: false
lang: en
layout: post
title: Silent Module Guard Failure Fix
translated: false
type: note
---

Saved to memory. Summary of the reflection:

Root cause: `ww/main.py` was missing `if __name__ == "__main__": main()`. The Hermes `/note` plugin called `python -m ww.main note` as a subprocess — Python imported the module but never executed anything. Silent no-op with exit code 0.

Why it was hard to notice: the plugin had a safety check that warns if `ww note watch` isn't running. Since the watcher WAS running, no warning appeared. The plugin printed "Queued." and the user assumed it worked. Classic silent failure — no error, no output, no queue entry.

Two fixes applied:
1. `ww/main.py` — added `if __name__ == "__main__": main()` at end
2. Plugin — switched from `sys.executable -m ww.main` to `shutil.which("ww")` CLI call

Lesson: any Python module that might be invoked via `python -m` needs the `__main__` guard. Worth checking across the codebase if other entry points have the same gap.
