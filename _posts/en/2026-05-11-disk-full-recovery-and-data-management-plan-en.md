---
audio: false
generated: true
image: false
lang: en
layout: post
title: Disk Full Recovery and Data Management Plan
translated: false
type: note
---

Yes — let's diagnose first, then fix.

**Current state**: Disk is 100% full. Not just the download — Claude Code itself can't even start bash (can't `mkdir` its session-env directory). So I can't run any commands until you manually free a few MB.

**Fastest unblock**: Delete the half-written `.part` file from the crashed shard. Shard 34 failed, its `.part` is dead weight, and `progress.json` still marks it as pending — deleting it loses zero real progress:

```bash
ls -lh datasets/fineweb-edu/*.part
rm datasets/fineweb-edu/*.part
df -h .
```

Once that frees a few GB, paste the `df -h` output and I'll take over.

**Then we pick a direction** (don't decide yet, just thinking ahead):

1. **Bigger disk**: Does this machine have a larger volume mounted somewhere? 400 GB clearly doesn't fit on the current one. If yes, `mv datasets/fineweb-edu/` to the bigger disk, symlink it back, script resumes transparently.
2. **Cut the target**: 100B tokens is heavy for a "small-scale" ablation. nanoGPT-scale runs use 10–25B (40–100 GB), which likely fits. Lower `TARGET_TOKENS`, re-plan; already-downloaded shards in `progress.json` still get reused.
3. **Switch to streaming**: `load_dataset(..., streaming=True)`, no parquet on disk. But the training side has to be rewritten — probably not worth it.

I'd lean **1** if there's a bigger disk, else **2**. Run the `rm` first and share `df -h`.
