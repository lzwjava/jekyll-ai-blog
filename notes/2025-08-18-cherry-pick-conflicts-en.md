---
audio: false
generated: true
image: false
lang: en
layout: post
title: Cherry Pick Conflicts and Solutions
translated: false
type: note
---

Git **cherry-pick** is a command that lets you take a commit from one branch and apply it onto another branch, without merging the whole branch history.

---

### How it works

* When you run `git cherry-pick <commit-hash>`, Git:

  1. Locates the changes introduced by that commit (a diff against its parent).
  2. Reapplies those changes onto your current branch, creating a new commit with a new hash.
  3. This means the commit content is reused, but it doesn’t keep the original commit’s ancestry.

It’s like saying:
*"Take just this one commit’s patch and stick it onto where I am right now."*

---

### Why conflicts happen

Conflicts arise because cherry-pick applies changes **out of their original context**. A few common reasons:

1. **Code drift**
   If the target branch has changed in the same areas of code since the original commit, Git can’t cleanly apply the patch. For example:

   * Original commit added a function in `fileA`.
   * In the target branch, someone renamed or removed that function.
     → Conflict when cherry-picking.

2. **Dependent commits missing**
   Sometimes a commit depends on earlier commits (e.g., refactorings, variable renames). If you cherry-pick it without those, the context is different, and conflicts appear.

3. **Overlapping changes**
   If both branches touched the same lines of code (even for different reasons), Git can’t decide automatically and stops for manual resolution.

---

### Example scenario

* `feature-branch` has commits A → B → C.
* You want commit B in `main`.
* You run `git checkout main && git cherry-pick B`.
* If `main` already touched the same file/lines as B, Git raises a conflict. You must open the file, resolve differences, `git add`, and then `git cherry-pick --continue`.

---

👉 In short: **Cherry-pick replays a patch in a new context. Conflicts happen when that context has diverged too much from the original.**

Would you like me to also walk you through **best practices to reduce cherry-pick conflicts** (like sequencing commits, using `-x`, or rebasing first)?
