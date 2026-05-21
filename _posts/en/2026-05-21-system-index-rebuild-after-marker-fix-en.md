---
audio: false
generated: true
image: false
lang: en
layout: post
title: System Index Rebuild After Marker Fix
translated: false
type: note
---

Here's the result:

| Before | After |
|---|---|
| Load average: **18+** | **7.58** (dropping) |
| mdworker processes: **13** | **0** (gone) |
| mds touching excluded dirs? | **No** — markers working |

**What's still happening**: `mds_stores` at 94% is rebuilding the main system index from scratch (because we erased it). This is a **one-time cost** — it'll finish in ~2 more minutes and settle to near 0%.

**Proof the exclusions worked**: All 13 mdworker processes died immediately after we set the markers. They were the ones crawling your Projects and Caches folders. Now only mds_stores remains, rebuilding just the system + Applications index.

**After today**: Every reboot will see a CPU spike of <30 seconds (not 15 minutes), because the heavy folders stay excluded permanently.