---
audio: false
generated: true
lang: en
layout: post
title: Using Git Pull and Push with Shallow Clones
translated: false
type: note
---

Yes, you can still use `git pull` or `git push` after cloning a repository with a limited history using `--depth=20`. However, there are some important considerations to keep in mind:

### 1. **What `--depth=20` Does**

- The `--depth=20` option creates a *shallow clone*, fetching only the most recent 20 commits (or the specified number) from the default branch (or the specified branch if you use `--branch`).
- This reduces the amount of history downloaded, making the clone faster and smaller in size, but the repository will not contain the full commit history.

### 2. **Using `git pull` with a Shallow Clone**

- **Yes, you can use `git pull`** in a shallow clone to fetch and merge new commits from the remote repository.
- By default, `git pull` will fetch new commits and update the shallow history, keeping it consistent with the remote branch.
- If new commits are added to the remote branch, `git pull` will fetch them and extend the history in your local repository, still respecting the shallow nature of the clone.

   **Note**: If the branch's history changes in a way that affects commits older than your shallow history (e.g., a force push or rebase on the remote), you may encounter issues. In such cases, you might need to deepen the history (using `git fetch --deepen=<n>` or `git fetch --unshallow` to fetch the full history) to resolve conflicts or continue working.

### 3. **Using `git push` with a Shallow Clone**

- **Yes, you can use `git push`** to push your local commits to the remote repository.
- A shallow clone does not restrict your ability to create new commits and push them to the remote repository, as long as the remote accepts your changes.
- However, if the remote repository requires operations that depend on the full history (e.g., a merge or rebase involving older commits), you may need to fetch more history to complete the push successfully.

### 4. **Limitations of Shallow Clones**

- **Limited History**: Some Git operations, like `git log`, `git blame`, or `git rebase`, may be limited because older commits are not available locally.
- **Merging and Rebasing**: If you need to merge or rebase with commits outside your shallow history, you may need to fetch more history using `git fetch --deepen=<n>` or `git fetch --unshallow`.
- **Force Pushes**: If the remote branch is rewritten (e.g., with `git push --force`), your shallow clone might not have enough context to handle the changes, requiring you to deepen the history or re-clone.

### 5. **How to Deepen a Shallow Clone (If Needed)**

   If you encounter issues with `git pull` or `git push` due to limited history, you can fetch additional history:

- **Deepen by a specific number of commits**:

     ```bash
     git fetch --deepen=20
     ```

     This fetches 20 more commits of history.
- **Fetch the full history**:

     ```bash
     git fetch --unshallow
     ```

     This converts your shallow clone into a full clone with the entire history.

### 6. **Practical Advice**

- A shallow clone with `--depth=20` is usually sufficient for most workflows, especially if you're only working on recent changes or contributing small updates.
- If you anticipate needing the full history (e.g., for complex merges, rebases, or debugging), consider cloning the full repository without the `--depth` option or deepening the history later as needed.
- Always ensure you have write access to the remote repository (e.g., `git@github.com:cisco/ChezScheme.git`) before attempting to push.

### Example Workflow

```bash
# Clone with limited history
git clone git@github.com:cisco/ChezScheme.git --depth=20
cd ChezScheme

# Make changes and commit
git commit -m "My changes"

# Pull latest changes
git pull origin main

# Push your changes
git push origin main
```

If you run into issues due to the shallow clone, deepen the history as described above.

### Summary

Yes, you can use `git pull` and `git push` with a shallow clone created using `--depth=20`. However, you may need to fetch additional history for certain operations if the shallow history is insufficient. Use `git fetch --deepen` or `git fetch --unshallow` to address any limitations.
