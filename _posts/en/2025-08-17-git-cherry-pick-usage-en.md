---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-code-fast-1
title: Git Cherry-Pick Overview and Usage
translated: false
type: note
---

### What is Git Cherry-Pick?

Git cherry-pick is a command that allows you to apply the changes from a specific commit (or set of commits) onto your current branch, creating a new commit with those changes. It's useful when you want to pick a particular fix or feature from one branch without merging the entire branch. Unlike a merge, which integrates all history, cherry-pick selectively copies changes.

### How Git Cherry-Pick Works Internally

1. **Select the Commit**: You specify a commit hash (e.g., via `git log` to find it) that contains the changes you want.

2. **Apply Changes**: Git takes the diff (the actual code changes) from that commit and tries to apply it to your current branch's working directory, using Git's three-way merge logic where possible.

3. **Create New Commit**: If successful, a new commit is made on your branch with:
   - The same changes as the original commit.
   - A new commit hash (because it's a fresh commit).
   - A commit message that references the original (e.g., via -x flag to append "cherry picked from commit <hash>").

   If there are merge conflicts (e.g., the target branch has incompatible changes), Git pauses and lets you resolve them manually before committing.

The process doesn't alter the original commit's history—it just copies the changes. This makes cherry-pick great for backporting bug fixes or applying features selectively.

### Basic Usage Steps

1. Ensure you're on the target branch (switch with `git checkout <branch>`).
2. Find the commit hash you want (e.g., `git log --oneline`).
3. Run: `git cherry-pick <commit-hash>`
   - For multiple: `git cherry-pick <hash1> <hash2>`
   - With options like `-n` (no commit, for staging) or `-x` (reference original).

4. If conflicts arise, edit the files, stage with `git add`, then `git cherry-pick --continue`.
5. If you abort midway: `git cherry-pick --abort`.

### Example Scenario

Suppose you have a feature branch with commits A -> B -> C, and you want to cherry-pick commit B onto the main branch.

- On main: `git checkout main`
- `git cherry-pick B` (replacing B with the actual hash)

This adds the changes from B as a new commit D on main, without pulling in A or C. The original B remains in the feature branch.

### Caveats and Tips

- Avoid cherry-picking merges (commits with multiple parents), as it can lead to issues—use `git cherry-pick -m 1 <merge-commit>` to specify a parent.
- It doesn't preserve the commit's metadata like author date, but `git cherry-pick --edit` lets you modify the message.
- For sequenced changes, cherry-pick multiple commits in order to avoid missing dependencies.
- Always test after cherry-picking, as it might introduce bugs if contexts differ.

For more details, the official Git docs provide comprehensive guidance: <https://git-scm.com/docs/git-cherry-pick>. If you run into specific issues, share your Git log output!
