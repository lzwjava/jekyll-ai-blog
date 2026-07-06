---
audio: false
generated: true
image: false
lang: en
layout: post
title: New ww note html command
translated: false
type: note
---

Done. Here's a summary of everything I added:

---

**`ww note html` — New command**

Reads clipboard content and creates a Jekyll-compatible `.html` visual note.

**Usage:**

```
ww note html                   # Create HTML note directly in BASE_PATH/notes/
ww note html --queue           # Queue for deferred processing via `ww note process`
ww note html --dir /path       # Custom output directory
```

**What it produces:**

A file like `2026-07-07-slug-en.html` in `~/projects/jekyll-ai-blog/notes/` with:

- **Jekyll frontmatter** (layout: post, title, lang, type)
- **Semantic HTML body** — LLM-converted from clipboard content with proper `<h2>`, `<pre><code class="language-xxx">`, `<ul>`, `<blockquote>`, etc.
- **Escaped code blocks** — safe for Jekyll/Liquid rendering

**Files changed:**

| File | Change |
| ------ | -------- |
| `ww/note/create_note_html.py` | **New** — module: title gen, slug gen, LLM→HTML conversion, Jekyll frontmatter |
| `ww/main.py` | Added `ww note html` subcommand dispatch + help text |
| `ww/note/note_queue.py` | Added `enqueue_html()` for queue-based workflow |
| `ww/note/note_queue_process.py` | Added `entry_type == "html"` handler in process loop |
| `completions/_ww` | Added `html` completion entry |

**Queue integration:** `ww note html --queue` → `ww note watch` auto-processes it, or `ww note process` drains it. Works exactly like `ww note log` but produces Jekyll HTML instead of raw log files.
