---
audio: false
date: 2025-09-13
generated: true
image: false
lang: en
layout: post
model: openai/gpt-5
title: GitHub Pages Requires Public Repositories
translated: false
type: note
---

Right — if you make your GitHub Pages repository private, you lose the free GitHub Pages hosting.

GitHub Pages only works automatically when the repo is **public**. If the repo is private, the `github.io` site won’t be published unless you’re on a **GitHub Enterprise plan with Pages for private repos enabled** (that’s a paid feature, not included in free or standard personal accounts).

So for your personal blog at `username.github.io`:

* **Public repo** → GitHub Pages builds and serves it at `https://username.github.io/`.
* **Private repo (free account)** → GitHub Pages is disabled.
* **Private repo (Enterprise)** → Still works, but only if your organization enables Pages for private repos.

Do you want me to also explain a workaround (like keeping your main repo private but syncing just the `_site` output to a separate public repo for publishing)?
