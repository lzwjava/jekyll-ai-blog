---
audio: false
generated: true
image: false
lang: en
layout: post
title: Backup Progress and Resume Fix
translated: false
type: note
---

Good data. The fix_backup2.sh is already on the Mac. Here's the situation:

========================================================================
  STATUS
========================================================================

Projects: 47/47 COMPLETE ✓

Pictures: PARTIAL — needs resume
  Already backed up:
    - small items ($RECYCLE.BIN, Camera Roll, scans, etc.)
    - originals/0: 311 files (1.3G)
    - originals/1: 322 files (1.9G)
    - originals/2: 291 files (1.6G)
    - originals/3: 328 files (1.9G)
    - originals/4: 140 files (557M) ← was mid-transfer when timed out
    - originals/5-F: EMPTY (not started)

  Remaining: ~3,496 files, ~24GB
  (originals 4-9, A-F + private + resources + database)

========================================================================
  FIX_BACKUP2.SH — on MacBook at ~/fix_backup2.sh
========================================================================

What it does differently from fix_backup.sh:
  - Transfers Photos library by subdirectory (not one giant rsync)
  - Each subdir is 1-3GB (won't timeout)
  - Uses --partial + --inplace so interrupted transfers RESUME
  - ServerAliveInterval=15 keeps SSH alive
  - Skips already-complete subdirs automatically (rsync checksum)

Run on MacBook:
  bash ~/fix_backup2.sh

If any single subdir times out, just run it again — rsync will
pick up where it left off thanks to --partial.

Estimated time: ~1-2 hours for the remaining 24GB.