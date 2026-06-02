---
audio: false
generated: true
image: false
lang: en
layout: post
title: Tab Killer Naming Convention Justification
translated: false
type: note
---

**Question:** Should the repository/tool be named `tabs-killer` or `tab-killer`?

**Answer:**

`tab-killer` — singular.

**Reasoning:**

The tool kills *the concept of a tab* (or tabs generically), not a specific collection called "tabs." CLI tools conventionally use the singular noun for what they operate on:

- `file-watcher`, not `files-watcher`
- `process-killer`, not `processes-killer`
- `port-scanner`, not `ports-scanner`
- `vim` kills buffers, `grep` finds lines — always singular

The pattern is `<singular-noun>-<verb-agent>`. You're building a *tab killer*, like a *bug killer* — not a *bugs killer*.

**`tabs-killer` reads as grammatically awkward** — it sounds like "a killer of tabs" phrased by a non-native speaker. `tab-killer` is idiomatic English and consistent with CLI tool naming conventions.

**Recommendation:** Rename to `tab-killer`. Since it's your repo, a simple GitHub rename + update README. If you have any aliases or scripts pointing to it, one sed pass fixes them:

```bash
sed -i 's/tabs-killer/tab-killer/g' ~/.zshrc ~/.bashrc ~/your-scripts/**/*.sh
```
