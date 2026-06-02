---
audio: false
generated: true
image: false
lang: en
layout: post
title: Mastering ncdu for Disk Cleanup
translated: false
type: note
---

## What is ncdu?

**ncdu** = **NCurses Disk Usage**. It's an interactive terminal tool that shows you exactly which folders and files are consuming disk space, with a visual tree you can navigate and explore in real-time. Think of it as a "disk usage explorer" — much faster and more intuitive than piping `du` commands.

---

## Installation

```bash
brew install ncdu
```

On Linux:

```bash
sudo apt install ncdu    # Debian/Ubuntu
sudo yum install ncdu    # Red Hat/CentOS
```

---

## Basic Usage

**Scan your entire home directory:**

```bash
ncdu ~
```

**Scan a specific folder:**

```bash
ncdu ~/Downloads
```

**Scan the entire system (requires sudo):**

```bash
sudo ncdu /
```

**Exclude certain directories (faster scan):**

```bash
ncdu --exclude node_modules --exclude .git ~/Projects
```

---

## Understanding the Interface

When ncdu launches, you'll see something like this:

```
 ncdu 1.16 ~ Total: 245.3 GiB  Apparent size: 120.4 GiB  Items: 89543

 --- /Users/yourname ---
  45.2 GiB [####################] /Library
  32.1 GiB [####################] /Projects
  28.5 GiB [####################] /Downloads
  12.3 GiB [####################] /Applications
   8.7 GiB [####################] /Desktop
   ...
```

**What each column means:**

- **Left number** = Size of that folder/file
- **Bar graph** = Visual representation of relative size
- **Folder/file name** = The path

---

## Keyboard Navigation

| Key | Action |
|-----|--------|
| **↑ / ↓** | Move up/down in the list |
| **→ / Enter** | Open/expand a folder |
| **← / Backspace** | Go back to parent folder |
| **d** | Delete selected file/folder (with confirmation) |
| **q** | Quit ncdu |
| **n** | Sort by name |
| **s** | Sort by size (largest first) |
| **a** | Sort by apparent size |
| **?** | Show help menu |
| **r** | Refresh/rescan current directory |
| **i** | Show file details (permissions, dates, etc.) |
| **c** | Show child count |
| **e** | Export results to file |
| **g** | Toggle percentage/graph display |

---

## Common Workflows

### 1. **Find and Delete Large Folders**

```bash
ncdu ~/Downloads
```

1. Press `↓` to navigate to the largest folder
2. Press `→` to expand and see what's inside
3. Find the culprit (old videos, backups, etc.)
4. Press `d` to delete
5. Confirm with `y`

### 2. **Scan Entire Home Directory**

```bash
ncdu ~
```

Great for finding "mystery space hogs." Common culprits:

- `~/Library/Caches` — Old app caches (safe to delete)
- `~/Library/Logs` — Accumulated logs
- `~/Downloads` — Old files you forgot about
- `~/.Trash` — Emptied files that didn't fully delete
- `~/Applications` — Old/duplicate apps

### 3. **Find Large Files (Not Just Folders)**

By default, ncdu shows folders. To see individual large **files**:

1. Press `→` to expand a folder
2. Look for files with large sizes
3. Files show without a trailing `/`

### 4. **Compare Folder Sizes Side-by-Side**

```bash
ncdu ~/Projects
```

Then use **`s`** to sort by size. Instantly see which project folder is the largest.

### 5. **Exclude Junk and Speed Up Scan**

```bash
ncdu --exclude node_modules --exclude .git --exclude .venv --exclude venv ~
```

Skips heavy but non-essential folders (dependencies, version control, virtual environments).

---

## Advanced Usage

### Export Results to a File

Press **`e`** inside ncdu to export to a text file (useful for reporting).

```bash
ncdu ~ --output results.txt
```

Then view it later:

```bash
ncdu --file results.txt
```

### Scan and Immediately Delete Large Items

```bash
ncdu -r ~
```

The `-r` flag prevents deletion confirmation (use carefully!).

### Non-Interactive Mode (Just Print Totals)

```bash
ncdu -0 ~ | head -20
```

Shows output in a simple format without the interactive UI.

### Ignore Mounted Volumes

```bash
ncdu --one-file-system ~
```

Doesn't cross into mounted drives/networks (good for avoiding scanning external drives).

---

## Pro Tips

### Tip 1: Check macOS System Bloat

```bash
ncdu ~/Library
```

Navigate to:

- `Caches` — Old app cache files (often safe to delete)
- `Logs` — Accumulated system logs
- `Application Support` — App-specific data (be careful here)

### Tip 2: Find Duplicate Files

While ncdu doesn't find duplicates directly, you can spot patterns:

```bash
ncdu ~/Downloads
```

Look for multiple copies of movies, archives, or installers.

### Tip 3: Monitor Size Growth Over Time

Export results at different times:

```bash
ncdu --output ~/Desktop/scan_$(date +%Y%m%d).txt ~
```

Compare outputs later to see what grew.

### Tip 4: Use with `find` for Surgical Deletion

Find all files larger than 1GB:

```bash
find ~ -size +1G -type f
```

Then open ncdu to visualize before deleting manually.

### Tip 5: Clean Up macOS Caches Safely

```bash
sudo ncdu ~/Library/Caches
```

Navigate each cache folder and delete with **`d`**. Most are safe to remove (apps will recreate them).

---

## Common Deletion Scenarios

### Scenario 1: Clean Downloads Folder

```bash
ncdu ~/Downloads
```

1. Sort by size (`s`)
2. Find old .dmg installers, zip files, old projects
3. Press `→` to confirm what's in a folder
4. Press `d` to delete

### Scenario 2: Remove Old Xcode/Developer Caches

```bash
ncdu ~/Library/Developer
```

Contains old simulators, build artifacts — often hundreds of GB. Navigate and selectively delete old versions.

### Scenario 3: Flush Node Package Dependencies

```bash
ncdu ~/Projects
```

Navigate into each project, check `node_modules` folder size, delete if you have a `package.json` (you can reinstall with `npm install`).

---

## Comparison with Other Tools

| Tool | Best For | Speed | Ease |
|------|----------|-------|------|
| **ncdu** | Interactive exploration & deletion | Fast | 🟢 Easy |
| **du** | Quick CLI one-liners | Very fast | 🟡 Medium |
| **dust** | Pretty CLI output | Fast | 🟡 Medium |
| **Grand Perspective** | Visual GUI overview | Medium | 🟢 Easy |

---

## Troubleshooting

**ncdu hangs on certain folders?**

```bash
ncdu --exclude .git --exclude node_modules ~
```

**Permission denied errors?**

```bash
sudo ncdu ~
```

**Want to scan but NOT have delete permissions?**

```bash
ncdu -r ~    # Read-only mode
```

---

## Quick Cheat Sheet

```bash
ncdu ~                           # Start scanning home
ncdu ~/Downloads                 # Scan Downloads
sudo ncdu /                      # Scan entire system
ncdu --exclude node_modules ~    # Skip heavy folders
ncdu --one-file-system ~         # Don't follow mounts
```

**Inside ncdu:**

- **↑↓** = navigate
- **→** = expand folder
- **←** = back
- **d** = delete
- **s** = sort by size
- **q** = quit

---

This should give you everything you need to master ncdu and reclaim disk space! Let me know if you hit any snags.
