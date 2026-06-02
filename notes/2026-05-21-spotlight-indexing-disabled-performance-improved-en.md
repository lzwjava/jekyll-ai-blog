---
audio: false
generated: true
image: false
lang: en
layout: post
title: Spotlight Indexing Disabled, Performance Improved
translated: false
type: note
---

Spotlight is **permanently disabled**. Here's what happened:

| Before | After |
|---|---|
| mds_stores: **14 GB RAM** | mds daemon: **471 MB** (idle, 0% CPU) |
| mdworker: **18 processes** eating CPU | **0** |
| Indexing all folders, all the time | **Disabled on all volumes** |
| Post-reboot: 15 min of CPU hell | Post-reboot: nothing |

**What changed**:
- `sudo mdutil -a -i off` — indexing turned off on `/`, `/System/Volumes/Data`, `/System/Volumes/Preboot`
- mds daemon is still alive (Apple locks that) but it's **idle at 471 MB and 0% CPU** instead of 14 GB + 90% CPU
- `Cmd+Space` will still launch apps from the existing index, but won't search file contents or index new files

**To re-enable** if you ever want it back:

```
sudo mdutil -a -i on
```
