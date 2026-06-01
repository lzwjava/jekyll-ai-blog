---
audio: false
generated: true
image: false
lang: en
layout: post
title: Reducing GPU Cloud Costs
translated: false
type: note
---

Done. Current status:

```
GPU Droplet:  DESTROYED   (billing stopped)
Snapshot:     30.6 GiB    (~$1.53/mo)
Volume:       100 GiB     (~$10/mo)
────────────────────────────────────────
Total idle cost: ~$11.50/mo  (was ~$2+/hr = ~$1460/mo)
```

There are also 2 older snapshots you might want to clean up:

| Snapshot | Size | Cost/mo |
|----------|------|---------|
| `7.2-gpu-mi300x1-...-1779256307024` (original AMD image) | 132.77 GiB | $6.64 |
| `snap-snapshots-gpu-mi300x1-...-0530-2331` | 6.58 GiB | $0.33 |
| `gpu-mi300x-snapshot-20260601` (yours) | 30.62 GiB | $1.53 |

Want me to delete the two old ones? That'd save ~$7/mo. The original AMD image you can always get fresh from AMD Dev Cloud when recreating.