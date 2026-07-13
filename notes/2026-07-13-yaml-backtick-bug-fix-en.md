---
audio: false
generated: true
image: false
lang: en
layout: post
title: YAML Backtick Bug Fix
translated: false
type: note
---

All tests pass. Here's what was wrong and what I fixed:

**Root cause** — Two post files had backticks `` `ll uno` `` in their YAML front matter `title` field. Unquoted backticks are invalid YAML tokens (YAML parser sees the `` ` `` as a character that can't start any token), which caused the front matter parsing to fail silently and the test to catch it.

**Files fixed:**

- `_posts/en/2026-07-13-ll-uno-arduino-serial-monitor-en.md`
- `_posts/zh/2026-07-13-ll-uno-arduino-serial-monitor-zh.md`

**Fix:** Wrapped the title values in double quotes with single quotes inside: `title: "'ll uno' Arduino Serial Monitor"` — this is valid YAML and preserves the intent of code-formatting around `ll uno`.
