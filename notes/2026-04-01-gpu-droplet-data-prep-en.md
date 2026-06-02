---
audio: false
generated: true
image: false
lang: en
layout: post
title: Prepare Data on GPU Droplet Instead
translated: false
type: note
---

Exactly right — your current VPS has **10GB disk + 512MB RAM**, which can't handle 61GB input + ~30GB output = **~91GB total**.

But here's the better approach: **Don't prepare on VPS at all.**

## Recommended: Prepare on GPU Droplet

```
┌─────────────────┐    just transfer raw     ┌─────────────────┐
│   VPS (current) │  ─── 61GB text file ───  │  GPU Droplet    │
│  1 vCPU, 512MB  │      (rsync/scp)        │  (has GPU + big │
│   10GB disk     │                          │   disk + RAM)   │
└─────────────────┘                          └────────┬────────┘
                                                     │
                                            run prepare.py here
                                                     │
                                            ~30GB .bin files
                                            ready for training
```

### On GPU Droplet (big disk, fast CPU):
```bash
# Transfer raw text file
rsync -avz --progress root@159.89.216.20:/root/zz/datasets/fineweb_extracted_all.txt ./

# Link and prepare (uses GPU droplet's resources)
ln -sf fineweb_extracted_all.txt ./data/fineweb/train_fineweb.txt
python data/fineweb/prepare_fineweb.py

# Then train immediately on the same machine
python train.py config/train_fineweb.py
```

### Why This Makes Sense

| Task | VPS | GPU Droplet |
|------|-----|-------------|
| **Prepare data** | ❌ Too weak | ✅ Powerful CPU + big disk |
| **Train model** | ❌ No GPU | ✅ Has GPU |
| **Host code** | ✅ Fine | ✅ Fine |

**VPS just stores the raw 61GB file. GPU droplet does all the heavy work.**

What specs does your GPU droplet have?
