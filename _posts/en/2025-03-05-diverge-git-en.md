---
audio: false
generated: true
lang: en
layout: post
title: Diverged Git Branches
translated: false
type: note
---

When your local `main` branch and the remote `origin/main` branch have diverged in Git—with 74 and 70 different commits respectively—it means they share a common ancestor but have since developed unique commits. Your goal is to make your local `main` branch match `origin/main` by resetting your local branch to the common ancestor (the "parent of both") and then using `git pull` to bring in the remote changes, effectively discarding your local diverging commits in favor of the remote ones. Below are the steps to achieve this.

### Steps to Fix the Divergence

1. **Fetch the Latest Remote Changes**
   Start by ensuring your local repository has the latest information from the remote. This updates your reference to `origin/main` without altering your local `main` branch yet.

   ```bash
   git fetch origin
   ```

2. **Find the Common Ancestor Commit**
   Use `git merge-base` to identify the common ancestor commit between your local `main` and `origin/main`. This is the point where the branches diverged.

   ```bash
   ancestor=$(git merge-base main origin/main)
   ```

   This command stores the commit hash of the common ancestor in the variable `ancestor`.

3. **Reset Local `main` to the Common Ancestor**
   Reset your local `main` branch to the common ancestor commit. The `--hard` option ensures that both the branch pointer and your working directory are updated, discarding all local commits and changes made after this point.

   ```bash
   git reset --hard $ancestor
   ```

   **Caution**: This step will discard all uncommitted changes in your working directory and staging area, as well as the 74 commits unique to your local `main`. If you need to preserve these, consider creating a backup branch first (see "Optional Backup" below).

4. **Pull the Remote Changes**
   Now, pull the changes from `origin/main`. Since your local `main` is now at the common ancestor, and `origin/main` is ahead by 70 commits, this will fast-forward your local `main` to match `origin/main`.

   ```bash
   git pull origin main
   ```

   After this, your local `main` branch will be identical to `origin/main`, with all local diverging commits discarded.

### Complete Command Sequence

Here’s the full sequence of commands to execute:

```bash
git fetch origin
ancestor=$(git merge-base main origin/main)
git reset --hard $ancestor
git pull origin main
```

### What Happens?
- **After Step 1**: Your local repository knows the latest state of `origin/main`.
- **After Step 2**: You’ve identified the common ancestor commit (e.g., a hash like `abc123`).
- **After Step 3**: Your local `main` is reset to `abc123`, losing the 74 unique local commits.
- **After Step 4**: `git pull` fast-forwards `main` to `origin/main`, bringing in the 70 commits from the remote branch.

The result is that your local `main` matches `origin/main` exactly, fulfilling your goal of using the remote branch.

### Optional Backup
If you’re unsure about discarding your local commits and want to preserve them for later, create a backup branch before resetting:

```bash
git branch backup-main
```

Run this before the `git reset` command. Your 74 local commits will remain on `backup-main`, and you can revisit them later if needed.

### Important Notes
- **Uncommitted Changes**: If you have uncommitted changes (in your working directory or staging area) that you want to keep, stash them before resetting:
  ```bash
  git stash
  ```
  After completing the process, you can retrieve them with `git stash pop`.
- **Why This Works**: Resetting to the common ancestor and pulling ensures a clean fast-forward to `origin/main`, avoiding merge conflicts that might arise from directly pulling with diverged branches.

By following these steps, you’ll successfully reset your local `main` to match `origin/main` as desired.
