---
audio: false
generated: true
image: false
lang: en
layout: post
title: Note Print Fix Complete
translated: false
type: note
---

The fix is already correct. Here's the state:

- `gitmessageai.py`: the `_print_note_urls` call and both dead functions (`_print_note_urls`, `_get_github_repo_url`) are removed. No more "Note created at" there.
- `note_workflow.py` line 166: the one remaining print is untouched. Only one fires per invocation.

So now `ww note create` prints exactly one `[info] Note created at ...` line, not two. The dead `import re` and `argparse` (was unused?) — no, `argparse` is still used by the `__main__` block. Only `import re` was removed as dead.

The `note_workflow.py` lines 166/168/170 have a mutually-exclusive try/except structure — only one branch runs, so there's no secondary duplication there either.