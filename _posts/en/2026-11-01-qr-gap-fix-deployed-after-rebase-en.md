---
audio: false
generated: true
image: false
lang: en
layout: post
title: QR gap fix deployed after rebase
translated: false
type: note
---

All fixed and deployed:

1. **Gap change**: 64px → **256px** (4x) between the two QR codes in `_layouts/post.html`
2. **Conflict resolution**: GitHub `main` kept moving because the earlier workflow run was pushing its own commits (translations etc.). I rebased my gap commit on top of each round and pushed — final commit `afbe41c4f` on `main`
3. **Workflow retriggered**: run [#41241271501](https://github.com/lzwjava/jekyll-ai-blog/actions/runs/41241271501) — `pending`, will cancel the in-progress run #41240797123 once it starts (concurrency group `pages` with `cancel-in-progress`), then build & deploy with the new 256px gap

Note: the `gitea` remote wasn't updated (earlier push timed out) — say the word if you want me to retry it.
