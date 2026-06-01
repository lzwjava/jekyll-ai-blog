---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 降低GPU云成本
translated: true
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

还有两个较旧的快照你可能想要清理：

| Snapshot | Size | Cost/mo |
|----------|------|---------|
| `7.2-gpu-mi300x1-...-1779256307024` (原始 AMD 镜像) | 132.77 GiB | $6.64 |
| `snap-snapshots-gpu-mi300x1-...-0530-2331` | 6.58 GiB | $0.33 |
| `gpu-mi300x-snapshot-20260601` (你的) | 30.62 GiB | $1.53 |

要我删除那两个旧的？那样每月能省约 $7。原始 AMD 镜像在重建时随时可以从 AMD Dev Cloud 获取新的。