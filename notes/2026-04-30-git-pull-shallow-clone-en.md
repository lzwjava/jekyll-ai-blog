---
audio: false
generated: true
image: false
lang: en
layout: post
title: Git Pull on a Shallow Clone
translated: false
type: note
---

Question: If I clone a repository with `--depth=10`, can I later run `git pull` to get more commits?

Answer:

Yes, you can run `git pull` later on a shallow clone. Here's what you need to know:

## Shallow Clone Basics

`--depth=10` creates a **shallow clone** — it only downloads the latest 10 commits instead of the full history. This makes the initial clone faster and smaller.

## Running `git pull` Later

```bash
git pull
```

This works fine and will **fetch new commits** pushed after your clone. It keeps the repo shallow — you'll still only have a limited history window, but it slides forward as new commits arrive.

## Deepening History (Optional)

If you later want **more history**, you can deepen or fully unshallow:

```bash
# Deepen by 10 more commits
git fetch --deepen=10

# Unshallow completely (fetch full history)
git fetch --unshallow

# Or equivalently
git pull --unshallow
```

## Key Behaviors Summary

| Command | Effect |
|---|---|
| `git pull` | Gets new commits, stays shallow |
| `git fetch --deepen=N` | Adds N more commits to history |
| `git fetch --unshallow` | Fetches complete history |
| `git log` | Shows only the shallow history |

## One Caveat

If you try to do operations that need full history (like `git merge-base` across deep branches, or certain `git log` range queries), you may hit errors like:

```
fatal: --unshallow on a complete repository does not make sense
```

or

```
error: Server does not allow request for unadvertised object
```

In those cases, just run `git fetch --unshallow` first.

**Short answer: `git pull` works perfectly fine after a shallow clone — no issues.**
