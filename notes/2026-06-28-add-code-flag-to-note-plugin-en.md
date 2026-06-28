---
audio: false
generated: true
image: false
lang: en
layout: post
title: Add --code flag to note plugin
translated: false
type: note
---

Done. Updated `~/.hermes/plugins/note/__init__.py`:

- Added `--code` flag parsing
- When `--code` is set: calls `wrap_code_snippets()` on the assistant response content before enqueuing, and stores `"code": true` in the queue entry
- Updated docstring and `args_hint`

Usage:
```
/note --code              # save last response with code wrapping
/note 3 --code            # save 3rd response with code wrapping
/note --title "Foo" --code
```

The queue entry flows through `ww note watch` / `ww note process` as usual — the content is already wrapped at enqueue time, same as the CLI path.
