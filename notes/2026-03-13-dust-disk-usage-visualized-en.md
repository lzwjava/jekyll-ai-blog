---
audio: false
generated: true
image: false
lang: en
layout: post
title: Dust Disk Usage Visualized Fast
translated: false
type: note
---

## What is dust?

**dust** = A faster, more beautiful alternative to `du`. It's a Rust-based CLI tool that shows disk usage in a tree format with color-coded output, progress bars, and intuitive sorting. It's designed to be prettier and more performant than traditional `du`, with a simpler command syntax.

**Key difference from `du`:** dust is optimized for quick scanning and visual clarity, while `du` is more "raw" and verbose.

---

## Installation

```bash
brew install dust
```

On Linux:
```bash
cargo install du-dust    # If you have Rust/Cargo
sudo apt install dust    # Debian/Ubuntu (some distros)
```

On macOS with MacPorts:
```bash
sudo port install dust
```

Verify installation:
```bash
dust --version
```

---

## Basic Usage

**Scan current directory:**
```bash
dust
```

**Scan a specific folder:**
```bash
dust ~/Downloads
```

**Scan home directory:**
```bash
dust ~
```

**Scan entire system (requires sudo):**
```bash
sudo dust /
```

---

## Understanding the Output

When you run `dust`, you'll see something like:

```
 45.6 GiB │████████████████████│ Library
 28.3 GiB │█████████████        │ Projects
 18.7 GiB │██████████           │ Downloads
 12.1 GiB │██████               │ Applications
  8.4 GiB │████                 │ Desktop
  6.2 GiB │███                  │ Documents
```

**What each column means:**
- **First number** = Size of the folder
- **Bar graph** = Visual representation (colored, proportional)
- **Folder name** = The directory name

**By default, dust:**
- Sorts by size (largest first)
- Shows only the top-level items
- Uses colors for better readability
- Includes a nice visual bar graph

---

## Command-Line Options

### Sorting & Display

| Flag | What It Does |
|------|-------------|
| `-r` | Reverse sort (smallest to largest) |
| `-s` | Sort by size (default) |
| `-n` | Sort by name alphabetically |
| `-d` | Sort by date modified |
| `-e` | Sort by file extension |
| `-c` | Show with color output (default) |
| `-C` | Disable color output |

### Limiting & Filtering

| Flag | What It Does |
|------|-------------|
| `-n <num>` | Show only top N results (e.g., `-n 20`) |
| `-d <depth>` | Limit recursion depth (e.g., `-d 2`) |
| `-X` | Exclude files matching regex |
| `-i` | Ignore case-sensitive matching |
| `-z` | Exclude hidden files |

### Output & Display

| Flag | What It Does |
|------|-------------|
| `-b` | Print sizes in bytes |
| `-k` | Print sizes in kilobytes |
| `-m` | Print sizes in megabytes |
| `-g` | Print sizes in gigabytes |
| `-T` | Display total with tree structure |
| `-L` | Use ASCII instead of Unicode |
| `-p` | Print percent of parent directory |
| `-A` | Aggregate small files |
| `-h` | Show help |

---

## Common Usage Patterns

### 1. **Find Largest Folders in Downloads**

```bash
dust ~/Downloads
```

Output shows folders ranked by size, largest first.

### 2. **Limit to Top 10 Results**

```bash
dust -n 10 ~
```

Shows only the 10 largest items in home directory.

### 3. **Show Only 2 Levels Deep**

```bash
dust -d 2 ~
```

Great for getting a high-level overview without drilling too deep:

```
 85.4 GiB │████████████████████│ Library
          │                    │   ├─ Caches (32.1 GiB)
          │                    │   ├─ Application Support (28.7 GiB)
          │                    │   └─ Logs (12.8 GiB)
 45.2 GiB │███████████         │ Projects
          │                    │   ├─ LargeProject (28.3 GiB)
          │                    │   └─ OtherProject (16.9 GiB)
```

### 4. **Reverse Sort (Smallest First)**

```bash
dust -r ~/Downloads
```

Useful to see what's actually important vs. taking up space.

### 5. **Exclude Certain Files/Folders**

```bash
dust -X 'node_modules|\.git' ~
```

Skip heavy dependencies and version control:

```bash
dust -X '\.cache|venv' ~/Projects
```

### 6. **Show Percentages**

```bash
dust -p ~
```

Shows what percentage of the parent each folder represents:

```
 45.6 GiB (38%) │████████████████████│ Library
 28.3 GiB (24%) │█████████████        │ Projects
 18.7 GiB (16%) │██████████           │ Downloads
 12.1 GiB (10%) │██████               │ Applications
```

### 7. **Scan Entire System**

```bash
sudo dust -n 20 /
```

Top 20 largest directories on your Mac.

### 8. **Show Total Size with Tree**

```bash
dust -T ~
```

Includes a summary tree showing cumulative sizes.

### 9. **Ignore Hidden Files**

```bash
dust -z ~
```

Excludes dotfiles and hidden folders (faster scan).

### 10. **Custom Unit Display**

Show sizes in megabytes:
```bash
dust -m ~/Downloads
```

Or gigabytes:
```bash
dust -g ~
```

---

## Real-World Scenarios

### Scenario 1: Clean Up macOS System Bloat

```bash
sudo dust -d 2 ~/Library | head -20
```

Look for:
- `Caches` — Safe to delete
- `Logs` — Safe to delete (usually)
- `Application Support` — Check before deleting

Then drill deeper:

```bash
dust ~/Library/Caches -n 15
```

### Scenario 2: Find Largest Projects

```bash
dust -d 2 ~/Projects -n 10
```

Identify which projects are consuming the most space.

### Scenario 3: Check Downloads for Old Installers

```bash
dust -d 1 ~/Downloads | grep -E '\.dmg|\.zip|\.iso'
```

Or just:

```bash
dust ~/Downloads -n 20
```

### Scenario 4: Monitor Disk Usage Growth

Scan periodically and compare:

```bash
dust -n 15 ~ > ~/Desktop/disk_usage_$(date +%Y%m%d).txt
```

Compare outputs to see what's growing.

### Scenario 5: Find Old Node/Python Caches

```bash
dust -X 'node_modules|__pycache__|\.venv' ~
```

Avoids showing dependency folders, focuses on actual code/data.

### Scenario 6: Scan Without Following Symlinks

```bash
dust ~/Applications
```

Works great for applications folder without descending into bundles.

---

## Advanced Combinations

### Find Large Files in Downloads, Show Top 5

```bash
dust ~/Downloads -n 5
```

### Get Full Tree of Largest Item

```bash
dust -d 10 ~/Library -n 1
```

Shows the entire tree structure of the single largest item.

### Export Results to File

```bash
dust -C ~ > disk_usage.txt
```

`-C` disables colors so the text file is clean.

### Pretty Print with Percentages and Top 20

```bash
dust -p -n 20 ~
```

### Scan Multiple Folders at Once

```bash
dust ~/Downloads ~/Projects ~/Library
```

Shows all three folders' top-level contents compared.

### Find Files Larger Than a Certain Size

```bash
dust ~ -d 10 | grep GiB
```

Filters output to show only items in gigabytes (aka "large").

---

## dust vs du vs ncdu: Quick Comparison

| Feature | `du` | `dust` | `ncdu` |
|---------|------|--------|--------|
| **Speed** | ⚡⚡ Very fast | ⚡⚡⚡ Fastest | ⚡⚡ Fast |
| **Visual** | Plain text | Beautiful, colored | Interactive |
| **Ease** | Hard (many flags) | Easy | Easy |
| **Interactive** | No | No | ✅ Yes |
| **Sorting** | Manual | Built-in | Built-in |
| **Deletion** | Manual | Manual | ✅ Direct delete |
| **Best for** | Scripts/piping | Quick overview | Exploring & cleaning |

**When to use each:**
- **`dust`** — You want a quick, pretty summary: `dust ~/Downloads`
- **`du`** — You're scripting or need raw data: `du -sh */ | sort -hr`
- **`ncdu`** — You need to interactively explore and delete: `ncdu ~`

---

## Pro Tips

### Tip 1: Create an Alias for Common Scans

Add to `~/.zshrc` or `~/.bash_profile`:

```bash
alias dusthome='dust -p ~'
alias dustsys='sudo dust -p /'
alias dustdown='dust ~/Downloads'
alias dustlibs='sudo dust ~/Library -d 2'
```

Then just:
```bash
dustdown
```

### Tip 2: Combine with `watch` for Real-Time Monitoring

```bash
watch -n 5 'dust -n 10 ~'
```

Updates every 5 seconds (good for monitoring active downloads).

### Tip 3: Compare Two Directories

```bash
dust ~/OldProject ~/NewProject
```

Side-by-side comparison of what's largest.

### Tip 4: Find Duplicate-Sized Files

While dust can't detect actual duplicates, you can spot suspicious patterns:

```bash
dust -d 5 ~/Downloads | grep -E '500 MiB|1 GiB'
```

### Tip 5: Check Application Size

```bash
dust /Applications -d 1 -n 20
```

See which apps are taking the most space.

### Tip 6: Aggregate Small Files Together

```bash
dust -A ~/Downloads
```

The `-A` flag combines small items into "Other" for cleaner output.

---

## Combining dust with Other Tools

### Use with grep to Filter

Show only items with "GiB" (large items):
```bash
dust ~ | grep GiB
```

### Pipe to head for Top N

```bash
dust ~ | head -15
```

### Find Large Caches

```bash
dust ~/Library/Caches -d 3 -n 20
```

### Check Specific File Types

```bash
dust ~ -d 5 | grep -E '\.iso|\.dmg|\.zip'
```

---

## Troubleshooting

**dust takes too long?**
```bash
dust -z -X 'node_modules|\.git' ~
```
Skip hidden files and large dependency folders.

**Want to exclude multiple patterns?**
```bash
dust -X 'node_modules|\.git|\.cache|__pycache__' ~
```

**Permission denied?**
```bash
sudo dust /
```

**Want plain text output (no colors)?**
```bash
dust -C ~ > results.txt
```

---

## Quick Cheat Sheet

```bash
dust                           # Scan current dir
dust ~                         # Scan home
dust ~/Downloads               # Scan specific folder
dust -n 20 ~                   # Show top 20
dust -d 2 ~                    # Show 2 levels deep
dust -p ~                      # Show percentages
dust -r ~/Downloads            # Reverse sort (smallest first)
dust -X 'node_modules|\.git' ~ # Exclude patterns
dust -c ~/Library/Caches       # Count files (not available, but useful combo)
sudo dust /                    # Scan entire system
dust -C ~ > output.txt         # Export without colors
```

---

## Summary

`dust` is perfect for:
- ✅ Quick disk usage overview
- ✅ Finding space hogs fast
- ✅ Pretty, colored output
- ✅ Simple command syntax
- ✅ Scripting & piping results

Use **dust** when you want speed and readability, use **ncdu** when you want to interactively explore and delete, and use **du** when you're scripting or need maximum control.

Let me know if you have questions!
