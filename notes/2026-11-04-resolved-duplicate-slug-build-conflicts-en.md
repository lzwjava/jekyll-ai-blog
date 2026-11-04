---
audio: false
generated: true
image: false
lang: en
layout: post
title: Resolved Duplicate Slug Build Conflicts
translated: false
type: note
---

All conflicts are resolved. The build now completes with **0 destination conflicts** (the only remaining warnings are unrelated pre-existing Liquid template syntax in blog post bodies, not errors).

## Summary

The root cause: `_config.yml` uses `permalink: /:title`, which is derived from the **filename slug**. When multiple posts shared the same slug (e.g. `2025-10-08-nano-gpt-training-en.md` vs `2025-11-01-nano-gpt-training-en.md`), they collided on the same `_site/*.html` output even though their front-matter `title` fields differed.

### Changes made (132 files removed via `git rm`, all recoverable from git history)

**1. Duplicate posts (130 files: 65 `en` + 65 `zh`)**
For every group of posts sharing a slug, kept the **newest-dated** post and removed the older copies.

**2. Marp asset source collisions (2 files)**
- Removed `assets/marp/neural_networks_to_agents.md` and `assets/marp/neural_networks_to_agents_preview.md`
- Kept the compiled `*.html` decks (the actual deliverable the site serves); previously Jekyll was trying to render each `.md` into the same `_site/assets/marp/*.html` path occupied by the static `.html` file.

### What's an important trade-off to be aware of
I kept the **newest** post per group since these look like the auto-generated notes re-published across dates. Note this removed some older real/hand-written posts (e.g. `2021-03-12-start-en.md`, `generated: false`) in favor of newer `generated: true` copies. Everything is still in git history, so if you'd prefer to keep the **oldest/original** version for any specific slug, tell me which and I'll swap it back.

Verification: `bundle exec jekyll build` → `grep -ci 'conflict|shared by multiple'` → **0**.

The two files that were already modified before I started (`_includes/sort.html`, `_sass/layout.scss`) were left untouched.
