---
audio: false
generated: true
image: false
lang: en
layout: post
title: MacBook Pro to Mac Mini Backup
translated: false
type: note
---

Script created and verified. Here's the summary:

```
~/mini-backup.sh on wuhuarong@192.168.1.52 (MacBook Pro 2017)
```

What it does:
- Backs up MacBook Pro → Mac Mini (huarong@192.168.1.54)
- Destination: ~/old-mac-backup/
- Uses SSH key auth (already configured)
- Downloads: EXCLUDED (per your request)

Phases:
1. SSH keys, git config, shell configs (.zshrc, .bashrc, history, etc.)
2. Projects (biggest chunk)
3. Personal files — Desktop, Documents, 个人资料, 照片整理, Pictures (NO Downloads)
4. App data — Joplin, OpenClaw, WeChat, Docker, Maven, tokens
5. Generate MANIFEST.txt on remote

Previous backup (~/macbook-backup/) was 6GB. This one should be ~5GB (minus Downloads's 963M).

Mac Mini has 239GB free — plenty of room.

To run:
```
ssh wuhuarong@192.168.1.52
bash ~/mini-backup.sh
```

The script will show colored progress and log to ~/mini-backup_<timestamp>.log.
