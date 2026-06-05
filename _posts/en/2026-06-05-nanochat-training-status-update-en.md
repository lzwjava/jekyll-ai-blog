---
audio: false
generated: true
image: false
lang: en
layout: post
title: Nanochat Training Status Update
translated: false
type: note
---

Here's the nanochat training status from tmux session 0 (sessions 7/12 don't exist — only 0 and 14 are active, both showing the same training output):

```
Progress:  step 60841 / 87,000  (69.93%)
Loss:      ~2.99  (healthy, stable)
LR:        0.49
Speed:     ~55,660 tok/sec, ~1,177 ms/step
Elapsed:   1,193 minutes  (~19.9 hours)
ETA:       ~513 minutes   (~8.5 hours)
Epoch:     1
GPU:       RTX 4070 @ 100% util, 55% mem, 66°C, 211W
```

Summary:

- About 70% done, roughly 26,160 steps remaining
- At ~1.18 sec/step, that's ~8.6 hours left (ETA confirms ~513 min)
- Loss is stable around 2.98-3.02 — training is healthy
- GPU is maxed out and running cool at 66°C

So you're looking at finishing around ~9-10pm tonight if no interruptions.
