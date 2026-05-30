---
audio: false
generated: true
image: false
lang: en
layout: post
title: Methodology for macOS Disk Space Investigation
translated: false
type: note
---

Here's the methodology:

## 1. Start broad — where is the space?

```bash
df -h /
```

Shows total disk, used, and available. This tells you how urgent it is and sets a baseline to measure against.

## 2. Top-level home directory scan

```bash
du -sh ~/* ~/.* 2>/dev/null | sort -rh | head -20
```

`du -sh` = disk usage, summarized, human-readable. This reveals which top-level directories are the biggest — typically `~/Library`, `~/projects`, `~/.cargo`, etc. You drill into the biggest ones next.

## 3. Known macOS hotspots

These are locations that commonly accumulate junk on macOS. You check each one:

```bash
# App caches (safe to delete, apps rebuild them)
du -sh ~/Library/Caches/* 2>/dev/null | sort -rh | head -20

# App logs
du -sh ~/Library/Logs/* 2>/dev/null | sort -rh | head -10

# Docker VM image (huge even when Docker isn't running)
du -sh ~/Library/Containers/com.docker.docker 2>/dev/null

# Homebrew installed packages + cached downloads
du -sh /opt/homebrew 2>/dev/null
du -sh /opt/homebrew/Cellar/* 2>/dev/null | sort -rh | head -10
du -sh ~/Library/Caches/Homebrew/downloads/* 2>/dev/null | sort -rh | head -5

# Language-specific caches
du -sh ~/.npm ~/.yarn ~/.bun ~/.cargo ~/.rustup 2>/dev/null | sort -rh
du -sh ~/Library/Caches/pip 2>/dev/null

# JetBrains IDEs (caches + app support)
du -sh ~/Library/Caches/JetBrains 2>/dev/null
du -sh ~/Library/Application\ Support/JetBrains 2>/dev/null

# Xcode
du -sh ~/Library/Developer/Xcode/* 2>/dev/null | sort -rh
```

The pattern: `du -sh <path>/* | sort -rh | head -N` — list all children, sort by size descending, show top N.

## 4. Project build artifacts (often the biggest)

```bash
# Rust target dirs — massive, rebuildable
du -sh ~/projects/*/target 2>/dev/null | sort -rh

# Node modules
du -sh ~/projects/*/node_modules 2>/dev/null | sort -rh
```

These are the #1 space hog for developers. A single `cargo build` can produce 5-27GB in `target/`.

## 5. Find recently modified large files

```bash
find ~ -type f -size +100M -mtime -7 2>/dev/null
```

This catches things actively growing — files over 100MB modified in the last 7 days. If disk keeps growing, run this and look for patterns (same file getting bigger, or new files appearing in the same directory).

## 6. Monitor live writes (if still growing)

```bash
sudo fs_usage -w -f disk 2>/dev/null | head -50
```

This is a macOS-specific tool that watches filesystem activity in real-time. Shows exactly which process is writing to which file. Useful when you can't figure out what's eating space.

## Summary of the pattern

```
df -h                          # how bad is it?
du -sh ~/* | sort -rh          # where are the big dirs?
du -sh <bigdir>/* | sort -rh   # drill into each big dir
find ~ -size +100M -mtime -7   # what's growing recently?
fs_usage                       # what's writing right now?
```

It's just repeated `du -sh | sort -rh` drilling down from biggest to smallest, combined with domain knowledge of where macOS/dev tools stash their junk.