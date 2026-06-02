---
audio: false
generated: true
image: false
lang: en
layout: post
title: Optimizing Data Transfer Costs Simplifies
translated: false
type: note
---

Yes, moving data across regions costs time (network transfer). DO doesn't have a "hyper link" between regions — it goes over public internet, roughly 100-500 Mbps, so 100 GB = ~30 min to a few hours.

But honestly, the simplest approach: **just recreate the GPU droplet when ready, download and prep data directly on it.** Data download + tokenization for GPT-2 training data is maybe 1-2 hours of GPU time = ~$4-8. Not worth optimizing around.

**The real cost is idle time, not compute time.**

Here's the math:

| Approach | Cost |
|----------|------|
| GPU droplet idle for 1 week while prepping data on CPU | $336 GPU idle + $16 CPU |
| GPU droplet on for 2 hrs to download + tokenize, then train | $4-8 for prep + training cost |

**Recommendation:** Keep things simple.

1. Delete the atl1 volume ($10/mo saved) — you have no data on it
2. Delete all snapshots except `gpu-mi300x-snapshot-20260601` ($7/mo saved)
3. When ready to train: recreate GPU droplet from snapshot, download data from HuggingFace, tokenize, train
4. Total idle cost: **~$1.53/mo** (just the snapshot)

Want me to clean up and go this route?
