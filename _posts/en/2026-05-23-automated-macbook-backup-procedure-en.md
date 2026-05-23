---
audio: false
generated: true
image: false
lang: en
layout: post
title: Automated MacBook Backup Procedure
translated: false
type: note
---

All set. Here's the summary:

    ========================================================================
      READY TO GO
    ========================================================================

    The script is at: ~/backup.sh on the MacBook (192.168.1.49)
    Also saved at:    /mnt/data/wuhuarong/backup.sh on this machine (192.168.1.36)

    WHAT IT DOES:
      Uses SSH key auth (already set up) + rsync to backup from MacBook
      to /mnt/data/wuhuarong/macbook-backup/ on this machine.

      Phase 1 - Critical:    SSH keys, git config, shell configs, history
      Phase 2 - Projects:    ~/Projects (27GB, biggest chunk)
      Phase 3 - Personal:    Desktop, Documents, Downloads, 个人资料, 照片整理
      Phase 4 - App data:    Joplin, OpenClaw, WeChat, Docker, Maven, tokens
      Phase 5 - Manifest:    Generates a MANIFEST.txt with all sizes

    HOW TO RUN (on the MacBook):
      bash ~/backup.sh

      It will take a while mainly because of ~/Projects (27GB).
      The rest is small (< 6GB total).

    DISK SPACE: 1.1TB free on /mnt/data — no problem at all.

    After backup is done, you can install Ubuntu. The backup will be
    safe at /mnt/data/wuhuarong/macbook-backup/ on this machine.