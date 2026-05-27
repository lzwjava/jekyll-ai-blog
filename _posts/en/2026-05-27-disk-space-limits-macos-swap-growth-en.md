---
audio: false
generated: true
image: false
lang: en
layout: post
title: Disk Space Limits macOS Swap Growth
translated: false
type: note
---

Bad news — **you can't manually increase swap on macOS**. The kernel manages it automatically, and there's no setting (GUI or CLI) to change the swap size.

Here's your current situation:

```
Swap:   2048 MB total, 1222 MB used (encrypted)
Disk:   460 GB total, 425 GB used, only 12 GB FREE (98% full!)
RAM:    16 GB
Compressor: ~16.5 GB being compressed
```

**The real problem is your disk is almost full.** With only 12 GB free, macOS can't grow swap even if it wants to. The system is memory-starved — heavy compressor usage (1M+ pages) and swap exhaustion mean you're thrashing.

What you can do:

1. **Free disk space** — this is the most impactful thing. You need at least 10-15% free (~45-70 GB) for healthy swap + swapfile growth. Some quick wins:

```
# Check what's eating space
du -sh ~/Library/Caches/*
du -sh ~/Downloads
# Empty trash
rm -rf ~/.Trash/*
# Clear Xcode derived data if present
rm -rf ~/Library/Developer/Xcode/DerivedData
# Clear Homebrew cache
brew cleanup --prune=all
# Clear pip/uv cache
pip cache purge
uv cache prune
```

2. **Close memory-heavy apps** — Safari with many tabs, Electron apps (Slack, VS Code, Discord) are typical offenders. `Activity Monitor -> Memory` sorted by usage.

3. **If you need more memory headroom long-term** — the M2 Air has unified memory, not upgradeable. The 16 GB limit is physical. Your options:
   - Use lighter apps (Arc instead of Chrome, etc.)
   - Keep fewer apps/tabs open simultaneously
   - For GPU/ML work, use your workstation (RTX 4070, 62 GB RAM) — that's what it's for

Bottom line: clean up that disk. 12 GB free on a 460 GB drive is the bottleneck, not swap configuration.