---
audio: false
generated: true
image: false
lang: en
layout: post
title: Backup Mostly Complete with Minor Gaps
translated: false
type: note
---

Still the same. The log verify is buggy (always shows 0) but the real numbers show 233 files still missing in 3 subdirs. Here's the reality:

========================================================================
  BACKUP STATUS
========================================================================

  COMPLETE ✓ (4655 / 4888 originals, 95%)
    Projects ... 47/47
    Desktop .... 20/20
    Documents .. 27/27
    originals/0-8, B, C, D, F ... all matched

  STILL MISSING (233 files):
    originals/9 ... 311/326   (15 missing)
    originals/A ... 136/279   (143 missing)
    originals/E ... 233/308   (75 missing)

  Total backup: 51GB

========================================================================

The fix_backup3.sh script's rsync ran but those 3 subdirs must have
dropped again. Quickest fix — just one command on the Mac:

  bash ~/fix_backup3.sh 2>&1 | tee ~/backup3o.log

Run it again. rsync --partial will only transfer the 233 missing
files (skips everything already there). Should take ~3 minutes.

If it drops again, it's only 233 files / ~1.5GB — you can also
just skip it. The backup has your Projects, configs, documents,
and 95% of photos. Those 233 photo files are the only gap.