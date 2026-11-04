---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Cleanup: Remove Badge, Tweak Search"
translated: false
type: note
---

All done and verified. Here's what changed:

## Changes made

**1. `_includes/sort.html`** — Removed the `Ask DeepWiki` badge link (`<a class="deepwiki-badge">`). The search form is **kept**, so the `?q=如何学英语` query flow still works unchanged.

**2. `_sass/layout.scss`** — Deleted the now-unused `.deepwiki-badge` / `:hover` styles.

**3. `_sass/dark-mode.scss`** — Added dark-mode styling for the search form so it no longer looks like a harsh white box in dark mode:

- form background → `#2a2a2a` (dark)
- input text → `#f0f0f0`, placeholder → `#9a9a9a`
- softer border (`#4f82e6`) and deeper shadow

## Verification

- Incremental Jekyll build succeeded (only the pre-existing, unrelated Sass deprecation warning remains).
- Rendered output has **0** `deepwiki-badge` occurrences.
- Compiled CSS now has `.dark-mode .deepwiki-form` rules (with the `#2a2a2a` background), plus the form/input/submit styles intact.

Note: I did **not** touch the separate "Devin" header icon-button in `_includes/header.html` that also links to DeepWiki — let me know if you want that removed too.

These edits are uncommitted. Want me to `git add` + commit (and push) them? Also, heads-up: the earlier `git push origin main` to GitHub was aborted, so the previous commits still aren't on the GitHub remote.
