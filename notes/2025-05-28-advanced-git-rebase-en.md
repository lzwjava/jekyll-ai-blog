---
audio: false
generated: true
lang: en
layout: post
title: 'Advanced Git: Rebase, Merge, Conflict Resolution, Squash'
translated: false
type: note
---

This guide covers advanced usage of `git rebase` and `git merge`, resolving conflicts, using `ours` and `theirs` strategies, and squashing commits. I'll provide concise explanations and practical examples for each topic, focusing on advanced workflows that assume familiarity with basic Git commands.

## 1. Git Merge: Advanced Usage
`git merge` combines multiple sequences of development into a single unified history. Advanced usage includes handling complex merges, using merge strategies, and managing merge commits.

### Key Merge Strategies
- **Recursive (default)**: Handles multiple common ancestors and is suitable for most merges.
  - Example: `git merge --strategy=recursive branch-name`
- **Ours**: Keeps the current branch's changes, discarding changes from the merged branch.
  - Example: `git merge --strategy=ours feature-branch`
- **Theirs**: Not a true strategy but can be emulated (see below for conflict resolution).
- **Octopus**: Merges multiple branches at once (used for >2 branches).
  - Example: `git merge branch1 branch2 branch3`

### Advanced Merge Options
- `--no-ff`: Forces a merge commit even if a fast-forward is possible, preserving branch history.
  - Example: `git merge --no-ff feature-branch`
- `--squash`: Combines all commits from the merged branch into a single commit on the current branch.
  - Example: `git merge --squash feature-branch && git commit`
- `--allow-unrelated-histories`: Merges branches with no common history.
  - Example: `git merge --allow-unrelated-histories external-repo-branch`

### Example: Merging with No Fast-Forward
```bash
git checkout main
git merge --no-ff feature-branch
# Creates a merge commit, preserving feature-branch history
```

## 2. Git Rebase: Advanced Usage
`git rebase` rewrites history by moving or modifying commits to create a linear history. It’s powerful for cleaning up branches but alters history, so use with caution on shared branches.

### Types of Rebase
- **Standard Rebase**: Replays commits from the current branch onto the base branch.
  - Example: `git rebase main` (while on `feature-branch`)
- **Interactive Rebase**: Allows editing, squashing, or reordering commits.
  - Example: `git rebase -i main`

### Interactive Rebase Commands
Run `git rebase -i <base>` (e.g., `git rebase -i HEAD~3` for the last 3 commits). This opens an editor with commands like:
- `pick`: Keep the commit as is.
- `reword`: Edit the commit message.
- `edit`: Pause rebase to amend the commit.
- `squash`: Combine with the previous commit.
- `fixup`: Like squash, but discards the commit message.
- `drop`: Remove the commit.

### Example: Interactive Rebase
To squash the last 3 commits:
```bash
git rebase -i HEAD~3
# In the editor, change "pick" to "squash" or "fixup" for the commits to combine
# Save and exit to complete
```

### Rebase onto a Different Base
To move a branch to a new base (e.g., moving `feature-branch` from `old-base` to `main`):
```bash
git rebase --onto main old-base feature-branch
```

### Rebase with Merge Commits
By default, rebase flattens merge commits. To preserve them:
```bash
git rebase -i --preserve-merges main
```

### Aborting a Rebase
If something goes wrong:
```bash
git rebase --abort
```

## 3. Resolving Merge/Rebase Conflicts
Conflicts occur when Git can’t automatically reconcile changes. Both `merge` and `rebase` can result in conflicts, resolved similarly.

### Steps to Resolve Conflicts
1. **Identify Conflicts**: Git pauses and lists conflicted files.
   - For merge: `git status` shows files with conflicts.
   - For rebase: Conflicts are resolved commit-by-commit during `git rebase -i`.
2. **Edit Conflicted Files**: Open files and look for conflict markers:
   ```text
   <<<<<<< HEAD
   Your changes
   =======
   Incoming changes
   >>>>>>> branch-name
   ```
   Manually edit to keep desired changes, then remove markers.
3. **Mark as Resolved**:
   - For merge: `git add <file>`
   - For rebase: `git add <file>`, then `git rebase --continue`
4. **Complete the Process**:
   - Merge: `git commit` (Git may auto-generate a commit message).
   - Rebase: `git rebase --continue` until all commits are applied.

### Example: Resolving a Merge Conflict
```bash
git checkout main
git merge feature-branch
# Conflict occurs
git status  # Lists conflicted files
# Edit files to resolve conflicts
git add resolved-file.txt
git commit  # Finalize merge
```

### Example: Resolving a Rebase Conflict
```bash
git checkout feature-branch
git rebase main
# Conflict occurs
# Edit conflicted files
git add resolved-file.txt
git rebase --continue
# Repeat until rebase completes
```

## 4. Using Ours and Theirs in Conflict Resolution
During conflicts, you may want to favor one side’s changes (`ours` or `theirs`). The meaning of `ours` and `theirs` depends on the operation.

### Merge: Ours vs. Theirs
- `ours`: Changes from the current branch (e.g., `main`).
- `theirs`: Changes from the branch being merged (e.g., `feature-branch`).
- Use the `--strategy-option` (`-X`) flag:
  - Keep `ours`: `git merge -X ours feature-branch`
  - Keep `theirs`: `git merge -X theirs feature-branch`

### Rebase: Ours vs. Theirs
- `ours`: Changes from the base branch (e.g., `main`).
- `theirs`: Changes from the branch being rebased (e.g., `feature-branch`).
- Use during rebase conflict resolution:
  ```bash
  git checkout --ours file.txt  # Keep base branch’s version
  git checkout --theirs file.txt  # Keep rebased branch’s version
  git add file.txt
  git rebase --continue
  ```

### Example: Merge with Theirs
To merge `feature-branch` into `main` and favor `feature-branch` changes:
```bash
git checkout main
git merge -X theirs feature-branch
```

### Example: Rebase with Ours
While rebasing `feature-branch` onto `main`, resolve a conflict by keeping `main`’s version:
```bash
git checkout feature-branch
git rebase main
# Conflict occurs
git checkout --ours file.txt
git add file.txt
git rebase --continue
```

## 5. Squashing Commits
Squashing combines multiple commits into one, creating a cleaner history. This is typically done with interactive rebase.

### Steps to Squash Commits
1. Start an interactive rebase for the desired commits:
   ```bash
   git rebase -i HEAD~n  # n = number of commits to squash
   ```
2. In the editor, change `pick` to `squash` (or `fixup`) for commits to combine into the previous commit.
3. Save and exit. Git may prompt to edit the commit message for the combined commit.
4. Push the updated history (force push if already shared):
   ```bash
   git push --force-with-lease
   ```

### Example: Squashing 3 Commits
```bash
git rebase -i HEAD~3
# Editor shows:
# pick abc123 Commit 1
# pick def456 Commit 2
# pick ghi789 Commit 3
# Change to:
# pick abc123 Commit 1
# squash def456 Commit 2
# squash ghi789 Commit 3
# Save and exit
# Edit combined commit message if prompted
git push --force-with-lease
```

### Squashing During Merge
To squash all commits from a branch during a merge:
```bash
git checkout main
git merge --squash feature-branch
git commit  # Create a single commit
```

## Best Practices and Tips
- **Backup Before Rebase**: Rebasing rewrites history. Create a backup branch:
  ```bash
  git branch backup-branch
  ```
- **Avoid Rebasing Shared Branches**: Rewriting history on public branches can cause issues for collaborators. Use `merge` instead.
- **Use `--force-with-lease` for Safety**: When pushing rewritten history, this prevents overwriting others’ changes.
- **Test After Resolving Conflicts**: Ensure your project builds and tests pass after resolving conflicts.
- **Use Tools for Conflicts**: GUI tools like VS Code, SourceTree, or `git mergetool` can simplify conflict resolution.
- **Communicate with Team**: If working in a team, coordinate rebases to avoid conflicts.

## Common Pitfalls
- **Losing Work in Rebase**: Always back up or use `git reflog` to recover lost commits.
- **Misusing Ours/Theirs**: Double-check which branch is `ours` vs. `theirs` in merge vs. rebase contexts.
- **Force Pushing Without Coordination**: Force-pushing shared branches can disrupt teammates. Use `--force-with-lease` and communicate.

## Recovering from Mistakes
- **View History**: Use `git reflog` to see previous states and recover lost commits:
  ```bash
  git reflog
  git checkout <commit-hash>
  ```
- **Reset to Pre-Merge State**:
  ```bash
  git reset --hard HEAD^  # Undo last merge commit
  ```
- **Abort Merge**: If a merge goes wrong:
  ```bash
  git merge --abort
  ```

This guide provides a solid foundation for advanced Git workflows. For specific scenarios or errors, let me know, and I can dig deeper or search for real-time solutions!
