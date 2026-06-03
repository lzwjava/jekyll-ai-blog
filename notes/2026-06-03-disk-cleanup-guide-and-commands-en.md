---
audio: false
generated: true
image: false
lang: en
layout: post
title: Disk Cleanup Guide and Commands
translated: false
type: note
---

OK here's the full picture. Your disk is at 94% (only 900MB truly free, not 12GB — that was including purgeable space).

TOP SPACE HOGS (sorted by size):

```
 CATEGORY                    SIZE    WHAT TO DO
 ─────────────────────────────────────────────────────────────
 ~/.cache/huggingface/       21 GB   Models you downloaded — safe to prune
 ~/projects/lzwjava.github.io 58 GB  Huge! Check for large media/old posts
 ~/Library/Containers/       37 GB   WeChat 19GB, Docker 8GB, QQ 4.5GB
 ~/.cache/ (total)           31 GB   HF 21GB + torch 4.6GB + pre-commit 3GB + uv 1.3GB
 ~/Library/Caches/           22 GB   JetBrains 7.1GB, Homebrew 3.7GB, pip 2.6GB
 ~/Library/Application Sup.  24 GB   JetBrains 5.4GB, nomic.ai 3.5GB, Lark 2GB
 ~/.npm/                     7.2 GB  Old npm cache
 ~/.cache/torch/             4.6 GB  PyTorch hub models
 ~/Library/Developer/        3.8 GB  CoreSimulator 3.3GB
```

QUICK WINS (safe to delete now, ~40+ GB):

```
# 1. HuggingFace cache (21 GB) — re-download on demand
huggingface-cli scan-cache
huggingface-cli delete-cache

# 2. npm cache (7.2 GB)
npm cache clean --force

# 3. Homebrew cache (3.7 GB)
brew cleanup --prune=all

# 4. pip cache (2.6 GB)
pip3 cache purge

# 5. pre-commit cache (3 GB)
pre-commit clean

# 6. PyTorch hub cache (4.6 GB) — check first
ls ~/.cache/torch/hub/
rm -rf ~/.cache/torch/hub/*

# 7. JetBrains caches (7.1 GB)
rm -rf ~/Library/Caches/JetBrains/*

# 8. uv cache (1.3 GB)
uv cache prune
```

BIGGER CLEANUP (need your call):

```
# WeChat (19 GB!) — open WeChat settings → Storage → Clear
# This is the single biggest easy win after HF cache

# Docker (8 GB) — if not using Docker on Air:
docker system prune -a --volumes

# lzwjava.github.io (58 GB) — what's in there?
du -sh ~/projects/lzwjava.github.io/*/ | sort -rh | head
# Likely large images, videos, or build artifacts
```

Want me to run the safe cleanup commands (items 1-8)? That should free ~40+ GB. For WeChat and the blog repo, I need your decision.
