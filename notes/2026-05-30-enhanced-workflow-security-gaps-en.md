---
audio: false
generated: true
image: false
lang: en
layout: post
title: Enhanced Workflow Security Gaps
translated: false
type: note
---

Here's what I found:

== CURRENT STATE ==

PRE-COMMIT (.pre-commit-config.yaml):
  [x] trailing-whitespace
  [x] end-of-file-fixer
  [x] check-yaml
  [x] check-toml
  [x] check-merge-conflict
  [x] debug-statements
  [x] ruff (lint + format)
  [x] pyright

CI (.github/workflows/):
  [x] unit_test.yml  — unittest + coverage
  [x] integration_test.yml — unittest discover
  [ ] No lint/type-check CI workflow
  [ ] No security scanning CI
  [ ] No coverage threshold enforcement

.gitignore:
  [x] .env, __pycache__, .coverage, .pytest_cache

Tests: 50+ test files — solid coverage exists.

== GAPS — ranked by value for ww ==

1. MISSING: No security hooks at all
   ww handles API keys (OpenRouter, GitHub, AMD cloud), SSH
   connections, cloud credentials. One leaked .env = disaster.
   Need: bandit + detect-secrets

2. MISSING: No large-file guard
   ML project — easy to accidentally commit model weights or
   large datasets. Need: check-added-large-files

3. MISSING: No CI workflow for ruff/pyright
   Pre-commit catches locally, but contributors who skip
   pre-commit (--no-verify) get nothing. Need: lint CI job.

4. MISSING: No dependency audit
   27 direct deps, many cloud/LLM SDKs. Need: pip-audit

5. MISSING: No coverage threshold
   Unit test CI runs coverage but doesn't gate on it.
   Tests could silently drop to 20% and CI still passes.

6. MISSING: No no-commit-to-branch
   Nothing prevents direct pushes to main.

== QUICK WINS (add in this order) ==

1. Add to .pre-commit-config.yaml:
   - bandit (security)
   - detect-secrets (credential leak prevention)
   - check-added-large-files (500KB max)
   - check-ast (Python syntax validity)
   - no-commit-to-branch (protect main)

2. Add lint CI job:
   - ruff check + ruff format --check
   - pyright
   - bandit -r ww/ -ll

3. Add coverage threshold to unit_test.yml:
   --cov-fail-under=60

4. Add pip-audit to CI

Want me to implement any of these? I'd suggest starting with the pre-commit additions (#1) since that's the highest-impact, lowest-effort change.
