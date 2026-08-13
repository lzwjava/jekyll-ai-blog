---
audio: false
generated: true
image: false
lang: en
layout: post
title: Revert homepage to notes
translated: false
type: note
---

Done. The homepage now shows notes instead of posts.

**Change** (`index.html`):
{% raw %}
```diff
-{% include sort.html type='posts' %}
+{% include sort.html type='notes' %}

-{% include post-list.html lang='en' type='posts' %}
+{% include post-list.html lang='en' type='notes' %}
```
{% endraw %}

**Verification:**
- `bundle exec jekyll build` completes successfully (the destination-conflict warnings are pre-existing duplicate-permalink issues, unrelated to this change)
- The generated `_site/index.html` now contains 12,507 `data-type="note"` items and is identical in listing to `notes-en.html`

This effectively reverts commit `0653f4f2d` ("show posts instead of notes on home page"), so `/` now matches the Notes feed.
