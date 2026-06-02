---
audio: false
generated: true
image: false
lang: en
layout: post
title: Clean Remote Branches With Prune
translated: false
type: note
---

`git fetch --prune` is a way to keep your local references to remote branches clean and up-to-date.

### What it does

* **`git fetch`** normally updates your local copy of the remote’s branches (like `origin/main`, `origin/feature-x`) without touching your own local branches.
* Over time, the remote repository might delete or rename some branches. Without cleanup, your local repo will still show those old remote-tracking branches (e.g., `origin/feature-old`).
* **Adding `--prune`** tells Git: *“If the remote no longer has a branch, delete my corresponding remote-tracking reference.”*

So, after running `git fetch --prune`, your local list of remote branches matches exactly what the remote currently has.

### Example

1. Remote has branches: `main`, `feature-a`.
2. You run `git fetch` → you now have `origin/main`, `origin/feature-a`.
3. Someone deletes `feature-a` on the remote.
4. If you run `git fetch`, you’ll still see `origin/feature-a` locally (stale reference).
5. If you run `git fetch --prune`, Git will notice `feature-a` is gone and remove `origin/feature-a` from your local repo.

### Why it’s useful

* Keeps `git branch -r` (remote branches list) clean.
* Avoids confusion when switching or merging into branches that no longer exist upstream.
* Often used with aliases (e.g., `git fetch -p`) or set as default with:

  ```bash
  git config fetch.prune true
  ```

That way, every `git fetch` automatically prunes stale branches.

---

Do you want me to also explain how **pruning interacts with tags** (since `git fetch --prune` only handles branches by default, but tags behave differently)?
