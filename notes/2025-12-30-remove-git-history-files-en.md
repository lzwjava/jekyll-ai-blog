---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Removing files from Git history
translated: false
type: note
---

**Question:** How to use git filter-repo to remove a file from Git history?

**Answer:**

`git filter-repo` is the recommended modern tool (faster and safer than the deprecated `git filter-branch` or BFG) for rewriting Git history, including permanently removing a specific file from all commits across the repository.

### Prerequisites

- Install `git-filter-repo` if not already available (it's not included in Git by default).
  Installation instructions: <https://github.com/newren/git-filter-repo#installation>
- **Backup your repository** first, as history rewriting is destructive and changes commit hashes.
- Preferably work on a **fresh clone** of the repository to avoid safety checks:

  ```
  git clone <repository-url> myrepo-clean
  cd myrepo-clean
  ```

### Basic Command to Remove a Single File

To completely remove a file (e.g., `path/to/secret.txt`) from the entire history:

```
git filter-repo --path path/to/secret.txt --invert-paths
```

- `--path <file>`: Specifies the file to target (path relative to repository root).
- `--invert-paths`: Keeps all files *except* the specified one(s). Without this, it would keep only the specified file and remove everything else.

You can specify multiple files:

```
git filter-repo --path file1.txt --path file2.config --invert-paths
```

### For Folders/Directories

To remove an entire directory (e.g., `old_folder/`):

```
git filter-repo --path old_folder/ --invert-paths
```

For more complex patterns (e.g., all files matching a glob):

```
git filter-repo --path-glob '*.secret' --invert-paths
```

Use `--path-glob` for globs, `--path-regex` for regex, or `--use-base-name` if matching by filename only (ignores path).

### Applying to All Branches and Tags

By default, `git filter-repo` affects all refs. To be explicit:

```
git filter-repo --path path/to/secret.txt --invert-paths --force
```

(The `--force` flag overrides the "fresh clone" safety check if needed.)

### After Rewriting History

1. Verify the file is gone:

   ```
   git log --all -- path/to/secret.txt
   ```

   (Should show no results.)

2. Clean up:
   The tool usually repacks automatically, but you can run:

   ```
   git reflog expire --expire=now --all
   git gc --prune=now
   ```

3. Push changes to remote (requires force push since history is rewritten):

   ```
   git push origin --force --all
   git push origin --force --tags
   ```

### Important Warnings

- **History rewrite changes all commit IDs** downstream of affected commits. All collaborators must re-clone the repository or manually recover (see `git filter-repo` docs for instructions).
- Coordinate with your team: Close open pull requests, notify others.
- If the file contained sensitive data and was already pushed, old commits may still be accessible temporarily on remotes (e.g., GitHub caches them briefly).
- For sensitive data removal, follow GitHub's full guide if using GitHub.

This process permanently erases the file from history, reducing repository size if it was large.

**References:**

- [GitHub - newren/git-filter-repo](https://github.com/newren/git-filter-repo)
- [GitHub Docs: Removing sensitive data from a repository](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)
