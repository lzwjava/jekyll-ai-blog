---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Rsync Dual Disk Backup Guide
translated: false
type: note
---

**Question:** Suppose I have two disks to back up some files totaling 50 GB. How do I use rsync to sync between my computer and two portable disks?

**Answer:**

For a simple backup strategy with **two portable disks** (e.g. two external USB drives), the most common and reliable approach is:

- Treat your **computer** (source folder) as the single source of truth.
- Use rsync to **mirror** that source to **each** portable disk separately (one rsync run per disk).
- This gives you two independent, identical backups.

Rsync does **not** natively copy to multiple destinations in one command (unless using advanced batch mode or scripts), so you run it twice — once for each disk.

### Recommended rsync command (macOS / Linux)

Connect both portable disks. Assume:

- Your files to back up are in: `~/ImportantData/` (or `/path/to/your/50GB/folder/`)
- Disk 1 mounts as: `/Volumes/BackupDisk1`
- Disk 2 mounts as: `/Volumes/BackupDisk2`

Use this **safe & commonly recommended** set of options:

```bash
# First backup — to Disk 1
rsync -avh --progress --delete \
  --exclude='.*' \
  --exclude='Desktop' --exclude='Downloads' --exclude='Library' \
  ~/ImportantData/  "/Volumes/BackupDisk1/ImportantData Backup/"

# Then to Disk 2 (same command, just change destination)
rsync -avh --progress --delete \
  --exclude='.*' \
  --exclude='Desktop' --exclude='Downloads' --exclude='Library' \
  ~/ImportantData/  "/Volumes/BackupDisk2/ImportantData Backup/"
```

Key options explained:

- `-a` = archive mode (recursive + preserves permissions, times, symlinks, etc.)
- `-v` = verbose (shows what’s happening)
- `-h` = human-readable sizes (easier to read)
- `--progress` = shows transfer progress for each file (very useful for 50 GB)
- `--delete` = deletes files on the backup disk that no longer exist in source (true mirror/backup)
- `--exclude='.*'` = skips macOS hidden files (.DS_Store, ._* files, etc.) — very common on macOS to avoid junk
- Add more `--exclude` for folders you never want to back up (e.g. caches, temp files)

### First time vs. later times

- **First run** (empty destination): Will copy all ~50 GB → takes longest (hours depending on USB speed).
- **Later runs** (incremental): Only changed/new/deleted files are processed → usually very fast (seconds to minutes).

### Even better / safer variants

1. **Add --dry-run first** (simulation — highly recommended!):

```bash
rsync -avh --dry-run --progress --delete ~/ImportantData/ "/Volumes/BackupDisk1/ImportantData Backup/"
```

Run this → check output → make sure nothing unexpected gets deleted.

2. **Keep modification times & extended attributes** (good on macOS):

```bash
rsync -aEvh --progress --delete ...
# -E preserves macOS extended attributes / resource forks
```

3. **Log the backup** (very useful for later checking):

```bash
rsync -avh --progress --delete --log-file=~/backup-log-$(date +%Y-%m-%d).txt \
  ~/ImportantData/ "/Volumes/BackupDisk1/ImportantData Backup/"
```

4. **Make it fully automatic** (one script):

Create a file `backup.sh`:

```bash
#!/bin/bash

SOURCE="$HOME/ImportantData/"
DEST1="/Volumes/BackupDisk1/ImportantData Backup/"
DEST2="/Volumes/BackupDisk2/ImportantData Backup/"

echo "Backing up to Disk 1..."
rsync -avh --progress --delete --exclude='.*' "$SOURCE" "$DEST1"

echo "Backing up to Disk 2..."
rsync -avh --progress --delete --exclude='.*' "$SOURCE" "$DEST2"

echo "Backup finished at $(date)"
```

Then run: `bash backup.sh`

### Tips for 50 GB on portable disks

- Use USB 3.0+ ports and drives → much faster than USB 2.0.
- First backup: do it overnight or when you don’t need the computer.
- Eject disks properly after backup (`diskutil eject /Volumes/BackupDisk1`).
- If disks are used only for backup → format them as **APFS** (macOS) or **exFAT** (cross-platform).
- Alternative tools if you want rotation/history (not just mirror): rsync + `--backup --backup-dir=../backups/$(date +%Y-%m-%d)` or tools like rsnapshot/Borg.

This gives you two separate, up-to-date backups — rotate them (e.g. keep one offsite) for better protection.

**References:**

- [https://apple.stackexchange.com/questions/224747/using-rsync-to-backup](https://apple.stackexchange.com/questions/224747/using-rsync-to-backup)
- [https://deepakness.com/blog/ext-hdd-backup](https://deepakness.com/blog/ext-hdd-backup)
- [https://serverfault.com/questions/137119/can-i-rsync-to-multiple-destinations-using-same-filelist](https://serverfault.com/questions/137119/can-i-rsync-to-multiple-destinations-using-same-filelist)
- [https://askubuntu.com/questions/556580/using-rsync-to-backup-to-two-locations](https://askubuntu.com/questions/556580/using-rsync-to-backup-to-two-locations)
