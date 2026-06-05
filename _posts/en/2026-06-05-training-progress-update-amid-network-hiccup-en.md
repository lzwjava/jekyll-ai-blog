---
audio: false
generated: true
image: false
lang: en
layout: post
title: Training Progress Update Amid Network Hiccup
translated: false
type: note
---

Training is alive and well! The LAN IP was unreachable (probably the router/switch hiccuped), but Tailscale works. Here's the update:

```
Progress:  step 66,141 / 87,000  (76.02%)
Loss:      ~2.91  (down from ~2.99 earlier — improving!)
LR:        0.40  (cosine schedule winding down)
Speed:     ~55,670 tok/sec, ~1,177 ms/step  (rock steady)
Elapsed:   1,297 minutes  (~21.6 hours)
ETA:       ~409 minutes   (~6.8 hours)
```

Key changes since last check (~1 hour ago):

- Steps advanced: 60,841 → 66,141 (+5,300 steps, ~1.15 hr)
- Progress: 70% → 76% (+6%)
- Loss: 2.99 → 2.91 (noticeable drop — good sign)
- LR: 0.49 → 0.40 (cosine decay in effect)
- ETA: 513 min → 409 min (consistent)

ETA points to finishing around **~4:30-5:00 AM** tonight. Training is healthy and stable.

Note: LAN IP 192.168.1.36 is currently unreachable (100% packet loss), but the machine is fine — use the Tailscale IP `100.111.30.44` to reach it.
