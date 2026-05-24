---
audio: false
generated: true
image: false
lang: en
layout: post
title: Solving SSH Timeouts in Long Rsync Backups
translated: false
type: note
---

Good question. Let me explain what's actually going on.

========================================================================
  WHY THE BACKUP KEPT FAILING
========================================================================

THE ROOT CAUSE: SSH connection drops during long transfers.

When you run rsync over SSH, the data flows like this:

  MacBook  ---[SSH tunnel]--->  Ubuntu machine (192.168.1.36)

The tunnel stays open the entire time rsync is running. If the tunnel
dies (network hiccup, WiFi glitch, idle timeout), rsync crashes.

WHAT HAPPENED EACH TIME:

  backup.sh:
    Tried to send ALL of ~/Projects (27GB) in ONE rsync call.
    Also tried ALL of ~/Pictures in ONE rsync call.
    SSH dropped mid-transfer → rsync crashes → code 255.

  fix_backup.sh:
    Fixed Projects by sending each project one at a time ✓
    But Pictures was still ONE giant rsync call.
    Transferred 1,392 files (~7GB) over 18 minutes, then:
    "io timeout after 1083 seconds" → SSH died again.

WHY SSH DIES:
  - The Photos library has 4,888 files, many are 10-80MB videos
  - Total: ~30GB
  - At ~3MB/s over LAN, that's ~3 hours of continuous SSH
  - Anything can break it: WiFi sleep, router timeout, macOS
    power management, TCP idle timeout

========================================================================
  WHY "COPY" (like scp) WOULD HAVE THE SAME PROBLEM
========================================================================

scp and rsync both use SSH underneath. They both would timeout
on a 30GB single transfer. The problem is NOT rsync — it's the
SSH tunnel dying during long transfers.

========================================================================
  HOW FIX_BACKUP2.SH SOLVES THIS
========================================================================

Instead of one giant rsync for the whole Photos library:

  BEFORE (fix_backup.sh):
    rsync entire Pictures/  → 30GB, 4888 files, one shot
    DIES after 18 minutes

  AFTER (fix_backup2.sh):
    rsync Pictures/照片图库.photoslibrary/database/    (133MB) ✓
    rsync Pictures/照片图库.photoslibrary/external/     (0B)    ✓
    rsync Pictures/照片图库.photoslibrary/private/      (3.3GB) ✓
    rsync Pictures/照片图库.photoslibrary/resources/    (1.9GB) ✓
    rsync Pictures/照片图库.photoslibrary/scopes/       (20KB)  ✓
    rsync Pictures/照片图库.photoslibrary/originals/0/  (1.3GB) ✓
    rsync Pictures/照片图库.photoslibrary/originals/1/  (1.9GB) ✓
    ...
    rsync Pictures/照片图库.photoslibrary/originals/F/  (1.2GB) ✓

  Each call is 1-3GB, finishes in 5-15 minutes.
  If one dies, you only redo that one subdir.

THE --partial FLAG:
  Normally when rsync dies, it deletes the incomplete file.
  With --partial, it KEEPS the partial file.
  Next time you run rsync, it resumes from where it stopped
  instead of starting over.

THE --inplace FLAG:
  Normally rsync writes to a temp file, then renames.
  With --inplace, it writes directly to the destination file.
  Combined with --partial, this means true resume capability.

ServerAliveInterval=15:
  Every 15 seconds, SSH sends a tiny "are you still there?" ping.
  Without this, if no data flows for a while (e.g., rsync is
  processing file lists), the router/OS may close the connection.

========================================================================
  TL;DR
========================================================================

The Mac's rsync (v2.6.9, ancient) + SSH over WiFi + 30GB Photos
library = guaranteed timeout. The fix is to break it into 16 small
chunks (one per originals subdirectory) so each chunk finishes
before the connection can die. Run it once, maybe twice if one
chunk fails, and you're done.