---
audio: false
generated: true
image: false
lang: en
layout: post
title: Incomplete Backup and Recovery Script
translated: false
type: note
---

========================================================================
  BACKUP STATUS
========================================================================

  COMPLETE:
    Projects ........ 47/47  ✓
    Desktop ......... 20/20  ✓
    Documents ....... 27/27  ✓
    Photos/0-5 ...... 1845/1845  ✓

  INCOMPLETE:
    Photos/6 ........ 213/297  (84 missing)
    Photos/7-F ...... 0/2846   (all 10 subdirs empty)

  Total missing: 2,930 files (~12GB)

========================================================================
  RUN ON MACBOOK:
    bash ~/fix_backup3.sh
========================================================================

What it does:
  - Transfers originals/6 through originals/F one at a time
  - Each subdir is 1.2-3.1GB, finishes in 5-10 min
  - --partial resumes if it dies mid-transfer
  - Built-in verify at the end with per-subdir count comparison
  - If one fails, just run it again — only the failed one needs redo

Why it wasn't "truly successful":
  The fix_backup2.sh script transferred the small library parts
  (database, private, resources, scopes) and originals/0-5 fine,
  but originals/6-F (the remaining 12GB) timed out. The script
  logged "DONE" because it didn't check the rsync exit codes
  properly for the batched originals transfers.