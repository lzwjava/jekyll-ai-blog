---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Git Filter Repo Path Options Guide
translated: false
type: note
---

**Question:** How does git filter-repo work, and what options are there for --path and --file?

**Answer:**

`git filter-repo` is currently (2025–2026) the recommended and fastest modern tool for rewriting Git history (replacing `git filter-branch` and BFG Repo-Cleaner in most cases).

### How git filter-repo fundamentally works

1. **Reads** the entire repository history once (from oldest → newest commit)
2. **Applies filtering rules** you specify (path filters, blob filters, commit message filters, email filters, etc.)
3. **Rewrites** only the commits that match / are affected by the rules
4. **Creates** a new commit graph (new commit SHAs)
5. **Updates** all references (branches, tags) to point to the new commits
6. **Discards** the old objects (unless you explicitly keep them)

Because it works with the **pack-file format** directly and avoids the porcelain layer, it is usually **10–50× faster** than `git filter-branch`.

### Most common usage patterns with `--path` / `--file`

```bash
# 1. Keep only files in one directory (most common use-case)
git filter-repo --path src/backend/ --path docs/

# 2. Remove one file everywhere (including renames)
git filter-repo --path logs/debug.log --invert-paths

# 3. Remove several files or folders
git filter-repo --path .env --path docker-compose.override.yml --path tests/ --invert-paths

# 4. Same but read paths from a file (very convenient)
git filter-repo --paths-from-file keep-these-paths.txt
# or
git filter-repo --paths-from-file remove-these-paths.txt --invert-paths
```

### Main `--path` / `--file` related options

| Option                        | Meaning                                                                                 | Most common usage                               | Notes / Caveats                                      |
|-------------------------------|-----------------------------------------------------------------------------------------|--------------------------------------------------|------------------------------------------------------|
| `--path <path>`               | Include only this path (file, folder, glob)                                            | `--path src/ --path README.md`                  | Can be repeated many times                           |
| `--paths-from-file <file>`    | Read list of paths from file (one per line), same semantics as `--path`                | `--paths-from-file keep.txt`                    | Very convenient for 10+ paths                        |
| `--invert-paths`              | **Invert** the selection: everything **except** the listed paths is kept               | `--path secret.txt --invert-paths`              | Most common way to **remove** files                  |
| `--path-glob <pattern>`       | Include/exclude using fnmatch-style glob (`*.py`, `ci/*`)                              | `--path-glob '*/secrets/*' --invert-paths`      | Does **not** need `--invert-paths` to exclude        |
| `--path-regex <regex>`        | Include/exclude using regular expression                                               | `--path-regex '.*\.bak$' --invert-paths`        | Very powerful but error-prone                        |
| `--use-base-name`             | Match only filename (not full path) when using `--path` / `--path-glob`                | `--path-glob '*.bak' --use-base-name`           | Rarely needed                                        |
| `--no-blobs-size-limit`       | Process even very large blobs (default cuts off at ~2 GiB)                             | —                                               | Use only when you know you have huge files           |

### Typical real-world command patterns (2025–2026)

```bash
# Remove single sensitive file everywhere (including renames)
git filter-repo --path api-keys.json --invert-paths --force

# Remove multiple files listed in a text file
git filter-repo --paths-from-file sensitive-files.txt --invert-paths --force

# Keep only frontend code + documentation
git filter-repo --path frontend/ --path docs/ --path README.md --path LICENSE --force

# Remove all .env* files using glob
git filter-repo --path-glob '.env*' --invert-paths --force

# Remove everything under any "secrets" folder
git filter-repo --path-glob '*/secrets/*' --invert-paths --force
```

### Important flags almost everyone uses with filter-repo

- `--force`
  Required after you already ran filter-repo once in the same clone

- `--dry-run`
  Show what would be done without actually rewriting anything

- `--analyze`
  Useful before first run — shows biggest files, biggest commits, path statistics

- `--target <directory>`
  Write filtered result into a separate directory instead of overwriting current repo

### Quick mental model

Think of it as:

```
git filter-repo --path ...    →  "only keep these paths"
git filter-repo --path ... --invert-paths   →  "delete these paths"
```

And you can combine normal `--path`, `--path-glob`, `--path-regex` and `--paths-from-file` — they all **add** to the include/exclude list.

**References:**

- [https://github.com/newren/git-filter-repo/blob/main/Documentation/git-filter-repo.txt](https://github.com/newren/git-filter-repo/blob/main/Documentation/git-filter-repo.txt)
- [https://github.com/newren/git-filter-repo](https://github.com/newren/git-filter-repo)
