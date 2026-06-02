---
audio: false
generated: true
image: false
lang: en
layout: post
title: Autolink Parsing Source Code Exploration
translated: false
type: note
---

For exploring how `<>` autolinks are actually parsed, here are the best open-source options:

**Best for learning implementation:**

1. **[markdown-it](https://github.com/markdown-it/markdown-it)** (JavaScript)
   - Modular, readable code
   - Autolink parsing: check `lib/rules_inline/autolink.js`
   - Easy to trace through the regex and state machine
   - Can test in browser with `npm install markdown-it` + Node REPL

2. **[CommonMark reference](https://github.com/commonmark/commonmark-spec)** (multiple implementations)
   - Official spec + reference implementations in C, Python, JavaScript
   - `commonmark.js` implementation is clean
   - Spec document itself shows exactly what `<>` should match

3. **[mistune](https://github.com/lepture/mistune)** (Python)
   - Minimal, ~500 lines of core parsing
   - Autolink pattern: `AUTOLINK = r'<([^ >\\\]|\\.)+'`
   - Easiest to hack on if you're Python-first
   - `pip install mistune && python3 -c "import mistune; print(mistune.parse('<https://example.com>'))"`

4. **[Pulldown-cmark](https://github.com/raphlinus/pulldown-cmark)** (Rust)
   - High-performance, used in production (Zed, rust-lang.org)
   - Autolink handling is in `parser/mod.rs`
   - Great if you want to learn Rust + see real-world Rust code

**Quick dive:**

```bash
git clone https://github.com/markdown-it/markdown-it.git
cd markdown-it
cat lib/rules_inline/autolink.js
```

The regex pattern and inline rule definition are tiny — you'll understand it in 5 minutes.

**My suggestion:** Start with **markdown-it** if you want readability, or **mistune** if you prefer Python. Both are small enough to fully understand in an afternoon.
