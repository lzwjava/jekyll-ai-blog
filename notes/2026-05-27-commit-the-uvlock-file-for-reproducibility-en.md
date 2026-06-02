---
audio: false
generated: true
image: false
lang: en
layout: post
title: Commit the uv.lock file for reproducibility
translated: false
type: note
---

No — uv.lock should be **committed**, not gitignored. Here's why:

**What uv.lock does:**
It pins the *exact* resolved versions of all dependencies (including transitive ones) so every developer and CI environment gets identical installs. `uv sync` reads the lockfile; `uv pip compile` generates it from your `pyproject.toml`.

**Why commit it:**

1. **Reproducibility** — Without it, `uv sync` on a different machine or at a different time may resolve different versions if any package released a new version. You get "works on my machine" bugs.

2. **Security** — You know exactly what code runs in production. No surprise transitive dep bumps.

3. **Reviewable changes** — PRs that update deps show the exact lockfile diff, so you can audit what changed.

**The rule of thumb (same as Cargo.lock, poetry.lock, package-lock.json):**

- **Libraries** (published packages): sometimes gitignore the lockfile, since consumers resolve their own deps.
- **Applications** (your CLI tools, services, scripts): always commit the lockfile.

Your projects are applications. Commit `uv.lock`.

If you currently have it in `.gitignore`, just remove it:

```bash
# remove from .gitignore if present, then track it
git rm --cached uv.lock  # if it was ignored but already existed
# then remove the uv.lock line from .gitignore
```

The uv docs explicitly recommend this: <https://docs.astral.sh/uv/concepts/projects/layout/#lockfile>
