---
audio: false
generated: true
image: false
lang: en
layout: post
title: Hand-Edited YAML Order Breaks Test
translated: false
type: note
---

## Root cause

Two layers conspire here:

**1. `scripts/create/file.py` template has no `prompt` field.**
The template emits keys in this order: `audio, generated, image, lang, layout, title, translated` — already alphabetical, no `prompt`. So the freshly created file is fine.

**2. `prompt` was added by hand later, appended after `title`.**
At some point you (or an editor) added the translation hint:
```
prompt: Do not translate specific items such as project names...
```
right after `title:`. Alphabetically `prompt` belongs between `layout` and `title`, not after it. That single hand-edit broke the ordering — and it's why the test flags exactly one misplaced key (`title` appearing where `prompt` should be).

**Why translated copies don't fail this test:**
`scripts/translation/markdown_translate_client.py:54` runs the dict through `yaml.dump(...)`, which sorts keys alphabetically by default. So `-zh.md`, `-ja.md`, etc. come out correctly ordered. But the source `-en.md` is never round-tripped through `yaml.dump`, so the hand-edited order is preserved verbatim.

**Why both `_posts/en/...` and `original/...` fail:**
They're the same file moved by `publish.py:78` (`shutil.move`) — `publish.py` doesn't normalize frontmatter. The bad order propagates.

## Fix options

- **Quick fix (just this file):** move the `prompt:` line in both `original/` and `_posts/en/` copies to sit between `layout:` and `title:`.
- **Permanent fix:** either add a `prompt: ""` placeholder slot in `scripts/create/file.py` template (alphabetical position), or have `publish.py` normalize key order via `yaml.dump` before moving the draft.

Want me to apply the quick fix to the two files, the permanent fix in `publish.py`, or both?