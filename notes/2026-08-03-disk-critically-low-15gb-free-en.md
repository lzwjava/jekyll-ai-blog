---
audio: false
generated: true
image: false
lang: en
layout: post
title: Disk critically low - 15GB free
translated: false
type: note
---

Yes — the disk is still critically low. Here's the full picture:

## Current status

| | |
|---|---|
| Filesystem `/dev/nvme0n1p2` | **916G total, 854G used, 15G free (99%)** |
| Inodes | 10% used — fine (not the problem) |

The ENOSPC error you're hitting is real: 15G free out of 916G.

## Top space consumers

**`/home/lzw/projects` — 488G**
- `jekyll-ai-blog/fineweb_test_dump` — **88G** (dataset dump)
- `llama.cpp/models` — **72G** (LLM weights)
- `imagenet` — **64G** (dataset)
- `backup.lzwjava.github.io/.git` — **57G** (git objects)
- `coco` — **38G**, `llama` — **31G**, `llama2.c` — **26G**, `open_llama_3b` — **13G**

**`/home/lzw/.cache` — 57G**
- `nanochat/base_checkpoints` — 27G + `chatsft_checkpoints` — 3.8G
- `uv` — 7.8G, `JetBrains` — 6.2G, `whisper` — 4.3G

**Other**
- `/home/lzw/.local/lib` — 38G, `Downloads` — 19G, `qDownloads` — 14G
- `/var` — 21G (`cuda-repo` 3.1G, `log` 2.7G, `crash` 609M)
- `/tmp/pip-unpack-fogsmaol` — 628M (orphaned pip temp dir)

## Safe cleanups I can do right now (~9G, no risk)

- `uv` cache: `uv cache clean` → ~7.8G
- `/var/crash` → 609M
- `/tmp/pip-unpack-*` leftovers → ~630M
- `pip` cache + apt cache

## Bigger wins (need your confirmation)

- `fineweb_test_dump` (88G), `backup.../.git` (57G), `llama.cpp/models` (72G) — these are the real fixes; if any are reproducible/re-downloadable, deleting them frees 50–90G each.

Want me to run the safe cleanups now, and if so, which of the big directories (datasets, models, git backup) are safe to remove?