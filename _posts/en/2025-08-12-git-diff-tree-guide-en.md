---
audio: false
generated: true
image: false
lang: en
layout: post
title: Git Diff-Tree Guide
translated: false
type: note
---

Here’s a practical, end-to-end guide to `git diff-tree`—what it is, when to use it, and the options you’ll actually reach for in real work. I’ll avoid big tables and stick to focused explanations with copy-pasteable examples.

# What `git diff-tree` actually does

* It compares **tree objects**. In everyday use, that usually means: “show me what changed in a **commit** compared to its parent(s).”
* It’s **plumbing** (script-friendly), unlike `git show`/`git log` which are porcelain (human-oriented).
* It never looks at your working directory; it only compares trees stored in the repo (commits, tags pointing to commits, or raw tree IDs).

# Basic forms you’ll use

1. Diff a commit against its parent

```bash
git diff-tree -p <commit>
```

If `<commit>` has one parent, you see a normal patch. If it’s a merge commit, you’ll see nothing unless you ask for merges (see below).

2. Diff two trees/commits explicitly

```bash
git diff-tree -p <old-tree-or-commit> <new-tree-or-commit>
```

Great when you want to compare any two points, not just “commit vs parent”.

3. Show only file names (no patch)

```bash
git diff-tree --name-only -r <commit>
```

Add `-r` to recurse into subdirectories so you get a flat list.

4. Show names with change type

```bash
git diff-tree --name-status -r <commit>
# Outputs lines like:
# A path/to/newfile
# M path/to/modified
# D path/to/deleted
```

5. Show a patch (full diff)

```bash
git diff-tree -p <commit>            # unified diff like `git show`
git diff-tree -U1 -p <commit>        # less context (1 line)
```

# Must-know options (with why/when)

* `-r` — Recurse into subtrees so you see all nested paths. Without it, a directory that changed might show as a single line.
* `--no-commit-id` — Suppress the “commit <sha>” header when you’re scripting per-commit output.
* `--root` — When a commit has **no parent** (initial commit), still show its changes vs the empty tree.
* `-m` — For merge commits, show diffs **against each parent** (produces multiple diffs).
* `-c` / `--cc` — Combined merge diff. `--cc` is a refined view (what `git show` uses for merges).
* `--name-only` / `--name-status` / `--stat` / `--numstat` — Different summary styles. `--numstat` is script-friendly (added/removed line counts).
* `--diff-filter=<set>` — Filter by change types, e.g. `--diff-filter=AM` (only Added or Modified); common letters: `A`dd, `M`odified, `D`eleted, `R`enamed, `C`opied, `T`ype changed.
* `-M` / `-C` — Detect renames and copies. Add an optional similarity threshold, e.g. `-M90%`.
* `--relative[=<path>]` — Restrict output to a subdirectory; without an argument, it uses the current working dir.
* `-z` — **NUL-terminate** paths for unambiguous machine parsing (handles newlines or tabs in filenames).
* `--stdin` — Read a list of commits (or pairs) from standard input. This is the secret sauce for fast batch operations.

# Canonical scripting patterns

### 1) List changed files for a single commit

```bash
git diff-tree --no-commit-id --name-status -r <commit>
```

### 2) Batch over many commits (fast!)

```bash
git rev-list main --since="2025-08-01" |
  git diff-tree --stdin -r --no-commit-id --name-status
```

`--stdin` avoids spawning `git` per commit and is much faster for large ranges.

### 3) Only additions and modifications in a directory

```bash
git diff-tree -r --no-commit-id --name-status \
  --diff-filter=AM <commit> -- src/backend/
```

### 4) Count lines added/removed per file (script-friendly)

```bash
git diff-tree -r --no-commit-id --numstat <commit>
# Outputs: "<added>\t<deleted>\t<path>"
```

### 5) Detect and show renames in a commit

```bash
git diff-tree -r --no-commit-id -M --name-status <commit>
# Lines like: "R100 old/name.txt\tnew/name.txt"
```

### 6) Patch for a merge commit

```bash
git diff-tree -m -p <merge-commit>     # per-parent patches
git diff-tree --cc <merge-commit>      # combined view (single patch)
```

### 7) Initial commit (no parent)

```bash
git diff-tree --root -p <initial-commit>
```

# Understanding the raw record format (if you parse by hand)

Use `--raw` (implicitly used by some modes) to get minimal, stable records:

```
:100644 100644 <oldsha> <newsha> M<TAB>path
```

* Numbers are file modes: `100644` regular file, `100755` executable, `120000` symlink, `160000` gitlink (submodule).
* Status is a single letter (`A`, `M`, `D`, etc.), possibly with a score (e.g., `R100`).
* For renames/copies you’ll see two paths. With `-z`, fields are NUL-separated; without `-z`, they’re tab-separated.

**Tip:** If you are building reliable tooling, always pass `-z` and split on NUL. Filenames with newlines exist.

# Comparing `git diff-tree` to related commands (so you pick the right one)

* `git diff`: compares **index/working tree** vs HEAD or any two commits/trees; interactive development.
* `git show <commit>`: a pretty wrapper for “diff vs parent + metadata.” Great for humans.
* `git log -p`: history plus patches. For ranges, it’s often more convenient than manually looping `diff-tree`.
* `git diff-tree`: plumbing for **precise, scriptable per-commit diffs**, batchable with `--stdin`.

# Real-world examples

### “What changed in this PR merge commit?”

```bash
git diff-tree --cc <merge-commit> | less
```

If you need parent-wise detail:

```bash
git diff-tree -m -p <merge-commit> | less
```

### “Feed a CI step a clean list of files modified by the latest commit”

```bash
git diff-tree --no-commit-id --name-only -r HEAD > changed.txt
```

### “Only Java files added or modified in the last 20 commits”

```bash
git rev-list -n 20 HEAD |
  git diff-tree --stdin -r --no-commit-id --name-only --diff-filter=AM |
  grep -E '\.java$'
```

### “Summarize churn (added/removed lines) for a release tag”

```bash
git diff-tree -r --no-commit-id --numstat v1.2.0..v1.3.0
```

### “Handle weird filenames safely”

```bash
git diff-tree -z -r --no-commit-id --name-status <commit> |
  awk -v RS='\0' 'NR%2{status=$0; next}{printf "%s %s\n", status, $0}'
```

# Performance notes

* Prefer `--stdin` with `git rev-list` for big ranges; it avoids process churn.
* Skip patches (`--name-only`/`--name-status`) when you don’t need line changes.
* Avoid rename detection (`-M`, `-C`) if you care about speed over accuracy.

# Gotchas & edge cases

* **No output for merges by default.** You must pass `-m` (per-parent) or `--cc`/`-c` (combined).
* **Initial commit is “empty tree vs tree”.** Use `--root` to force a diff.
* **Submodules** show mode `160000` and a SHA (gitlink). You won’t see inner diffs unless you diff inside the submodule repo.
* **Pathspecs are after `--`.** If you filter by paths, put them after `--` to avoid ambiguity.
* **Filenames with whitespace/newlines.** Always add `-z` if you’re parsing.

# Quick “cheat snippets” you’ll actually reuse

```bash
# Files changed (flat list)
git diff-tree --no-commit-id --name-only -r <commit>

```
