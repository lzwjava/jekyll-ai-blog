---
audio: false
generated: true
image: false
lang: en
layout: post
title: Git Rebase Squash Order Explained
translated: false
type: note
---

When you run `git rebase -i` (interactive rebase) to squash commits, Git follows a very specific order and logic:

---

### 1. Default Order

When you start an interactive rebase (e.g., `git rebase -i HEAD~5`), Git opens your editor with the **commits listed from oldest to newest** (top = oldest, bottom = newest).
The order matters: this is the sequence Git will try to replay onto the new base.

---

### 2. Pick vs. Squash

* **pick** → keep the commit as-is.
* **squash (or s)** → combine this commit with the **previous commit marked as `pick`**.
* **fixup (or f)** → same as squash, but discards the commit message (only keeps the first commit’s message).

So if you write:

```
pick  a1b2c3  Initial feature
squash d4e5f6  Minor fix
squash g7h8i9  Small cleanup
pick  j1k2l3  Another feature
```

Git will merge `d4e5f6` and `g7h8i9` into `a1b2c3`, producing a single commit.

---

### 3. Rearranging Commits

You can **reorder commits directly in the rebase editor** by moving lines up or down.
For example:

```
pick  a1b2c3  Initial feature
pick  j1k2l3  Another feature
squash d4e5f6  Minor fix
squash g7h8i9  Small cleanup
```

Here, Git will first apply `a1b2c3`, then `j1k2l3`.
The `squash` commits (`d4e5f6` and `g7h8i9`) will now squash into **`j1k2l3`**, since squash always merges into the most recent preceding `pick`.

---

### 4. Editing Messages

After squashing, Git pauses and lets you **edit the commit message** for the squashed commit. You can:

* Keep all messages.
* Combine them manually.
* Keep only the first one.

---

### 5. Common Pitfalls

* If you put `squash` as the very first commit (no `pick` before it), Git will throw an error—it needs a base commit to squash into.
* If commits conflict after reordering, you’ll need to resolve conflicts manually during rebase.
* Reordering can change history significantly; only do it on branches you haven’t pushed/shared yet, unless you’re sure you want to rewrite history.

---

✅ In short:

* Commits are listed **oldest → newest**.
* `pick` keeps, `squash` merges into the **nearest earlier `pick`**.
* You can rearrange commits manually in the editor; squash always attaches downward commits into the previous picked one.

---

Do you want me to illustrate this with a **before/after commit history example** (showing `git log --oneline` before and after squashing)? That usually makes the order clearer.
