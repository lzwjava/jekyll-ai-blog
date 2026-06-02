---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: Mastering Linux Find Command
translated: false
type: note
---

The `find` command is one of the most powerful tools for searching files and directories in Linux. It recursively searches through directory hierarchies based on criteria you specify.

## Basic Syntax

```bash
find [path...] [expression]
```

## Common Use Cases

**Search by filename:**
```bash
find /path -name "filename.txt"
find /path -iname "*.pdf"  # case-insensitive
```

**Search by file type:**
```bash
find /path -type f  # files only
find /path -type d  # directories only
find /path -type l  # symbolic links
```

**Search by size:**
```bash
find /path -size +100M  # larger than 100MB
find /path -size -1k    # smaller than 1KB
find /path -size 50M    # exactly 50MB
```

**Search by modification time:**
```bash
find /path -mtime -7   # modified in last 7 days
find /path -mtime +30  # modified more than 30 days ago
find /path -mmin -60   # modified in last 60 minutes
```

**Search by permissions:**
```bash
find /path -perm 644   # exactly 644
find /path -perm -644  # at least 644
find /path -perm /u+w  # user has write permission
```

**Search by owner:**
```bash
find /path -user username
find /path -group groupname
```

**Combining criteria with logical operators:**
```bash
find /path -name "*.log" -and -size +10M
find /path -name "*.txt" -or -name "*.md"
find /path -not -name "*.tmp"
find /path \\( -name "*.jpg" -or -name "*.png" \\) -and -size +1M
```

## Executing Commands on Results

**Delete files:**
```bash
find /path -name "*.tmp" -delete
find /path -name "*.log" -exec rm {} \;
```

**Execute command on each file:**
```bash
find /path -type f -exec chmod 644 {} \;
find /path -name "*.txt" -exec grep "pattern" {} \;
```

**Execute command with multiple files (more efficient):**
```bash
find /path -name "*.txt" -exec grep "pattern" {} +
```

**Interactive confirmation:**
```bash
find /path -name "*.bak" -ok rm {} \;
```

## Advanced Options

**Limit search depth:**
```bash
find /path -maxdepth 2 -name "*.txt"  # search only 2 levels deep
find /path -mindepth 1 -name "*.txt"  # skip the starting directory
```

**Find empty files or directories:**
```bash
find /path -empty
find /path -type f -empty  # empty files only
```

**Find by access/change time:**
```bash
find /path -atime -7   # accessed in last 7 days
find /path -ctime +30  # status changed more than 30 days ago
```

**Find files newer/older than reference:**
```bash
find /path -newer reference_file
find /path -not -newer reference_file
```

**Search multiple paths:**
```bash
find /path1 /path2 /path3 -name "*.conf"
```

**Print results with details:**
```bash
find /path -name "*.txt" -ls
find /path -name "*.txt" -printf "%p - %s bytes\n"
```

## Practical Examples

**Find and compress old log files:**
```bash
find /var/log -name "*.log" -mtime +30 -exec gzip {} \;
```

**Find large files in home directory:**
```bash
find ~ -type f -size +100M -exec ls -lh {} \; 2>/dev/null
```

**Find files modified today:**
```bash
find /path -type f -mtime 0
```

**Find duplicate filenames:**
```bash
find /path -type f -printf "%f\n" | sort | uniq -d
```

**Find and count files by extension:**
```bash
find /path -type f -name "*.jpg" | wc -l
```

**Find world-writable files (security check):**
```bash
find /path -type f -perm -002
```

**Find setuid files (security check):**
```bash
find / -perm -4000 -type f 2>/dev/null
```

## Performance Tips

The `find` command processes options from left to right, so place the most restrictive criteria first for better performance. Use `-name` or `-type` early in your expression, and put expensive operations like `-exec` at the end.

For faster searches on indexed systems, consider using `locate` for simple filename searches, though `find` offers far more flexibility and always shows current filesystem state.
