---
audio: false
generated: true
image: false
lang: en
layout: post
title: Combining Multi-Part RAR Files
translated: false
type: note
---

Question: How do you combine multi-part RAR files (part1.rar, part2.rar) into a single archive?

Answer:

Multi-part RAR files are designed to be extracted together automatically — you don't need to manually "combine" them first. Here's how:

**Method 1: Extract directly (recommended)**
Just open or extract `part1.rar` — the RAR tool will automatically pull in `part2.rar` and reassemble the original file.

```bash
# Using unrar (Linux/macOS)
unrar x part1.rar

# Using rar
rar e part1.rar
```

**Method 2: Combine into a single RAR using CLI**

```bash
# Step 1: Extract
unrar x part1.rar ./output/

# Step 2: Re-pack into one archive
rar a combined.rar ./output/*
```

**Method 3: Using WinRAR (Windows GUI)**

1. Right-click `part1.rar`
2. Select **"Extract Here"** or **"Extract to folder"**
3. WinRAR auto-reads all parts

> ⚠️ **Important:** All parts (`part1.rar`, `part2.rar`, etc.) must be in the **same folder** before extracting.

**Naming conventions to be aware of:**

| Old format | New format |
| --- | --- |
| `archive.part1.rar` | `archive.part1.rar` |
| `archive.r00`, `archive.r01` | `archive.part2.rar` |

References:

- [RAR and WinRAR Official Documentation](https://www.win-rar.com/documentation.html)
- [unrar man page](https://linux.die.net/man/1/unrar)
