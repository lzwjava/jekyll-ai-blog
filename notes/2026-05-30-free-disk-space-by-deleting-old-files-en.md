---
audio: false
generated: true
image: false
lang: en
layout: post
title: Free Disk Space by Deleting Old Files
translated: false
type: note
---

Here's the picture. You have 460GB disk, only **2.9GB free** (81% used). Here are the top offenders and cleanup commands:

## TOP OFFENDERS

```
  27 GB   ~/projects/warp/target          (Rust build artifacts)
  19 GB   /opt/homebrew                   (Homebrew packages)
  12 GB   ~/Library/JetBrains             (caches + app support)
   8 GB   Docker container data           (not running, safe to nuke)
   8 GB   Bodhi-AI/target + node_modules
   7 GB   ~/.npm                          (npm cache)
   7 GB   ~/Library/Caches/JetBrains
   3.7 GB ~/Library/Caches/Homebrew
   3 GB   various node_modules
   2.5 GB ~/Library/Caches/pip
   2.8 GB ~/.hermes
   1.8 GB ~/.cargo
   1.3 GB LarkShell cache
   1 GB   Playwright browsers
```

## QUICK WINS — Safe to delete now

```bash
# 1. Rust target dirs (biggest win — 34+ GB)
rm -rf ~/projects/warp/target
rm -rf ~/projects/Bodhi-AI/target
rm -rf ~/projects/zenith/bamboo/target

# 2. npm cache (7 GB)
npm cache clean --force

# 3. Docker (8 GB, Docker isn't even running)
rm -rf ~/Library/Containers/com.docker.docker

# 4. Homebrew cache (3.7 GB)
brew cleanup --prune=all

# 5. JetBrains caches (7 GB, won't break projects)
rm -rf ~/Library/Caches/JetBrains

# 6. pip cache (2.5 GB)
pip cache purge

# 7. Playwright browsers (1 GB, only if you don't need them)
npx playwright uninstall --all

# 8. Homebrew download cache leftovers
rm -f ~/Library/Caches/Homebrew/downloads/*.dmg
```

## MEDIUM — Review first

```bash
# JetBrains app support (5.4 GB) — only if you don't need old IDE versions
du -sh ~/Library/Application\ Support/JetBrains/*

# Unused Homebrew formulae (llvm alone is 1.7 GB)
brew leaves           # list manually installed
brew uninstall <pkg>  # remove ones you don't use
```

## MONITORING — If disk keeps growing

```bash
# Watch what's being written right now
sudo fs_usage -w -f disk 2>/dev/null | head -50

# Or find files modified in last hour
find ~ -type f -mmin -60 -size +10M 2>/dev/null

# Quick recheck of total usage
du -sh ~/projects ~/Library ~/.npm ~/.cargo ~/.hermes 2>/dev/null
```

The Rust `target` dirs alone would free ~34GB. That's your biggest win — they rebuild on next `cargo build` but it's worth it with 2.9GB free. Want me to run any of these for you?