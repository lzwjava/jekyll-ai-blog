---
audio: false
generated: true
image: false
lang: en
layout: post
title: Lessons from Failed Rsync Backups
translated: false
type: note
---

Now I have the full picture. Here's what went wrong last time:

**Issue 1: SSH connection drops (rsync error code 255)**
```
rsync error: unexplained error (code 255) at ... io.c(453) [sender=2.6.9]
```
The SSH connection dies mid-transfer. The original `backup.sh` had no `ServerAliveInterval` — when a large transfer (Projects ~27GB) runs for a long time with no data flowing on the control channel, the router or OS silently kills the TCP connection. rsync gets a broken pipe and exits with code 255.

**Issue 2: Old rsync version (2.6.9)**
macOS ships rsync 2.6.9 from 2006. It has known bugs with:
- Symlink handling in deeply nested directories (node_modules have thousands of symlinks)
- No `--timeout` support to recover from stalls
- Worse error reporting than modern rsync 3.x

**Issue 3: node_modules symlink explosion**
Projects with node_modules (like `admin-vue3-micro-qiankun`) have tens of thousands of symlinks. The backup log is full of symlink lines. rsync 2.6.9 struggles with these — slow scanning, broken link resolution, connection timeout during the file list phase.

**Issue 4: Photos library too large to transfer in one shot**
The Photos library (`照片图库.photoslibrary`) is ~4GB with 4,888 original files. The first attempt (backup.sh → fix_backup.sh) failed. The fix scripts evolved:
- `fix_backup2.sh` — broke Photos into subdirectory batches (resources, originals, private, etc.)
- `fix_backup3.sh` — broke originals/ further into hex subdirs (0-F), each with 266-338 files
- Even then, `backup4.log` shows all 16 originals subdirs showing `0 vs XXX INCOMPLETE` — the transfer said "OK" but the verification found 0 files on the remote. The `--inplace` flag or path mismatch caused silent data loss.

**Issue 5: No `--partial` flag originally**
Without `--partial`, an interrupted rsync deletes the partially-transferred file. So every connection drop means restarting that file from scratch. With `--partial`, rsync keeps the partial file and resumes.

**Issue 6: No timeout protection**
The original script had no `--timeout=N`. When the network stalls, rsync hangs forever. The fix scripts added `--timeout=300` and `--timeout=600`.

**How the current `mini-backup.sh` addresses these:**
- `ServerAliveInterval=30` + `ServerAliveCountMax=10` — keepalive pings every 30s, drop after 10 failures
- `--partial` — resume interrupted files
- `--timeout=300` — don't hang forever on stalls
- Incremental rsync on existing backup — much less data to transfer this time
- Skipping node_modules via `--exclude` would be even better, but the script doesn't do that yet

Want me to add `--exclude='node_modules'` and `--exclude='.git'` to skip the biggest problem dirs?
