---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-code-fast-1
title: Squashing Git Commits by Author
translated: false
type: note
---

### Understanding the Goal
Git doesn't have a built-in "squash by author" command, but you can achieve this using interactive rebase to manually group and squash commits. The idea is to take the last 10 commits (assuming they involve 3 distinct authors) and merge each author's commits into a single commit per author, resulting in 3 commits total.

This assumes:
- You're on the branch with those commits (e.g., main or feature branch).
- The commits are linear (no merges).
- You know the authors in advance.

If commits are non-linear or complex, this may require careful handling to avoid conflicts.

### Steps to Squash Commits by Author
1. **Check the Latest 10 Commits**
   Run `git log --oneline -10` to see the last 10 commits, including their hashes, authors, and messages. Identify the authors (e.g., via `git log --format="%an" -10 | sort | uniq` to list unique authors).

2. **Start an Interactive Rebase**
   Identify the commit before the 10th one. If your latest commit is at HEAD, and there are 10 commits, the base is `HEAD~10`. Run:
   ```
   git rebase -i HEAD~10
   ```
   This opens an editor (vim by default) with a list of the last 10 commits. It looks like this:
   ```
   pick abc123 First commit by Author A
   pick def456 Second commit by Author A
   pick ghi789 Commit by Author B
   pick jkl012 Commit by Author C
   ... (more commits)
   ```
   - Each line starts with `pick`.

3. **Mark Commits to Squash by Author**
   For each author, change `pick` to `s` (squash) on all their commits except the first one you want to keep for that author. Decide on:
   - One "keep" commit per author (pick the earliest or most relevant one as the base).
   - Change the rest by that author to `s` to squash them into it.
   Example (for 3 authors):
   ```
   pick abc123 First commit by Author A (keep this one)
   s    def456 Second commit by Author A (squash into above)
   pick ghi789 Commit by Author B (keep this one)
   pick jkl012 First commit by Author C (keep this one)
   s    mno345 Second commit by Author C (squash into above)
   ```
   Save and exit the editor. This starts the rebase.

4. **Edit Commit Messages During Rebase**
   For each squash operation, Git will pause and let you edit the commit message (combining the squashed ones). Update it to something like "Squashed commits by Author A: description". Save and continue.
   If there are more squashes, repeat for each author. Run `git rebase --continue` after each edit.
   If conflicts arise (rare in simple squash), resolve them with `git add <file>` then `git rebase --continue`.

5. **Verify and Push**
   After rebase completes, check the log: `git log --oneline -10`. You should see 3 commits, each from one author.
   Force-push if pushing to a shared branch (destructive rebase): `git push --force-with-lease origin branch-name`.
   **Warning:** Only force-push if you're sure the old commits aren't needed elsewhere, as this rewrites history.

### Tips and Caveats
- If authors have many commits, group them efficiently in the rebase list (all of Author A's together, etc.).
- For automation, tools like `git-interactive-rebase-tool` or scripts can help, but manual rebase is straightforward.
- If you need to filter by exact author, use `git log --author="Author Name"` beforehand to confirm.
- Test on a backup branch first to avoid data loss.

For more on rebase: `git help rebase`. If this doesn't match your exact scenario, provide more details about the commit structure.
