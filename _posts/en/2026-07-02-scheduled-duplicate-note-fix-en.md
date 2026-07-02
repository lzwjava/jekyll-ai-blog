---
audio: false
generated: true
image: false
lang: en
layout: post
title: Scheduled Duplicate Note Fix
translated: false
type: note
---

The workflow runs on a schedule (every 2 hours), not on push — so the next run will pick up the fix automatically. Here's the full story:

---

## Root Cause

**Duplicate note pair** detected by `test_no_duplicate_notes`:

| File | Path | Lines |
|------|------|-------|
| `2025-10-06-finacle-vs-avaloq-1-en.md` | notes/ + _posts/en/ +_posts/zh/ | 66 |
| `2025-10-06-finacle-vs-avaloq-en.md` | notes/ + _posts/en/ +_posts/zh/ | 45 |

Same date (`2025-10-06`), same title *"Finacle vs Avaloq Banking Platforms"*, same content. The `-1` variant was a prose-formatted regeneration of the table-based original. The similarity check (first 200 chars with 90%+ match) flagged them as duplicates.

## Fix Applied

Removed all 3 `-1` suffixed duplicates:

- `notes/2025-10-06-finacle-vs-avaloq-1-en.md`
- `_posts/en/2025-10-06-finacle-vs-avaloq-1-en.md`
- `_posts/zh/2025-10-06-finacle-vs-avaloq-1-zh.md`

## Verification

- `test_no_duplicate_notes` passes locally: `✓ No duplicates found among 10953 files`
- Pre-commit hook passed: `Duplicate notes check....Passed`
- Pushed to `main` as `0f12685ab`
- Workflow runs on schedule (`0 */2 * * *`), so next deploy at ~T+2h will pick up the fix

The second failure (run 28501676010) was the same root cause — it also failed on this duplicate pair.
