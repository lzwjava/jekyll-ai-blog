---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Counting Items with Linux ls
translated: false
type: note
---

Here are the most common ways to count items (files, directories, lines, etc.) using the `ls` command in Linux/Unix/macOS terminals:

### 1. Count files/directories in the current directory (simple & most common)

```bash
ls | wc -l
```

This pipes the output of `ls` to `wc -l` (word count, lines).
**Warning**: This can give a slightly wrong result if filenames contain newlines. Safer alternatives below.

### 2. Accurate count (recommended)

```bash
ls -1 | wc -l
```

The `-1` (number one) forces `ls` to output exactly one entry per line.

Or even better (works with special characters and newlines in names):

```bash
find . -maxdepth 1 -type f | wc -l          # only regular files
find . -maxdepth 1 -type d | wc -l          # only directories
find . -maxdepth 1 | wc -l                  # files + directories + current dir (.)
```

### 3. One-liner using only ls (no pipe)

```bash
ls -A1 | wc -l    # counts almost everything except . and ..
ls -a1 | wc -l    # counts absolutely everything including . and ..
```

- `-A` = all except `.` and `..`
- `-a` = truly all (including hidden)

### 4. Count only files (exclude directories)

```bash
ls -p | grep -v / | wc -l
```

(`-p` adds `/` to directories, then we filter them out)

Or more reliably:

```bash
find . -maxdepth 1 -type f | wc -l
```

### 5. Count only directories

```bash
ls -d */ | wc -l
```

Or:

```bash
find . -maxdepth 1 -type d | wc -l
```

### 6. Pretty output with a message

```bash
echo "Total items: $(ls -1 | wc -l)"
echo "Files: $(find . -maxdepth 1 -type f | wc -l)"
echo "Directories: $(find . -maxdepth 1 -type d | wc -l)"
```

### Quick cheat sheet

| What you want to count              | Command                              |
|-------------------------------------|--------------------------------------|
| Everything in current folder        | `ls -1 \| wc -l`                     |
| All (including hidden)              | `ls -a1 \| wc -l`                     |
| Only files                          | `find . -maxdepth 1 -type f \| wc -l`|
| Only directories                    | `find . -maxdepth 1 -type d \| wc -l`|
| Files + dirs (excluding . and ..)   | `ls -A1 \| wc -l`                    |

The `find` versions are the most reliable if you have weird filenames. The simple `ls | wc -l` works 99% of the time and is what most people use day-to-day.
