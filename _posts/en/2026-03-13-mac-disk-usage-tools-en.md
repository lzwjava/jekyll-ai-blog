---
audio: false
generated: true
image: false
lang: en
layout: post
title: Mac Disk Usage Tools Guide
translated: false
type: note
---

You're looking for **`du`** (disk usage) — it's the classic CLI tool for this on macOS. Here are the most practical approaches:

## Quick commands with `du`

**Find largest directories in current folder:**
```bash
du -sh */ | sort -hr
```
- `-s` = summary (total per directory)
- `-h` = human-readable (GB, MB, etc.)
- `sort -hr` = sort by size descending

**Find largest items recursively:**
```bash
du -sh ./* | sort -hr | head -20
```

**For a specific path (e.g., Downloads):**
```bash
du -sh ~/Downloads/* | sort -hr | head -10
```

---

## Better alternatives (more interactive)

**`ncdu`** — This is probably what you're remembering. It's interactive and makes exploring huge folders easy:
```bash
brew install ncdu
ncdu ~/Downloads
```
Then navigate with arrow keys, press `d` to delete, `q` to quit. Much more user-friendly than raw `du`.

**`dust`** — Rusty alternative, cleaner output:
```bash
brew install dust
dust -r ~/Downloads  # -r = reverse sort (largest first)
```

---

## GUI tools (if you prefer pointing & clicking)

- **Disk Diag** — Shows what's taking up space visually
- **Grand Perspective** — Free, visual tree of your disk
- **CleanMyMac** — Paid, but scans and suggests cleanups automatically

---

## One-liner to nuke large old files

Delete files older than 30 days over 100MB:
```bash
find ~/Downloads -type f -mtime +30 -size +100m -delete
```

**Which tool rings a bell?** If `ncdu` isn't it, let me know — there's also `lsof` for tracking what's currently using space, or `fsearch` for fast file searching.
