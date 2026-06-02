---
audio: false
generated: true
image: false
lang: en
layout: post
title: Understanding Pre-Commit Hook Behavior with Auto-Fixers
translated: false
type: note
---

I see the friction — but here's the thing: `trailing-whitespace` and `end-of-file-fixer` **already do auto-fix**. The "Failed" status just means they modified files. Pre-commit then aborts the commit on purpose (by design), so you must `git add` + commit again.

There is **no config flag** in `.pre-commit-config.yaml` that makes pre-commit auto-stage and continue — it's an intentional safety choice by pre-commit's authors. It's not like `ruff --fix` where the fix happens and the same hook then re-checks; for the pre-commit-hooks fixers, the "fix" *is* the modification, and any modification = failure.

So the real options are:

1. **Editor-side fix (recommended)** — make your editor trim trailing whitespace + ensure newline at EOF on save. Then these hooks never trigger. I can add a `.editorconfig` so VS Code / most editors do this automatically.
2. **Remove the two noisy hooks** — drop `trailing-whitespace` and `end-of-file-fixer` from `.pre-commit-config.yaml`. They mainly catch editor sloppiness; if your editor handles it, they're redundant.
3. **Wrapper script** — a `git commit` wrapper that runs `pre-commit run` first, `git add -u`, then commits. More moving parts, works but lives outside the config file.

Which do you want? My pick is #1 (editorconfig) + keep the hooks as a safety net — that way you stop hitting the double-commit, but commits from other machines still get cleaned up.
