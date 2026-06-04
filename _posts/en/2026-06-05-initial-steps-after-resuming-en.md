---
audio: false
generated: true
image: false
lang: en
layout: post
title: Initial Steps After Resuming
translated: false
type: note
---

Training is running. Here's the status:

```
Config:  window_pattern="L"  ✓  (fixed, no SSSL warning)
Resumed: step 10,000 -> training from step 10,001
Target:  87,000 steps
Speed:   ~55,700 tok/sec, ~1,177ms/step
ETA:     ~1,511 minutes (~25.2 hours remaining)

CORE eval at step 10k:  0.1168
Validation bpb:         0.9402

Initial samples (same as before - model hasn't learned new stuff yet):
  - "capital of France" -> still wrong ("south of the country")
  - "5x+3=13" -> still looping
```

First training steps just started (10001, 10002, 10003). Loss ~2.97. Running smooth. It'll checkpoint at step 20k.
