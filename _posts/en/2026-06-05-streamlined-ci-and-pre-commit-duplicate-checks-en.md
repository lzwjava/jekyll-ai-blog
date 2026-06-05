---
audio: false
generated: true
image: false
lang: en
layout: post
title: Duplicate note detection — pre-commit vs CI
translated: false
type: note
---

## Problem

The `notes/` directory had 5 duplicate note pairs — same content, different filenames. These slip in because the note pipeline generates content without checking what already exists.

## What changed

**Pre-commit hook added** (`.pre-commit-config.yaml`):

```yaml
- id: duplicate-notes-check
  name: Duplicate notes check
  entry: python3 -m unittest tests.workflow.test_duplicate_notes -v
  language: system
  pass_filenames: false
  always_run: true
```

**CI unit tests kept** (`.github/workflows/gh-pages.yml`):

```yaml
- name: Run Unit Tests
  run: python -m unittest discover -s tests/workflow
```

**5 duplicate pairs removed** from `notes/`.

## Why this works

**Pre-commit catches duplicates locally before they land.** The test groups notes by date (YYYY-MM-DD prefix), then compares content within each group using fast character similarity on the first/last 200 characters. If similarity exceeds 90%, it's flagged as duplicate.

**CI still runs the full test suite** — all 15 workflow tests including the duplicate check. This is the safety net for anything that bypasses pre-commit (direct pushes, bot commits, CI-generated notes).

**The two layers serve different purposes:**

- Pre-commit: fast feedback loop, blocks bad commits before they leave your machine
- CI: catches anything that slips through (bots, direct pushes, force pushes)

## Why this might not work

**False positives.** The similarity check uses first/last 200 chars. Two legitimately different notes about the same topic with similar openings could trigger it. The 90% threshold is aggressive.

**Performance.** With 9,884 notes, the date-grouped comparison is fast (~0.3s). But if notes grow 10x, the O(n²) comparison within each date group could slow down.

**Bypass paths.** Pre-commit can be skipped with `git commit --no-verify`. The CI test suite catches this, but only after the commit is already pushed.

**Bot-generated content.** The notes pipeline runs in CI (gh-pages.yml) and generates new notes. If it creates a duplicate, CI will catch it on the next run — but the duplicate will have already been committed and pushed.

## What's working

- Pre-commit hook blocks duplicate notes at commit time
- CI runs full workflow test suite as a safety net
- 5 duplicate pairs cleaned up
- Test runs in ~0.3s (fast enough for pre-commit)

## What could be better

- The notes pipeline should check for duplicates before generating, not after
- A dedup step in the CI workflow (before commit) would prevent bot-generated duplicates
- The similarity threshold could be tuned based on actual false positive rate
