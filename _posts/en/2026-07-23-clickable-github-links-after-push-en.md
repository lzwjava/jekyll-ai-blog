---
audio: false
generated: true
image: false
lang: en
layout: post
title: Clickable GitHub Links After Push
translated: false
type: note
---

Look good — syntax checks out. Here's what I changed:

**`ww/note/note_queue_process.py`** — After a successful commit & push, the watch/process command now prints a clickable GitHub link for each pushed note:

```python
# After "[ok] All notes committed and pushed", it prints:
#   https://github.com/lzwjava/jekyll-ai-blog/blob/main/notes/2026-07-23-nanochat-evaluation-built-in-and-external-en.md
```

The new `_print_note_links()` function:

1. Reads the git remote URL to get `owner/repo`
2. Finds the git working tree root to relativize file paths
3. Prints a `https://github.com/<owner>/<repo>/blob/main/<relative-path>` link per file

So your watch output will now look like:

```
[ok] All notes committed and pushed
  https://github.com/lzwjava/jekyll-ai-blog/blob/main/notes/2026-07-23-nanochat-evaluation-built-in-and-external-en.md
[ok] Cleaned 1 processed entry/entries from queue
```
