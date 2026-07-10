---
audio: false
generated: true
image: false
lang: en
layout: post
title: Convert Clipboard to Jekyll HTML Note
translated: false
type: note
---

Here's the full breakdown of `ww note html`.

---

## What `ww note html` does

Reads your clipboard, converts the content to a **Jekyll-compatible HTML page**, and writes it to `BASE_PATH/notes/` — the same directory as markdown notes — but as a `.html` file that renders visually rich content right in the browser.

## Two workflow modes

| Mode | Command | Behavior |
|------|---------|----------|
| **Direct** | `ww note html` | Creates the HTML file immediately in `BASE_PATH/notes/` |
| **Queued** | `ww note html --queue` | Enqueues it in `~/.config/ww/note_queue.json` with `type: "html"`. `ww note process` or `ww note watch` picks it up later |

The queued path integrates with the existing pipeline — `ww note watch` detects the new entry and auto-processes it, just like markdown notes and logs.

## The pipeline (direct mode)

```
Clipboard content
    ↓
1. clean_grok_tags()     — strip <grok:render> tags
2. clean_content()        — strip leading "# Title" and stray ---
3. _generate_title()      — LLM: short English title (≤6 words, ≤60 chars)
4. _generate_slug()       — LLM: URL-safe slug (hyphens, lowercase, ≤8 parts)
5. _content_to_html()     — LLM: convert to semantic HTML5
6. _format_front_matter() — Jekyll YAML frontmatter
7. write to file          — {date}-{slug}-en.html in BASE_PATH/notes/
```

## The HTML output format

The file starts with Jekyll frontmatter (same layout/title/lang as markdown notes) followed by the HTML body:

```yaml
---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Your Generated Title"
translated: false
type: note
---
```

Then semantic HTML — the LLM produces `<h2>`, `<h3>`, `<p>`, `<pre><code class="language-xxx">`, `<ul>/<ol>`, `<blockquote>`, `<a>`, `<img>`, `<table>`, `<hr>` tags. Code blocks are escaped so Liquid/Jekyll doesn't choke on `{{ }}` or `{% raw %}{% %}{% endraw %}` patterns.

The `layout: post` frontmatter means Jekyll wraps this with the same theme/layout as every other post — headers, footers, sidebar, CSS — so the "visualize" aspect comes from both the semantic HTML structure and the Jekyll theme.

## Files created/changed

| File | Δ | What |
|------|---|------|
| `ww/note/create_note_html.py` | **+189** new | Core module: title generation, LLM→HTML conversion, Jekyll frontmatter, file write |
| `ww/main.py` | +7 | Added `elif subcmd == "html":` dispatch + help text in _print_help() |
| `ww/note/note_queue.py` | +6 | Added `enqueue_html()` — reads clipboard, enqueues with `type: "html"` |
| `ww/note/note_queue_process.py` | +5 | Added `elif entry_type == "html":` in process_queue — calls `create_note_html()` and skips markdown-specific post-processing |
| `completions/_ww` | +1 | Added `'html:Create a Jekyll HTML note (visual)'` to `note_cmds` array |

## Error handling

- **Empty clipboard** → `"Content is empty or invalid."`
- **Duplicate file** → `"HTML note already exists: {path}"` (file not overwritten)
- **LLM failure** → falls back to basic HTML wrapping (`<p>` with line breaks and HTML-escaped content)
- **Reasoning model noise** → title >60 chars auto-truncated to 6 words; trailing quotes stripped

## Usage in context

```bash
# 1. Copy content
cmd+C on some markdown/text/code

# 2a. Create HTML note immediately
ww note html

# 2b. Or queue it and process later
ww note html --queue
ww note process   # later, in batch

# File lands at:
# ~/projects/jekyll-ai-blog/notes/2026-07-07-your-slug-en.html
```
