---
audio: false
generated: true
image: false
lang: en
layout: post
title: Pre Commit Hooks on GitHub Guide
translated: false
type: note
---

**Question:** How do you use pre-commit hooks with a `.pre-commit-config.yaml` file, and do they work when the repository is hosted on GitHub?

---

**Answer:**

## Overview

Pre-commit hooks from the `pre-commit` framework are **client-side** by nature — they run on each developer's local machine. However, there are two complementary layers you can use:

1. **Local hooks** — run on each developer's machine before every `git commit`
2. **Server-side / CI enforcement** — run on GitHub via GitHub Actions or pre-commit.ci

---

## Part 1: Local Setup (Every Team Member Must Do This)

### Step 1 — Install the `pre-commit` tool

```bash
pip install pre-commit
```

### Step 2 — Commit `.pre-commit-config.yaml` to your repo

This file (the one you showed) should live at the root of your repo and be committed like any other file. It needs a `rev` (version tag) for each hook source:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0   # <-- specify a version tag!
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
  - repo: https://github.com/psf/black
    rev: 23.12.0  # <-- specify a version tag!
    hooks:
      - id: black
```

### Step 3 — Install the hooks into the local git repo

```bash
pre-commit install
```

This installs the hook scripts into your `.git/hooks` directory, so `pre-commit` will now run automatically on every `git commit`.

### Step 4 — (Optional) Run manually on all files

```bash
pre-commit run --all-files
```

---

## Part 2: What Happens on Commit

The pre-commit hook runs first, before you even type a commit message. If it exits non-zero, the commit is aborted. You'll see output like:

```
Trim Trailing Whitespace.......................Passed
Fix End of Files...............................Passed
black..........................................Failed
- hook id: black
- files were modified by this hook
```

When hooks **auto-fix** files (like Black reformatting code), the modified files are left as unstaged changes. You must stage them and commit again:

```bash
git add .
git commit -m "your message"
```

You always need to stage and commit any changes that the hooks make — this gives you final say on what enters the codebase.

To **bypass hooks temporarily** (use sparingly):

```bash
git commit -m "WIP" --no-verify
```

---

## Part 3: Does It Work With GitHub-Hosted Repos?

### The Critical Limitation

Pre-commit hooks are client-side — they are triggered by local operations like committing and merging, not by server-side network operations. This means:

- GitHub does **not** automatically run them
- If a teammate hasn't run `pre-commit install`, their commits bypass the hooks entirely
- Commits made through the **GitHub web UI** skip local hooks completely

### Solution A: GitHub Actions (Recommended for Teams)

Someone may create a pull request via the GitHub UI, and pre-commit hooks won't run natively in that case. To enforce hooks on every push/PR, add a workflow file:

```yaml
# .github/workflows/pre-commit.yml
name: pre-commit

on:
  pull_request:
  push:
    branches: [main]

jobs:
  pre-commit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v3
      - uses: pre-commit/action@v3.0.1
```

By default, this action runs all hooks against all files. You can also specify a single hook via `extra_args`.

### Solution B: pre-commit.ci (Easiest Option)

You can run hooks both locally and in the cloud. As a CI check with `https://pre-commit.ci`, you can enforce passing hooks on pull requests and auto-fix trivial problems like styling, even if the committer does not have a local installation.

Simply sign in at [pre-commit.ci](https://pre-commit.ci), connect your GitHub repo, and it handles everything — no extra workflow files needed.

---

## Summary Table

| Layer | Who runs it | Enforces formatting | Requires setup per dev |
| --- | --- | --- | --- |
| Local `pre-commit install` | Developer's machine | Yes, blocks commit | Yes |
| GitHub Actions | GitHub CI runner | Yes, fails PR/push | No (automatic) |
| pre-commit.ci | Cloud service | Yes, can auto-fix | No (automatic) |

The recommended approach for teams is **both**: local hooks for fast feedback, plus GitHub Actions or pre-commit.ci as the safety net.

---

**References:**

- [pre-commit official docs](https://pre-commit.com/)
- [pre-commit/action on GitHub Marketplace](https://github.com/marketplace/actions/pre-commit)
- [Stefanie Molin – How to Set Up Pre-Commit Hooks](https://stefaniemolin.com/articles/devx/pre-commit/setup-guide/)
- [Running pre-commit hooks as GitHub Actions](https://thomasthornton.cloud/2022/08/04/running-pre-commit-hooks-as-github-actions/)
- [pre-commit.ci](https://pre-commit.ci)
