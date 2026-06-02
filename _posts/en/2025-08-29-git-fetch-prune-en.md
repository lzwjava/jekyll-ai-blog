---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-code-fast-1
title: Git Fetch and Prune Overview
translated: false
type: note
---

### What is `git fetch`?
`git fetch` downloads the latest changes (commits, branches, tags) from a remote repository without merging them into your current branch. It updates your local remote-tracking branches (e.g., `origin/main`) to match the remote state. This keeps your local repo in sync but doesn't alter your working files or local branches.

### What is the `--prune` Option?
The `--prune` flag tells Git to remove remote-tracking branches that no longer exist on the remote. For example, if someone deletes a branch on GitHub, your local copy (e.g., `origin/old-branch`) persists unless pruned.

### How Does `git fetch --prune` Work?
- **Execution**: Run it as `git fetch --prune` (or `git fetch -p` for short). It combines fetch and prune in one command.
- **Steps**:
  1. Git connects to the remote and fetches updates, updating remote-tracking branches to reflect new commits, added branches, or deleted branches.
  2. It scans for stale remote-tracking branches (those without a counterpart on the remote) and deletes them locally.
- **Result**: Your local repo stays current and clean. No merging occurs—it's a read-only sync.

### Practical Example
Suppose you have:
- Local branch: `main`, tracking `origin/main`.
- A stale local remote-tracking branch: `origin/deleted-feature`.

Running `git fetch --prune` for `origin`:
- Fetches any new commits.
- Removes `origin/deleted-feature` (since it's gone on the remote).
- Doesn't touch your local branches.

### What It Means
It means "fetch the latest remote data and clean up outdated references" in your local repository. Use it regularly to avoid confusion from old branch refs. Equivalent to `git fetch` followed by `git remote prune origin`, but conveniently combined. For safety, it only affects remote-tracking branches, not your own work.
