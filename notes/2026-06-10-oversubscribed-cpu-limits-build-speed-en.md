---
audio: false
generated: true
image: false
lang: en
layout: post
title: Oversubscribed CPU Limits Build Speed
translated: false
type: note
---

Here's the verdict based on live system state:

**System:** 20 CPU cores, 235GB RAM (218GB available)

**Current build (MAX_JOBS=32):**
- 32 active clang-22 processes, all CPU-saturated (50-90% each)
- Progress: 1158/2525 objects (~46%)
- Load average: 34.4 — already 1.7x oversubscribed
- RAM usage: ~17GB of 235GB (plenty of headroom)

**Can you set MAX_JOBS=64?**

Technically yes, but it will NOT help and will likely hurt:

- **CPU bottleneck:** 20 cores × 100% = 20 full cores of work. With 32 jobs you're already at ~170% utilization. Adding 32 more jobs just means more context switching between the same 20 cores.
- **RAM is fine:** 64 jobs would use ~12-50GB, well under 235GB.
- **Diminishing returns:** The build is CPU-bound, not memory-bound. You'd see load average jump to ~60+, but actual compilation rate would stay flat or drop due to scheduler thrashing.
- **Risk:** Occasional OOM kills from transient spikes, or hipcc failures from resource starvation.

**Recommendation:** Keep it at 32. With 20 cores, the sweet spot is probably 20-24 jobs. Going above that just adds contention. If you want faster builds, the bottleneck is the number of CPU cores, not job count.
