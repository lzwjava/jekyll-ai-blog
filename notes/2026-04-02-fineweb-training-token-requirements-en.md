---
audio: false
generated: true
image: false
lang: en
layout: post
title: FineWeb Token Requirements for Model Training
translated: false
type: note
---

Depends on your goal. For a **1.5B model to be decent**, you'd want ~100B-1T tokens ideally. FineWeb sample-10BT is ~10B tokens — so 60GB (assuming ~1T tokens total in full FineWeb) is a solid chunk but not the full dataset.

**If you want to use the H200 properly:**
- **1.5B model** → needs ~100B tokens for good training. 60GB of FineWeb (~maybe 200B+ tokens?) would be plenty
- **2.8B model** → needs ~200B+ tokens

Can you check how big the fineweb data is on that machine? Run:

```bash
du -sh /root/nanoGPT/data/fineweb/
```

Also — the `sample-10BT` is just a 10B token sample. The full FineWeb is 1.4T tokens. If your 60GB is from the full dataset, you're golden. If it's the 10BT sample, that's only ~10B tokens for 1.5B model — you'll overfit hard.
