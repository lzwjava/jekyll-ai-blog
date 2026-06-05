---
audio: false
generated: true
image: false
lang: en
layout: post
title: Streamlined CI and pre-commit duplicate checks
translated: false
type: note
---

Here's what I did:

1. **Removed the full unit test step from `.github/workflows/gh-pages.yml`** — the "Run Unit Tests" step that ran `python -m unittest discover -s tests/workflow` is gone. No more running 15 workflow tests in CI.

2. **Added duplicate-notes-check to `.pre-commit-config.yaml`** — runs `python3 -m unittest tests.workflow.test_duplicate_notes -v` on every commit. Catches duplicates before they land.

3. **Fixed 5 duplicate note pairs** that existed in today's `notes/`:
   - `rust-path-separator-scope-navigation-en.md` vs `understanding-rust-double-colon-path-separator-en.md`
   - `building-personal-moats-beyond-job-titles-en.md` vs `build-durable-skills-not-fragile-titles-en.md`
   - `marcs-lebanon-energy-storage-market-diary-en.md` vs `a-solo-market-development-journey-en.md`
   - `nanochat-training-run-evaluation-and-recommendations-en.md` vs `training-run-undertrained-per-scaling-laws-en.md`
   - `fixing-vscode-proxy-authentication-prompts-en.md` vs `fixing-vscode-proxy-popups-en.md`

4. **Reinstalled pre-commit** with `-f` flag to fix the migration mode warning.

The hook is now live — any commit with duplicate notes in `notes/` will be blocked.
