---
audio: false
generated: true
image: false
lang: en
layout: post
title: 70GB Git Garbage Found
translated: false
type: note
---

Found it. Here's the breakdown of your 460GB disk:

| Item | Size | % of Data |
| ------ | ------ | ----------- |
| **projects/lzwjava.github.io git** | **~70 GB** | **17%** |
| WeChat | 21 GB | 5% |
| Docker | 8 GB | 2% |
| Claude (Hermes/agents) | 10 GB | 2% |
| JetBrains | 6.5 GB | 2% |
| Other projects (70 repos) | ~40 GB | 10% |
| Caches | ~10 GB | 2% |
| Applications | 38 GB | 9% |
| App Support misc | ~25 GB | 6% |
| Other (system, dotfiles, QQ, etc.) | ~190 GB | 45% |
| **Free** | **5.9 GB** | **—** |

**The two big findings:**

1. **lzwjava.github.io git repo — 70 GB total, 43 GB in pack files + 27 GB in garbage pack files.** This is the main culprit. `git count-objects` shows 55 pack files totalling 43 GiB, plus **~27 GiB of orphaned tmp_pack_* garbage** — those are left over from interrupted repack/gc operations. The working tree (`_site/`, `README.md`) is only ~302 MB; everything else is git history and orphaned temp files.

2. **`~27 GB of garbage`tmp_pack_*` files** sitting in `.git/objects/pack/`. Those can be safely removed.

**Action plan:**

```
cd ~/projects/lzwjava.github.io
rm -f .git/objects/pack/tmp_*
git repack -a -d --depth=250 --window=250
git gc --prune=now --aggressive
```

That will: (a) delete 27 GB of orphaned temp packs, (b) deduplicate 55 pack files into one, and (c) reclaim maybe 20+ GB more from delta optimization. This repo has 35M objects in packs — it's been accumulating cruft for years.

Want me to run this cleanup? It'll take a couple minutes but should free ~50 GB+.

Also worth looking at: WeChat (21 GB in Containers — it stores images/videos), Docker (8 GB), and Claude (10 GB — likely conversation history).
