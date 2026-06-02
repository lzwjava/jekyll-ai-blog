---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixed Duplicate Notes Bug Report
translated: false
type: note
---

Done. Here's the summary:

**Root Cause:**

1. `create_note_from_content()` had NO duplicate check - only `create_note()` checked
2. Hermes `/note` plugin and research agent call `create_note_from_content()` directly
3. Bug in `check_duplicate_notes.py`: `note_files[:-1]` removed oldest file instead of newest

**Fixes Applied:**

1. **ww repo** (`/Users/lzwjava/projects/ww`):
   - Added duplicate check to `create_note_from_content()` - checks against latest 200 notes
   - Fixed `check_duplicate_notes.py` line 84: `note_files[:-1]` → `note_files[1:]`
   - Committed and pushed

2. **jekyll-ai-blog repo** (`/Users/lzwjava/projects/jekyll-ai-blog`):
   - Removed duplicate file: `2026-05-30-cost-saving-gpt-3-training-on-amd-cloud-en.md`
   - Kept: `2026-05-30-reduce-gpt-3-training-costs-amd-cloud-en.md`
   - Committed and pushed

**CI Status:** The next GitHub Actions run should pass the duplicate check test.
