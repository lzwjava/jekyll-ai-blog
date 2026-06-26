---
audio: false
generated: true
image: false
lang: en
layout: post
title: 16 GB Freed After macOS Restart
translated: false
type: note
---

Here's what happened — this is normal macOS/APFS behavior:

**The ~16 GB difference (490 → 474 GB) came from:**

1. **Swap files** — Your M2 Air has 16 GB RAM. Before restart, with heavy workload (multiple iOS simulator disk images mounted, LLM tools, etc.), macOS was swapping to disk. Swap gets cleared on reboot. Currently only the 2 GB sleepimage exists, but before restart swap could easily have been 8-12 GB.

2. **APFS local Time Machine snapshots** — macOS creates periodic local snapshots that count as "used" space but are invisible in Finder. Right now there are zero snapshots, confirming they existed before and were released on restart. Each snapshot can be several GB.

3. **Purgeable space** — macOS marks cached iCloud content, system caches, and temporary data as "purgeable." This shows as "used" in disk utilities but gets reclaimed on reboot.

4. **/private/var/folders/** — Temporary files for running processes (currently 942 MB, could have been multi-GB before restart).

**Bottom line:** The 16 GB was always there — macOS was just using your disk as overflow for memory pressure and caching. The restart cleared swap, snapshots, and temp files. This is expected and will happen again as you use the machine.

**Tip:** With only 54 GB free (now ~18 GB free on the data volume), you're running tight. You could reclaim the 14 GB of user caches (`rm -rf ~/Library/Caches/pip`, `Homebrew`, `JetBrains`, `LarkShell` etc.) if you need space.
