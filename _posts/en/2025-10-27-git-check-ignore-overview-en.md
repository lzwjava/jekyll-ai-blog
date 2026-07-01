---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Git Check-Ignore Command Overview
translated: false
type: note
---

### What is `git check-ignore`?

The `git check-ignore` command is a Git tool used to determine whether a specific file or path is ignored by Git's ignore mechanisms, such as `.gitignore` files, `.git/info/exclude`, or global ignore files (via `core.excludesFile`). It's particularly useful for debugging why a file isn't being tracked or added to the repository.

If the path is ignored, the command outputs the path (and optionally the matching pattern). If it's not ignored, there's no output (exit code 0). This makes it script-friendly for automation.

### Basic Usage

Run it with one or more paths to check:

```
git check-ignore <pathname>...
```

- **Example**: Check if a single file is ignored:

  ```
  git check-ignore path/to/myfile.txt
  ```

  - Output: If ignored, prints `path/to/myfile.txt`. If not, prints nothing.

- **Example**: Check multiple files:

  ```
  git check-ignore file1.txt file2.txt dir/file3.txt
  ```

  - Outputs only the ignored paths, one per line.

### Key Options

| Option | Description | Example |
| -------- | ------------- | --------- |
| `-v`, `--verbose` | Show the ignore pattern that matched (e.g., the line from `.gitignore`). | `git check-ignore -v path/to/myfile.txt`<br>Output: `path/to/myfile.txt: .gitignore:1:*.txt` (path + file:line:pattern) |
| `-q`, `--quiet` | Suppress output, but still use exit code (0 if not ignored, 1 if ignored). Useful in scripts. | `git check-ignore -q path/to/myfile.txt`<br>(No output; check `$?` for exit code) |
| `--stdin` | Read paths from standard input instead of command line. | `echo "file1.txt\nfile2.txt" \| git check-ignore --stdin` |
| `--non-matching` | Invert the output: Show paths that are *not* ignored. | `git check-ignore --non-matching -v file1.txt file2.txt` |

### Common Use Cases

1. **Debugging `.gitignore` Rules**:
   - If `git status` doesn't show a file you expect, run `git check-ignore -v <file>` to see exactly which rule is ignoring it.
   - Example output: `src/logs/app.log: .gitignore:5:logs/*` (indicating line 5 in `.gitignore` matches).

2. **In Scripts**:
   - Check if a file should be added:

     ```
     if git check-ignore -q myfile.txt; then
         echo "File is ignored, skipping..."
     else
         git add myfile.txt
     fi
     ```

3. **Batch Checking**:
   - List all ignored files in a directory:

     ```
     find . -type f -print0 | xargs -0 git check-ignore
     ```

### Tips

- It respects the Git ignore stack: local `.gitignore`, global excludes, etc.
- Works on untracked files or those already in the repo (but checks against ignore rules).
- For more details, see the official docs.

[Git check-ignore Documentation](https://git-scm.com/docs/git-check-ignore)
[Stack Overflow: Git command to show which specific files are ignored](https://stackoverflow.com/questions/466764/git-command-to-show-which-specific-files-are-ignored-by-gitignore)
[Using git check-ignore to debug your .gitignore](https://alexwlchan.net/til/2020/using-git-check-ignore-to-debug-your-gitignore/)
