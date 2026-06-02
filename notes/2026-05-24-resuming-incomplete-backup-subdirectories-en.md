---
audio: false
generated: true
image: false
lang: en
layout: post
title: Resuming Incomplete Backup Subdirectories
translated: false
type: note
---

========================================================================
  BACKUP STATUS — 95% COMPLETE
========================================================================

  COMPLETE ✓
    Projects ............ 47/47
    Desktop ............. 20/20
    Documents ........... 27/27
    Photos originals .... 4655/4888 (13 of 16 subdirs perfect)

  3 SUBDIRS STILL SHORT (233 files):
    originals/9 ... 311/326  (15 missing)
    originals/A ... 136/279  (143 missing)
    originals/E ... 233/308  (75 missing)

  Total backup: 51GB

========================================================================
  JUST RUN THIS AGAIN ON THE MACBOOK:
    bash ~/fix_backup3.sh
========================================================================

It will:

- Skip originals/0-8,B,D,F,C (already complete, rsync detects no diff)
- Resume originals/9, A, E (only transfers the 233 missing files)
- Takes ~5 minutes

After that, everything should show OK in the verify step.
