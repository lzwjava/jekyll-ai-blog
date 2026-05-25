---
audio: false
generated: true
image: false
lang: en
layout: post
title: Duplicate Note Removal Fixes Tests
translated: false
type: note
---

Here's what happened:

THE PROBLEM
===========
Two notes had identical content but different filenames:
  - 2026-05-24-agentsmd-per-project-context-flow-en.md
  - 2026-05-24-how-hermes-agent-uses-project-context-files-en.md

The duplicate detection test (test_no_duplicate_notes) compares note body content within each date group. Both files had the exact same 79-line body about how AGENTS.md works in Hermes Agent (startup injection + runtime subdirectory hints).

THE FIX
=======
Deleted the less descriptive duplicate (agentsmd-per-project-context-flow-en.md), kept the better-named one (how-hermes-agent-uses-project-context-files-en.md).

  git rm notes/2026-05-24-agentsmd-per-project-context-flow-en.md
  git commit -m "fix(notes): remove duplicate note, keep how-hermes-agent-uses-project-context-files-en"
  git push

CI RETRIGGER
============
Push to main automatically triggers the "Deploy Jekyll" workflow (the main deploy pipeline). That workflow:
  1. Translates posts/notes via DeepSeek
  2. Fixes markdown tables
  3. Installs ww CLI
  4. Runs unit tests (including test_no_duplicate_notes) ← this should now pass
  5. Builds Jekyll site
  6. Deploys to lzwjava.github.io

The "Build and Deploy" workflow (manual trigger) also ran its tests step. Both should pass now since the duplicate is gone.