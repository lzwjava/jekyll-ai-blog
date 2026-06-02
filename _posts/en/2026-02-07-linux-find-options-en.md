---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: Mastering Linux Find Command Options
translated: false
type: note
---

The `find` command is one of the most powerful tools in Unix/Linux for searching files and directories. Here's a thorough guide to its options and capabilities.

## Basic Syntax

```bash
find [path...] [expression]
```

## Starting Points and Paths

You can specify one or more starting directories:

```bash
find /home /var /tmp -name "*.log"    # Search multiple directories
find . -name "file.txt"                # Current directory
find / -name "config"                  # Entire filesystem
```

## Tests and Filters

**Name-based searches:**
- `-name pattern` - Case-sensitive name match (supports wildcards)
- `-iname pattern` - Case-insensitive name match
- `-path pattern` - Match full path
- `-ipath pattern` - Case-insensitive path match
- `-regex pattern` - Match path with regular expression
- `-iregex pattern` - Case-insensitive regex

```bash
find . -name "*.txt"
find . -iname "README*"
find . -regex ".*\.(jpg|png|gif)"
```

**Type-based searches:**
- `-type f` - Regular files
- `-type d` - Directories
- `-type l` - Symbolic links
- `-type b` - Block devices
- `-type c` - Character devices
- `-type p` - Named pipes (FIFOs)
- `-type s` - Sockets

```bash
find /var -type d -name "log*"
find . -type f -name "*.sh"
```

**Size-based searches:**
- `-size n[cwbkMG]` - File size (c=bytes, w=2-byte words, b=512-byte blocks, k=KB, M=MB, G=GB)
- Use `+` for greater than, `-` for less than, no prefix for exact

```bash
find . -size +100M              # Larger than 100MB
find . -size -1k                # Smaller than 1KB
find /var/log -size +50M -size -100M  # Between 50-100MB
```

**Time-based searches:**
- `-mtime n` - Modified n days ago
- `-atime n` - Accessed n days ago
- `-ctime n` - Status changed n days ago
- `-mmin n` - Modified n minutes ago
- `-amin n` - Accessed n minutes ago
- `-cmin n` - Status changed n minutes ago
- `-newer file` - Modified more recently than file
- `-newerXY reference` - More flexible time comparisons

```bash
find . -mtime -7                # Modified in last 7 days
find . -mtime +30               # Modified more than 30 days ago
find . -mmin -60                # Modified in last hour
find . -newer reference.txt     # Newer than reference.txt
```

**Permission-based searches:**
- `-perm mode` - Exact permission match
- `-perm -mode` - All specified bits are set
- `-perm /mode` - Any specified bits are set

```bash
find . -perm 644                # Exactly 644
find . -perm -644               # At least 644
find /bin -perm /u+s,g+s        # SUID or SGID set
```

**Ownership searches:**
- `-user name` - Owned by user
- `-group name` - Owned by group
- `-uid n` - Owned by user ID
- `-gid n` - Owned by group ID
- `-nouser` - No valid user owner
- `-nogroup` - No valid group owner

```bash
find /home -user john
find . -nouser                  # Find orphaned files
```

**Depth control:**
- `-maxdepth n` - Descend at most n levels
- `-mindepth n` - Don't search above n levels
- `-depth` - Process directory contents before the directory itself

```bash
find . -maxdepth 2 -name "*.txt"
find . -mindepth 3 -type f
```

**Other useful tests:**
- `-empty` - Empty files or directories
- `-executable` - Executable files
- `-readable` - Readable files
- `-writable` - Writable files
- `-links n` - Files with n hard links
- `-inum n` - Files with inode number n
- `-samefile name` - Files referring to the same inode

```bash
find . -empty -type d           # Empty directories
find /usr/bin -executable -type f
```

## Logical Operators

Combine tests with logical operators:
- `-a` or `-and` - AND (default if omitted)
- `-o` or `-or` - OR
- `-not` or `!` - NOT
- `( expression )` - Grouping (escape parentheses in shell)

```bash
find . -name "*.txt" -o -name "*.md"
find . -type f -not -name "*.log"
find . \\( -name "*.c" -o -name "*.h" \\) -a -mtime -7
```

## Actions

**Display actions:**
- `-print` - Print full path (default)
- `-print0` - Print with null separator (safe for xargs -0)
- `-printf format` - Custom format output
- `-ls` - List in ls -dils format
- `-fls file` - Like -ls but write to file

```bash
find . -name "*.txt" -print0
find . -printf "%p\t%s bytes\n"
```

**Execution actions:**
- `-exec command {} \;` - Execute command for each file
- `-exec command {} +` - Execute command with multiple files
- `-execdir command {} \;` - Execute from file's directory
- `-ok command {} \;` - Like -exec but asks for confirmation

```bash
find . -name "*.tmp" -exec rm {} \;
find . -type f -exec chmod 644 {} +
find . -name "*.jpg" -execdir convert {} {}.png \;
```

**Deletion:**
- `-delete` - Delete matched files (be careful!)

```bash
find . -name "*.bak" -delete
find . -type f -empty -delete
```

**Other actions:**
- `-quit` - Exit immediately after first match
- `-prune` - Don't descend into directory

```bash
find . -name ".git" -prune -o -type f -print
```

## Practical Examples

```bash
# Find large files in home directory
find ~ -type f -size +500M -exec ls -lh {} \;

# Find and archive old log files
find /var/log -name "*.log" -mtime +90 -exec gzip {} \;

# Find broken symbolic links
find . -type l ! -exec test -e {} \; -print

# Find files modified today
find . -type f -mtime 0

# Find world-writable files (security check)
find / -perm -002 -type f 2>/dev/null

# Find setuid files (security audit)
find / -perm -4000 -type f 2>/dev/null

# Count files by extension
find . -type f | sed 's/.*\.//' | sort | uniq -c

# Find duplicate filenames
find . -type f -printf "%f\n" | sort | uniq -d

# Clean up temporary files
find /tmp -type f -atime +7 -user $(whoami) -delete
```

## Performance Tips

- Put most restrictive tests first
- Use `-maxdepth` early to limit searching
- Use `-prune` to skip directories
- Use `-print0` with `xargs -0` for filenames with spaces
- Redirect stderr to avoid permission errors: `2>/dev/null`

The `find` command is incredibly flexible and can be combined with other Unix tools through pipes and command substitution to create powerful file management workflows.
