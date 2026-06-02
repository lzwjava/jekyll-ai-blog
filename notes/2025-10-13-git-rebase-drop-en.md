---
audio: false
generated: true
image: false
lang: en
layout: post
model: openai/gpt-5
title: Git Rebase Drop Removes Commits
translated: false
type: note
---

Yes — exactly.

When you use **`drop`** during an interactive `git rebase -i`, it means **“remove this commit entirely from the history.”**

Here’s what happens:

* Git will **skip applying** that commit while replaying the others.
* The resulting branch will look as if that commit **never existed** — its changes and its commit message are both gone.
* The following commits will still be applied (if they don’t depend on the removed changes).

Example:

```bash
git rebase -i HEAD~4
```

You might see something like:

```
pick a1b2c3d Fix typo
pick b2c3d4e Add README
pick c3d4e5f Implement login
pick d4e5f6g Add debug log
```

If you change the last line to:

```
drop d4e5f6g Add debug log
```

then after saving and closing the editor, Git will rebase the branch and **exclude that commit**.

So yes — “drop” = **delete the commit from the branch history.**

Would you like me to explain how that differs from `revert` (which *undoes* a commit but keeps a record of it)?
