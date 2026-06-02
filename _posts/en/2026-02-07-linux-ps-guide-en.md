---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: Mastering Linux ps Command Guide
translated: false
type: note
---

I'll give you a comprehensive introduction to the `ps` command and its options for listing processes.

## What is ps?

The `ps` command displays information about active processes on a Unix/Linux system. It's one of the most fundamental tools for process management and system monitoring.

## Basic Usage

The simplest form shows processes for the current user in the current terminal:

```bash
ps
```

## Common Option Styles

The `ps` command has three different option styles that can be mixed:

1. **Unix options** - preceded by a dash (e.g., `-e`)
2. **BSD options** - no dash (e.g., `aux`)
3. **GNU long options** - two dashes (e.g., `--forest`)

## Most Useful Commands

**See all processes for all users:**

```bash
ps aux          # BSD style
ps -ef          # Unix style
```

**See processes in a tree/hierarchy:**

```bash
ps auxf         # BSD style with forest view
ps -ef --forest # Unix style with tree
```

**See processes for a specific user:**

```bash
ps -u username
ps aux | grep username
```

**See processes by PID:**

```bash
ps -p 1234
ps -p 1234,5678,9101  # multiple PIDs
```

## Key Options Explained

### BSD Style (no dash)

- `a` - show processes for all users
- `u` - display user-oriented format (shows owner, CPU%, memory%, etc.)
- `x` - include processes without a controlling terminal
- `f` - ASCII art process hierarchy/forest
- `w` - wide output (don't truncate command lines)
- `ww` - unlimited width

### Unix Style (with dash)

- `-e` - select all processes
- `-f` - full format listing
- `-l` - long format
- `-u user` - processes for specific user
- `-p pid` - specific process ID(s)
- `-C command` - processes by command name
- `-o format` - custom output format
- `--forest` - ASCII art process tree

## Understanding the Output

When you run `ps aux`, you'll see columns like:

```
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
```

- **USER** - process owner
- **PID** - process ID
- **%CPU** - CPU usage percentage
- **%MEM** - memory usage percentage
- **VSZ** - virtual memory size (KB)
- **RSS** - resident set size (physical memory in KB)
- **TTY** - controlling terminal (? means no terminal)
- **STAT** - process state:
  - `R` - running
  - `S` - sleeping (interruptible)
  - `D` - sleeping (uninterruptible, usually I/O)
  - `T` - stopped
  - `Z` - zombie
  - `<` - high priority
  - `N` - low priority
  - `s` - session leader
  - `+` - foreground process group
- **START** - when process started
- **TIME** - cumulative CPU time
- **COMMAND** - command with arguments

## Custom Output Formats

You can customize which columns to display:

```bash
ps -eo pid,user,%cpu,%mem,command
ps aux --sort=-%cpu | head    # top CPU users
ps aux --sort=-%mem | head    # top memory users
```

## Practical Examples

**Find a specific process:**

```bash
ps aux | grep firefox
```

**Show threads:**

```bash
ps -eLf          # all threads
ps -T -p 1234    # threads for specific PID
```

**Watch processes in real-time:**

```bash
watch -n 1 'ps aux --sort=-%cpu | head -20'
```

**See process with full command line:**

```bash
ps auxww | grep process_name
```

**Count processes:**

```bash
ps aux | wc -l
```

**See process tree from specific process:**

```bash
ps -ef --forest | grep -A 5 process_name
```

## Commonly Used Combinations

```bash
ps aux              # Everything, detailed
ps -ef              # Everything, different format
ps auxf             # Everything with hierarchy
ps -u $(whoami)     # Just your processes
ps -C httpd         # All httpd processes
ps -p $$            # Current shell process
```

## Tips

- For real-time monitoring, consider using `top` or `htop` instead
- Combine with `grep`, `sort`, `head`, and `tail` for filtering
- Use `pgrep` for simpler process searching by name
- The output can be piped to `awk` or `cut` for specific fields

The `ps` command is incredibly versatile. Start with `ps aux` or `ps -ef` for general overview, then add options as needed for more specific information.
