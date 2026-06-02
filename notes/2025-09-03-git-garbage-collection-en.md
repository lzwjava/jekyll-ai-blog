---
audio: false
generated: true
image: false
lang: en
layout: post
title: Git Garbage Collection Explained
translated: false
type: note
---

`git gc` stands for **Git garbage collection**. It’s a housekeeping command that cleans up and optimizes your local repository.

### What it does

* **Compresses file history**: Git stores objects (commits, trees, blobs) in a database. Over time, many loose objects accumulate. `git gc` packs them together into a compact binary file, saving disk space.
* **Removes unreachable objects**: If you deleted branches or rebased, some commits may no longer be reachable from any reference. Git keeps them for safety, but `git gc` eventually cleans them up.
* **Optimizes references**: It rewrites and packs refs like tags and branches to make lookups faster.
* **Prunes reflogs**: Old reflog entries (records of HEAD changes) beyond the expiry period get removed.

### Why it sometimes happens automatically

* Git runs **automatic background `gc`** when the number of loose objects or pack files crosses a threshold. For example, if you’ve made a lot of commits, rebases, or merges, Git may trigger it.
* Many Git commands (like `git fetch`, `git merge`, or `git rebase`) check whether a `gc` is advisable and run it automatically if needed.
* This helps keep your repo performant without you having to think about it.

### When to run it manually

* If your repository feels **slow** or **bloated** (e.g., large `.git` folder).
* After doing a **big cleanup** (like deleting branches or removing large files from history).
* If you want to force immediate cleanup:

  ```bash
  git gc --prune=now --aggressive
  ```

  *(be careful: `--aggressive` can take a long time, especially on large repos)*

---

Do you want me to also explain how to **check when Git last ran `gc` automatically** and what thresholds trigger it?
